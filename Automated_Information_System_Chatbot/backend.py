from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory, flash
from flask_mail import Mail, Message
import sqlite3
import os
import json
import datetime
import hashlib
import secrets
import re
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
from openai import OpenAI
from werkzeug.security import generate_password_hash, check_password_hash
from pywebpush import webpush, WebPushException
from dotenv import load_dotenv

load_dotenv()

VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY')
VAPID_CLAIMS = { "sub": "mailto:ambarawa.lapas@gmail.com" }

app = Flask(__name__)
app.config.update(
    MAIL_SERVER    = os.getenv('MAIL_SERVER'),
    MAIL_PORT      = int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS   = os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USERNAME  = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD  = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Chatbot Lapas Ambarawa', 'no-reply@lapasambarawa.com')
)

def send_reset_email(to, link):
    """
    Kirim email berisi link reset password.
    """
    msg = Message(
        subject="Reset Password Your App",
        recipients=[to]
    )
    msg.body = f"""
    Hai,

    Kamu meminta reset password. Klik link berikut untuk membuat password baru:

    {link}

    Jika ini bukan kamu, abaikan email ini.
    """
    # (Bisa juga msg.html = render_template('email/reset_password.html', link=link))
    mail.send(msg)

mail = Mail(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def send_push(subscription_info, payload):
    print("Sending push to subscription:", subscription_info)
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
    except WebPushException as ex:
        print("WebPush error:", ex)
        if hasattr(ex, 'response') and ex.response:
            print("Status code:", ex.response.status_code, "Body:", ex.response.text)
        else:
            print("No response attribute on exception; kemungkinan error network atau library.")

CORS(app)  # Enable CORS for all routes
app.secret_key = os.getenv('SECRET_KEY')
# Tambahkan konfigurasi session yang lebih aman
app.config['SESSION_COOKIE_SECURE'] = False  # Hanya HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Tidak bisa diakses via JavaScript
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=1)  # Session timeout
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Setup OpenAI API (Tempatkan di bagian konfigurasi)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
openai.api_key = app.config['OPENAI_API_KEY']

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_openai_response(question, context="", intent=None, confidence=None):
    """Enhanced OpenAI integration with better prompting and error handling"""
    # Validasi input bermakna terlebih dahulu
    if not is_meaningful_input(question):
        return None
        
    try:
        if not app.config['OPENAI_API_KEY']:
            print("OpenAI API key tidak dikonfigurasi")
            return None
            
        client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
        
        # Jika intent belum ada, deteksi terlebih dahulu
        if intent is None or confidence is None:
            intent, confidence = detect_intent(question)
        
        # Jika setelah deteksi masih tidak ada intent yang valid, return None
        if intent == "unknown" or confidence < 0.2:
            return None
        
        # Enhance system prompt with intent awareness
        system_prompt = """
        Kamu adalah chatbot resmi Lapas 2 Ambarawa yang membantu memberikan informasi kepada pengunjung dan keluarga narapidana.
        Berikan jawaban yang singkat, informatif, dan bermanfaat berdasarkan konteks yang diberikan.
        Jawaban harus dalam Bahasa Indonesia yang sopan dan formal.
        
        Jika tidak mengetahui jawaban dengan pasti, katakan "Maaf, saya tidak memiliki informasi lengkap mengenai hal tersebut. 
        Silakan hubungi petugas Lapas 2 Ambarawa melalui nomor (024) 123456 untuk informasi yang lebih akurat."
        
        Pastikan jawaban tidak terlalu panjang (maksimal 3-4 kalimat) agar nyaman dibaca di aplikasi mobile.
        """
        
        # Add intent-specific instructions untuk SEMUA intent
        CONFIDENCE_THRESHOLD = 0.7
        
        if intent == "jadwal_kunjungan" and confidence > CONFIDENCE_THRESHOLD:
            system_prompt += "\nFokus pada informasi jadwal kunjungan dengan menyebutkan hari, waktu, dan jenis pengunjung secara jelas."
        elif intent == "persyaratan_kunjungan" and confidence > CONFIDENCE_THRESHOLD:
            system_prompt += "\nFokus pada syarat-syarat yang diperlukan untuk berkunjung, terutama dokumen identitas dan prosedur."
        elif intent == "layanan_kesehatan" and confidence > CONFIDENCE_THRESHOLD:
            system_prompt += "\nFokus pada informasi layanan kesehatan yang tersedia, jadwal dokter, dan prosedur jika narapidana sakit."
        elif intent == "kontak_info" and confidence > CONFIDENCE_THRESHOLD:
            system_prompt += "\nFokus pada informasi kontak seperti nomor telepon, alamat, email, dan cara menghubungi petugas."
        elif intent == "program_rehabilitasi" and confidence > CONFIDENCE_THRESHOLD:
            system_prompt += "\nFokus pada program pembinaan, rehabilitasi, kegiatan, dan pelatihan yang tersedia untuk narapidana."
        
        # Better conversation prompt structure
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Konteks tentang Lapas 2 Ambarawa:\n{context}\n\nPertanyaan pengunjung: {question}"}
        ]
        
        # Enhanced API parameters
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.5,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        answer = response.choices[0].message.content
        
        # Simple answer validation
        if answer == "UNKNOWN" or "tidak memiliki informasi" in answer.lower():
            return None
            
        return answer
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

# Database initialization
def init_db():
    conn = sqlite3.connect('lapas_chatbot.db')
    cursor = conn.cursor()
    
    # FAQ Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT NOT NULL,
        keywords TEXT NOT NULL
    )
    ''')
    
    # Visiting Schedule Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visiting_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        time TEXT NOT NULL,
        visitor_type TEXT NOT NULL,
        notes TEXT
    )
    ''')
    
    # Requirements Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requirements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL
    )
    ''')
    
    # Health Services Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        schedule TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # Contact Information Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value TEXT NOT NULL,
        category TEXT NOT NULL
    )
    ''')
    
    # Rehabilitation Programs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rehabilitation_programs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_name TEXT NOT NULL,
        description TEXT NOT NULL,
        schedule TEXT
    )
    ''')
    
    # User Messages Log
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        session_id TEXT,
        response_quality TEXT
    )
    ''')
    
    # User Table (for admin access)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT    UNIQUE NOT NULL,
        email       TEXT    UNIQUE NOT NULL,
        password_hash TEXT  NOT NULL,
        role        TEXT    NOT NULL DEFAULT 'user',
        token       TEXT,
        locked_until DATETIME DEFAULT NULL,
        failed_attempts INTEGER NOT NULL DEFAULT 0
    );
    ''')

    # Device Tokens Table untuk Push Notification
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS device_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        platform TEXT NOT NULL,
        last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Chat Analysis Table untuk metrik
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        total_chats INTEGER DEFAULT 0,
        ai_responses INTEGER DEFAULT 0,
        successful_responses INTEGER DEFAULT 0,
        failed_responses INTEGER DEFAULT 0
    )
    ''')
    
    # Modifikasi chat_history untuk menambah metrik
    cursor.execute("PRAGMA table_info(chat_history)")
    existing = [row[1] for row in cursor.fetchall()]

    # 2. Jika belum ada, baru tambahkan
    if 'response_quality' not in existing:
        cursor.execute('''
            ALTER TABLE chat_history
            ADD COLUMN response_quality TEXT
        ''')
    # Insert sample data
    insert_sample_data(conn, cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(conn, cursor):
    # Check if data already exists
    if cursor.execute("SELECT COUNT(*) FROM faq").fetchone()[0] == 0:
        # Sample FAQ data with keywords for better matching
        faq_data = [
            ("Apa jam kunjungan di Lapas?", "Jam kunjungan bervariasi berdasarkan hari dan jenis pengunjung. Silakan lihat jadwal lengkap di bagian Jadwal Kunjungan.", "kunjungan", "jam kunjungan jadwal besuk jenguk waktu berkunjung datang"),
            ("Apa saja persyaratan untuk mengunjungi tahanan?", "Persyaratan utama adalah membawa KTP/identitas yang valid, berpakaian sopan, dan mendaftar di loket pendaftaran. Lihat detail lengkap di bagian Persyaratan.", "kunjungan", "syarat persyaratan dokumen bawa perlu diperlukan ktp identitas"),
            ("Bagaimana jika tahanan sakit?", "Lapas 2 Ambarawa memiliki layanan kesehatan dengan dokter jaga. Untuk kasus darurat, tahanan akan dirujuk ke RS terdekat.", "kesehatan", "sakit kesehatan dokter medis perawatan obat"),
            ("Apa saja program rehabilitasi yang tersedia?", "Kami memiliki berbagai program rehabilitasi termasuk pelatihan keterampilan, pendidikan kesetaraan, pembinaan keagamaan, dan konseling.", "rehabilitasi", "program rehabilitasi kegiatan pelatihan binaan keterampilan belajar pendidikan"),
            ("Bagaimana cara mengirim barang kepada tahanan?", "Barang dapat dikirim saat jam kunjungan dengan melalui pemeriksaan petugas. Ada batasan jenis dan jumlah barang yang diperbolehkan.", "kunjungan", "kirim barang kiriman paket bawaan titip"),
            ("Apakah ada transportasi umum ke Lapas?", "Ya, Lapas 2 Ambarawa dapat diakses dengan angkutan umum dari terminal Ambarawa. Anda juga dapat menggunakan ojek online.", "umum", "transportasi angkutan umum kendaraan bis bus ojek taksi ke sampai"),
            ("Berapa lama waktu kunjungan yang diperbolehkan?", "Waktu kunjungan maksimal adalah 30 menit per kunjungan sesuai dengan jadwal yang telah ditetapkan.", "kunjungan", "lama durasi waktu kunjungan berapa lama menit jam"),
            ("Larangan apa saja saat berkunjung ke Lapas?", "Senjata, obat terlarang, minuman beralkohol, peralatan elektronik, uang tunai melebihi Rp 500.000", "kunjungan", "syarat persyaratan larangan Barang Terlarang dilarang tidak boleh"),
            ("Bagaimana cara menghubungi petugas Lapas?", "Anda dapat menghubungi Lapas 2 Ambarawa melalui nomor telepon (024) 123456 atau email info@lapas2ambarawa.go.id", "kontak", "hubungi kontak telepon nomor telp hp email alamat")
        ]
        cursor.executemany("INSERT INTO faq (question, answer, category, keywords) VALUES (?, ?, ?, ?)", faq_data)
        
        # Sample visiting schedule
        schedule_data = [
            ("Senin", "09.00 - 12.00 WIB", "Tahanan", "Harap datang 30 menit sebelum jadwal berakhir"),
            ("Selasa", "09.00 - 12.00 WIB", "Narapidana", "Harap datang 30 menit sebelum jadwal berakhir"),
            ("Rabu", "09.00 - 12.00 WIB", "Tahanan", "Harap datang 30 menit sebelum jadwal berakhir"),
            ("Kamis", "09.00 - 12.00 WIB", "Narapidana", "Harap datang 30 menit sebelum jadwal berakhir"),
            ("Jumat", "13.00 - 15.00 WIB", "Keluarga Jauh", "Khusus pengunjung dengan jarak tempuh >100km")
        ]
        cursor.executemany("INSERT INTO visiting_schedule (day, time, visitor_type, notes) VALUES (?, ?, ?, ?)", schedule_data)
        
        # Sample requirements
        requirements_data = [
            ("Identitas", "KTP/SIM/Paspor yang masih berlaku", "kunjungan"),
            ("Dokumen Pendukung", "Surat keterangan keluarga (jika mengunjungi kerabat)", "kunjungan"),
            ("Pakaian", "Pakaian sopan (tidak ketat, tidak transparan, tidak pendek)", "kunjungan"),
            ("Prosedur", "Mendaftar di loket pendaftaran minimal 30 menit sebelum jam kunjungan berakhir", "kunjungan"),
            ("Barang Bawaan", "Barang yang diperbolehkan: makanan (tanpa kemasan kaleng/kaca), pakaian (maksimal 2 stel), obat-obatan (dengan resep dokter)", "kunjungan"),
            ("Barang Terlarang", "Barang yang dilarang: senjata, obat terlarang, minuman beralkohol, peralatan elektronik, uang tunai melebihi Rp 500.000", "kunjungan")
        ]
        cursor.executemany("INSERT INTO requirements (title, description, category) VALUES (?, ?, ?)", requirements_data)
        
        # Sample health services
        health_services_data = [
            ("Klinik Umum", "Senin-Jumat: 08.00-16.00 WIB", "Layanan pemeriksaan kesehatan umum oleh dokter dan paramedis"),
            ("Dokter Umum", "Senin, Rabu, Jumat: 09.00-14.00 WIB", "Konsultasi dan pemeriksaan oleh dokter umum"),
            ("Dokter Gigi", "Selasa: 09.00-13.00 WIB", "Perawatan dan konsultasi kesehatan gigi"),
            ("Psikolog", "Kamis: 10.00-14.00 WIB", "Konseling dan terapi psikologis"),
            ("Layanan Darurat", "24 jam", "Penanganan kasus darurat dengan koordinasi RS terdekat")
        ]
        cursor.executemany("INSERT INTO health_services (service_name, schedule, description) VALUES (?, ?, ?)", health_services_data)
        
        # Sample contact information
        contacts_data = [
            ("Kantor Utama", "(024) 123456", "telepon"),
            ("Layanan Informasi", "(024) 654321", "telepon"),
            ("Layanan Kesehatan", "(024) 123789", "telepon"),
            ("Email Umum", "info@lapas2ambarawa.go.id", "email"),
            ("Email Pengaduan", "pengaduan@lapas2ambarawa.go.id", "email"),
            ("Alamat", "Jl. Lapas No. 123, Ambarawa, Jawa Tengah", "alamat")
        ]
        cursor.executemany("INSERT INTO contacts (name, value, category) VALUES (?, ?, ?)", contacts_data)
        
        # Sample rehabilitation programs
        rehab_programs_data = [
            ("Pembinaan Keagamaan", "Program pembinaan mental spiritual untuk berbagai agama yang dilaksanakan secara rutin", "Setiap hari sesuai jadwal ibadah"),
            ("Pelatihan Keterampilan Menjahit", "Pelatihan keterampilan menjahit untuk bekal keterampilan setelah bebas", "Senin & Rabu: 10.00-12.00 WIB"),
            ("Pelatihan Pertukangan", "Pelatihan keterampilan pertukangan kayu untuk bekal keterampilan", "Selasa & Kamis: 10.00-12.00 WIB"),
            ("Pelatihan Komputer", "Pelatihan dasar penggunaan komputer dan internet", "Jumat: 10.00-12.00 WIB"),
            ("Program Pertanian", "Program bertani di lahan Lapas untuk pengembangan keterampilan", "Setiap hari: 07.00-09.00 WIB"),
            ("Pendidikan Kesetaraan", "Program pendidikan Paket A, B, dan C bekerja sama dengan Dinas Pendidikan", "Senin-Jumat: 13.00-15.00 WIB"),
            ("Konseling Kelompok", "Program konseling psikologi secara berkelompok", "Kamis: 10.00-12.00 WIB")
        ]
        cursor.executemany("INSERT INTO rehabilitation_programs (program_name, description, schedule) VALUES (?, ?, ?)", rehab_programs_data)
 
        admin_user = ("admin", "suniabernardo@gmail.com", generate_password_hash("admin123"), "admin")
        cursor.execute("INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)", admin_user)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('lapas_chatbot.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_auth_token(username, role):
    """Generate authentication token for API"""
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    token_data = {
        'username': username,
        'role': role,
        'exp': expiry.timestamp()
    }
    # Menggunakan SECRET_KEY untuk signing
    payload = json.dumps(token_data)
    token = hashlib.sha256((payload + app.secret_key).encode()).hexdigest()
    
    # Simpan token ke database
    conn = get_db_connection()
    try:
        # Tambahkan kolom token jika belum ada
        cursor = conn.execute('PRAGMA table_info(users)')
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'token' not in columns:
            conn.execute('ALTER TABLE users ADD COLUMN token TEXT')
            
        conn.execute('UPDATE users SET token = ? WHERE username = ?', (token, username))
        conn.commit()
    finally:
        conn.close()
        
    return token

def validate_token(token):
    """Validate authentication token"""
    if not token:
        return False
        
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
        
        if not user:
            return False
            
        # Verifikasi expiry
        token_data = get_token_data(token)
        if token_data and 'exp' in token_data:
            if datetime.datetime.utcnow().timestamp() > token_data['exp']:
                return False
                
        return user
    finally:
        conn.close()

def get_token_data(token):
    """Extract data from token"""
    # Cari token di database untuk mendapatkan username
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT username, role FROM users WHERE token = ?', (token,)).fetchone()
        if not user:
            return None
            
        # Recreate token untuk mendapatkan data
        for exp_days in range(30, -1, -1):
            expiry = datetime.datetime.utcnow() + datetime.timedelta(days=exp_days)
            token_data = {
                'username': user['username'],
                'role': user['role'],
                'exp': expiry.timestamp()
            }
            payload = json.dumps(token_data)
            test_token = hashlib.sha256((payload + app.secret_key).encode()).hexdigest()
            
            if test_token == token:
                return token_data
                
        return None
    finally:
        conn.close()


def process_question(question):
    question_normalized = question.lower().strip()
    
    # Enhanced input validation - filter meaningless input
    if not is_meaningful_input(question_normalized):
        return generate_meaningless_input_response(), "meaningless"
    
    if is_thank_you(question_normalized):
        return handle_thank_you(), "gratitude"
    
    if is_greeting(question_normalized):
        return handle_greeting(), "greeting"
  
    if is_goodbye(question_normalized):
        return handle_goodbye(), "goodbye"

    # 1) Deteksi intent dulu dan ambil yang confidence tertinggi
    intent, confidence = detect_intent(question_normalized)
    
    # Set threshold yang konsisten
    CONFIDENCE_THRESHOLD = 0.7
    
    if confidence > CONFIDENCE_THRESHOLD:
        if intent == "jadwal_kunjungan":
            return get_visiting_schedule(), "database"
        elif intent == "persyaratan_kunjungan":
            return get_requirements(), "database"
        elif intent == "layanan_kesehatan":
            return get_health_services(), "database"
        elif intent == "kontak_info":
            return get_contact_info(), "database"
        elif intent == "program_rehabilitasi":
            return get_rehabilitation_programs(), "database"

    # 2) Baru cek FAQ di database - dengan validasi tambahan
    conn = None
    try:
        conn = get_db_connection()
 
        # 2a) Cek kecocokan langsung di pertanyaan FAQ
        exact_match = conn.execute(
            'SELECT answer FROM faq WHERE LOWER(question) LIKE ?', 
            ('%' + question_normalized + '%',)
        ).fetchone()
        
        if exact_match:
            return exact_match['answer'], "database"
            
        # 2b) Jika tidak ada exact match, coba keyword matching dengan validasi
        keywords = extract_keywords(question_normalized)
        if keywords and len(keywords) > 0:  # Pastikan ada keywords yang valid
            # Hanya cari jika ada minimal 1 keyword yang panjangnya > 2
            valid_keywords = [k for k in keywords if len(k) > 2]
            if valid_keywords:
                for keyword in valid_keywords:
                    matches = conn.execute(
                        'SELECT answer FROM faq WHERE keywords LIKE ? OR question LIKE ?', 
                        ('%' + keyword + '%', '%' + keyword + '%')
                    ).fetchall()
                    if matches:
                        return matches[0]['answer'], "database"
    
    finally:
        if conn:
            conn.close()

    # 3) Jika tidak ketemu di FAQ, panggil OpenAI sebagai fallback
    # Gunakan intent dan confidence yang sudah didapat sebelumnya
    context = get_relevant_context(question_normalized, intent, confidence)
    openai_answer = get_openai_response(question_normalized, context, intent, confidence)
    if openai_answer:
        return openai_answer, "ai"

    # 4) Default response
    return generate_default_response(), "default"

def is_meaningful_input(text):
    """
    Validasi apakah input adalah teks yang bermakna
    Filter out single characters, gibberish, dan input yang tidak bermakna
    """
    if not text or text.isspace():
        return False
    
    # Filter single character (kecuali yang bermakna seperti emoji atau punctuation yang valid)
    if len(text) == 1:
        # Allow meaningful single characters
        meaningful_single_chars = ['?', '!', '👍', '👌', '🙏', '❤️', '😊']
        return text in meaningful_single_chars
    
    # Filter input yang hanya berisi karakter berulang
    if len(set(text.replace(' ', ''))) <= 1:  # Semua karakter sama
        return False
    
    # Filter input yang hanya berisi angka tanpa konteks
    if text.isdigit():
        return False
    
    # Filter input yang hanya berisi simbol tanpa huruf
    if not re.search(r'[a-zA-Z\u00C0-\u017F\u0100-\u024F]', text):  # No letters (including accented)
        # Kecuali emoji atau simbol yang bermakna
        meaningful_symbols = ['?', '!', '👍', '👌', '🙏', '❤️', '😊', '😢', '😭', '🤔']
        return any(symbol in text for symbol in meaningful_symbols)
    
    # Filter gibberish - teks yang tidak memiliki pola kata yang wajar
    words = text.split()
    if words:
        # Cek rasio vokal dan konsonan
        total_chars = sum(len(word) for word in words)
        if total_chars > 3:
            vowels = sum(text.lower().count(v) for v in 'aiueoàáâãäåæèéêëìíîïòóôõöøùúûü')
            vowel_ratio = vowels / total_chars
            # Rasio vokal yang wajar dalam bahasa Indonesia/Inggris
            if vowel_ratio < 0.1 or vowel_ratio > 0.8:
                return False
    
    # Filter kata-kata yang sangat pendek tanpa makna
    meaningful_words = []
    for word in words:
        if len(word) >= 2:  # Minimal 2 karakter
            meaningful_words.append(word)
        elif word.lower() in ['a', 'i', 'u', 'o', 'e']:  # Huruf vokal tunggal bisa bermakna dalam konteks
            continue
        else:
            # Single character yang tidak bermakna
            continue
    
    # Jika tidak ada kata bermakna, return False
    if not meaningful_words and len(words) > 0:
        # Cek apakah ada kata pendek yang bermakna dalam bahasa Indonesia
        indonesian_short_words = ['ya', 'ok', 'iya', 'hai', 'hi', 'eh', 'ah', 'oh', 'wah', 'hm']
        if not any(word.lower() in indonesian_short_words for word in words):
            return False
    
    return True

def get_visiting_schedule():
    conn = get_db_connection()
    schedules = conn.execute('SELECT day, time, visitor_type, notes FROM visiting_schedule ORDER BY CASE day WHEN "Senin" THEN 1 WHEN "Selasa" THEN 2 WHEN "Rabu" THEN 3 WHEN "Kamis" THEN 4 WHEN "Jumat" THEN 5 WHEN "Sabtu" THEN 6 WHEN "Minggu" THEN 7 END').fetchall()
    conn.close()
    
    result = "<h3>Jadwal Kunjungan Lapas 2 Ambarawa</h3><table style='width:100%; border-collapse: collapse;'>"
    result += "<tr><th style='border:1px solid #ddd; padding:8px;'>Hari</th><th style='border:1px solid #ddd; padding:8px;'>Waktu</th><th style='border:1px solid #ddd; padding:8px;'>Jenis Pengunjung</th><th style='border:1px solid #ddd; padding:8px;'>Catatan</th></tr>"
    
    for schedule in schedules:
        result += f"<tr><td style='border:1px solid #ddd; padding:8px;'>{schedule['day']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{schedule['time']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{schedule['visitor_type']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{schedule['notes'] or '-'}</td></tr>"
    
    result += "</table>"
    return result

def get_requirements():
    conn = get_db_connection()
    requirements = conn.execute('SELECT title, description FROM requirements WHERE category = "kunjungan" ORDER BY id').fetchall()
    conn.close()
    
    result = "<h3>Persyaratan Kunjungan</h3><ul style='list-style-type: disc; padding-left:20px;'>"
    
    for req in requirements:
        result += f"<li><strong>{req['title']}:</strong> {req['description']}</li>"
    
    result += "</ul>"
    return result

def get_health_services():
    conn = get_db_connection()
    services = conn.execute('SELECT service_name, schedule, description FROM health_services ORDER BY id').fetchall()
    conn.close()
    
    result = "<h3>Layanan Kesehatan</h3><table style='width:100%; border-collapse: collapse;'>"
    result += "<tr><th style='border:1px solid #ddd; padding:8px;'>Layanan</th><th style='border:1px solid #ddd; padding:8px;'>Jadwal</th><th style='border:1px solid #ddd; padding:8px;'>Deskripsi</th></tr>"
    
    for service in services:
        result += f"<tr><td style='border:1px solid #ddd; padding:8px;'>{service['service_name']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{service['schedule']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{service['description']}</td></tr>"
    
    result += "</table>"
    return result

def get_contact_info():
    conn = get_db_connection()
    contacts = conn.execute('SELECT name, value, category FROM contacts ORDER BY category, id').fetchall()
    conn.close()
    
    result = "<h3>Informasi Kontak</h3>"
    
    categories = {}
    for contact in contacts:
        cat = contact['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(contact)
    
    for cat, items in categories.items():
        result += f"<h4>{cat.capitalize()}</h4><ul style='list-style-type: disc; padding-left:20px;'>"
        for item in items:
            result += f"<li><strong>{item['name']}:</strong> {item['value']}</li>"
        result += "</ul>"
    
    return result

def get_rehabilitation_programs():
    conn = get_db_connection()
    programs = conn.execute('SELECT program_name, description, schedule FROM rehabilitation_programs ORDER BY id').fetchall()
    conn.close()
    
    result = "<h3>Program Rehabilitasi</h3><table style='width:100%; border-collapse: collapse;'>"
    result += "<tr><th style='border:1px solid #ddd; padding:8px;'>Program</th><th style='border:1px solid #ddd; padding:8px;'>Deskripsi</th><th style='border:1px solid #ddd; padding:8px;'>Jadwal</th></tr>"
    
    for program in programs:
        result += f"<tr><td style='border:1px solid #ddd; padding:8px;'>{program['program_name']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{program['description']}</td>"
        result += f"<td style='border:1px solid #ddd; padding:8px;'>{program['schedule']}</td></tr>"
    
    result += "</table>"
    return result

def get_relevant_context(question, intent=None, confidence=None):
    """Get relevant context from database with improved semantic matching"""
    # Validasi input bermakna terlebih dahulu
    if not is_meaningful_input(question):
        return ""
    
    # Jika intent belum ada, deteksi terlebih dahulu
    if intent is None or confidence is None:
        intent, confidence = detect_intent(question)

     # Intent-based contextual information dengan threshold yang konsisten
    CONFIDENCE_THRESHOLD = 0.7
    
    if intent == "jadwal_kunjungan" and confidence > CONFIDENCE_THRESHOLD:
        schedules = conn.execute('SELECT day, time, visitor_type FROM visiting_schedule').fetchall()
        context_parts.append("\nJadwal Kunjungan:")
        for schedule in schedules:
            context_parts.append(f"{schedule['day']}: {schedule['time']} ({schedule['visitor_type']})")
    
    elif intent == "persyaratan_kunjungan" and confidence > CONFIDENCE_THRESHOLD:
        requirements = conn.execute('SELECT title, description FROM requirements WHERE category = "kunjungan"').fetchall()
        context_parts.append("\nPersyaratan Kunjungan:")
        for req in requirements:
            context_parts.append(f"- {req['title']}: {req['description']}")
    
    elif intent == "layanan_kesehatan" and confidence > CONFIDENCE_THRESHOLD:
        services = conn.execute('SELECT service_name, schedule FROM health_services').fetchall()
        context_parts.append("\nLayanan Kesehatan:")
        for service in services:
            context_parts.append(f"- {service['service_name']}: {service['schedule']}")
    
    elif intent == "kontak_info" and confidence > CONFIDENCE_THRESHOLD:
        contacts = conn.execute('SELECT name, value FROM contacts').fetchall()
        context_parts.append("\nInformasi Kontak:")
        for contact in contacts:
            context_parts.append(f"- {contact['name']}: {contact['value']}")
    
    elif intent == "program_rehabilitasi" and confidence > CONFIDENCE_THRESHOLD:
        programs = conn.execute('SELECT program_name, schedule FROM rehabilitation_programs').fetchall()
        context_parts.append("\nProgram Rehabilitasi:")
        for program in programs:
            context_parts.append(f"- {program['program_name']}: {program['schedule']}")
    
    # Extract keywords with enhanced NLP
    keywords = extract_keywords(question)
    
    # Jika tidak ada keywords valid, return empty context
    if not keywords:
        return ""
    
    conn = get_db_connection()
    context_parts = []
    
    # Use keywords for better context matching
    if keywords:
        # Primary search: keyword matching in FAQ
        faq_contexts = []
        for keyword in keywords:
            # Skip keyword yang terlalu pendek
            if len(keyword) < 3:
                continue
                
            query = """
            SELECT question, answer FROM faq 
            WHERE keywords LIKE '%' || ? || '%' 
            OR question LIKE '%' || ? || '%'
            """
            results = conn.execute(query, (keyword, keyword)).fetchall()
            for result in results:
                faq_contexts.append((result['question'], result['answer']))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_faqs = []
        for q, a in faq_contexts:
            if q not in seen:
                seen.add(q)
                unique_faqs.append((q, a))
        
        # Add top 3 most relevant FAQs to context
        if unique_faqs:
            context_parts.append("FAQs yang relevan:")
            for q, a in unique_faqs[:3]:  # Limit to top 3 to keep context focused
                context_parts.append(f"Q: {q}\nA: {a}")
    
    conn.close()
    return "\n".join(context_parts)

def generate_meaningless_input_response():
    """Response untuk input yang tidak bermakna"""
    responses = [
        "Maaf, saya tidak mengerti maksud Anda. Silakan ajukan pertanyaan yang lebih jelas tentang Lapas 2 Ambarawa.",
        "Mohon berikan pertanyaan yang lebih spesifik. Saya dapat membantu dengan informasi jadwal kunjungan, persyaratan, layanan kesehatan, kontak, atau program rehabilitasi.",
        "Silakan tanyakan sesuatu yang lebih jelas. Misalnya 'Kapan jadwal kunjungan?' atau 'Apa syarat berkunjung?'",
        "Maaf, input Anda kurang jelas. Coba tanyakan tentang hal-hal terkait Lapas 2 Ambarawa yang ingin Anda ketahui."
    ]
    return secrets.choice(responses)

def extract_keywords(text):
    """Extract meaningful keywords from user text with improved validation"""
    if not is_meaningful_input(text):
        return []
    
    text = text.lower()
    
    # More comprehensive stopwords list in Indonesian
    stopwords = {
        'apa', 'yang', 'dengan', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 
        'adalah', 'ini', 'itu', 'atau', 'juga', 'saya', 'kamu', 'dia', 'mereka',
        'kami', 'kita', 'akan', 'sudah', 'telah', 'sedang', 'bisa', 'dapat',
        'boleh', 'harus', 'sebagai', 'oleh', 'tentang', 'bahwa', 'secara',
        'hal', 'jika', 'maka', 'tetapi', 'namun', 'tapi', 'sih', 'ya', 'iya',
        'dong', 'deh', 'loh', 'kok', 'gimana', 'bagaimana', 'kenapa', 'mengapa',
        'juga', 'sih', 'sama', 'ada', 'punya', 'mau', 'ingin', 'cari', 'tau', 'tahu'
    }
    
    # Extract meaningful words (longer than 2 chars, not in stopwords)
    words = re.findall(r'\w+', text)
    keywords = []
    
    for word in words:
        # Filter kata yang bermakna
        if (len(word) > 2 and 
            word not in stopwords and 
            not word.isdigit() and  # Bukan angka
            len(set(word)) > 1):    # Tidak semua huruf sama
            keywords.append(word)
    
    # Jika tidak ada keywords yang valid, return empty list
    if not keywords:
        return []
    
    # Add extra weight to important keywords
    important_keywords = {
        'jadwal': 'jadwal kunjungan waktu jam',
        'kunjungan': 'kunjungan jadwal besuk jenguk',
        'berkunjung': 'kunjungan jadwal besuk jenguk',
        'syarat': 'persyaratan dokumen ketentuan',
        'dokumen': 'persyaratan syarat ketentuan',
        'kesehatan': 'dokter obat sakit perawatan',
        'sakit': 'kesehatan dokter obat perawatan',
        'kontak': 'hubungi telepon alamat email',
        'program': 'pembinaan kegiatan rehabilitasi'
    }
    
    # Expand keywords with related terms
    expanded_keywords = keywords.copy()
    for word in keywords:
        if word in important_keywords:
            expanded_keywords.extend(important_keywords[word].split())
    
    # Remove duplicates and filter again
    unique_keywords = []
    seen = set()
    for keyword in expanded_keywords:
        if keyword not in seen and len(keyword) > 2:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords
    
def detect_intent(text):
    """Detect the intent of the user's message with improved input validation"""
    # Cek dulu apakah input bermakna
    if not is_meaningful_input(text):
        return "unknown", 0.0
    
    # Normalize text
    text = text.lower().strip()
    
    # Enhanced intent patterns with expanded keyword recognition
    intent_patterns = {
        "jadwal_kunjungan": [
            r"(jadwal|jam|waktu|kapan|bisa|boleh|hari|info).*(kunjung|besuk|jenguk|datang|bertemu|berkunjung)",
            r"(kunjung|besuk|jenguk|datang|bertemu|ketemu).*(jam|waktu|jadwal|kapan|bisa|boleh|hari)",
            r"(buka|tutup|bisa).*(kunjungan|besuk|jenguk)",
            r"(hari|waktu|jam).*(apa|kapan).*(kunjungan|besuk|jenguk)",
            r"(berkunjung|mengunjungi|menjenguk|bertemu|ketemu|datang).*(kapan|jam|hari|waktu)",
            r"(bisa|boleh|jadwal|kapan).*(ketemu|bertemu|jumpa|kunjung)"
        ],
        "persyaratan_kunjungan": [
            r"(syarat|persyarat|dokumen|bawa|perlu|butuh|perlukan|diperlukan).*(kunjung|besuk|jenguk|datang|bertemu)",
            r"(apa).*(syarat|persyarat|dokumen|bawa|perlu|butuh|perlukan).*(kunjung|besuk|jenguk)",
            r"(kunjung|besuk|jenguk).*(syarat|persyarat|dokumen|bawa|perlu|butuh)",
            r"(bawa|membawa|perlu|butuh).*(apa).*(kunjung|besuk|jenguk)",
            r"(identitas|ktp|kartu|dokumen|surat).*(kunjung|besuk|jenguk|bertemu)",
            r"(prosedur|proses|tata cara|cara).*(kunjung|besuk|jenguk|bertemu)",
            r"(ketentuan|aturan).*(kunjung|besuk|jenguk|bertemu)"
        ],
        "layanan_kesehatan": [
            r"(layanan|pelayanan|fasilitas).*(sehat|sakit|obat|dokter|medis|berobat|periksa)",
            r"(sakit|obat|dokter|klinik|medis|kesehatan|penyakit|perawatan|berobat|periksa)",
            r"(bagaimana|apa|kalau|jika|apabila).*(sakit|obat|kesehatan|rawat|periksa).*(tahanan|napi|narapidana|wbp)",
            r"(tahanan|napi|narapidana|wbp).*(sakit|obat|kesehatan|rawat|periksa)",
            r"(jadwal|jam|kapan).*(dokter|klinik|kesehatan|periksa|berobat)",
            r"(fasilitas|layanan).*(medis|kesehatan|dokter)"
        ],
        "kontak_info": [
            r"(kontak|hubung|telepon|telp|telpon|nomor|hp|email|alamat|lokasi|tempat|dimana)",
            r"(bagaimana|gimana|cara).*(hubung|kontak|telepon).*(petugas|lapas|penjara)",
            r"(nomor|telepon|telp|telpon|hp|email|alamat|whatsapp|wa).*(lapas|petugas|penjara)",
            r"(informasi|info).*(kontak|hubung|telepon|alamat)",
            r"(letak|lokasi|alamat|dimana).*(lapas|penjara)"
        ],
        "program_rehabilitasi": [
            r"(program|kegiatan|aktivitas|rehabilitasi|pembinaan|binaan)",
            r"(rehabilitasi|pembinaan|binaan|pelatihan|pendidikan|keterampilan).*(program|kegiatan|aktivitas)",
            r"(apa saja|apa|ada).*(program|kegiatan|aktivitas|rehabilitasi|pembinaan|binaan|pelatihan)",
            r"(kegiatan|aktivitas|program).*(tahanan|napi|narapidana|wbp)",
            r"(pelatihan|pendidikan|keterampilan|bakat|minat)",
            r"(bina|pembinaan|binaan).*(mental|spiritual|keagamaan|agama)"
        ]
    }
    
    # Advanced scoring logic with contextual awareness
    intent_scores = {}
    words = text.split()
    total_words = len(words)
    
    # Jika hanya ada 1 kata dan terlalu pendek, kembalikan unknown
    if total_words == 1 and len(text) < 3:
        return "unknown", 0.0
    
    # Cek apakah ada kata bermakna
    meaningful_words = [word for word in words if len(word) > 1]
    if not meaningful_words:
        return "unknown", 0.0
    
    for intent, patterns in intent_patterns.items():
        score = 0
        matched_words = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        matched_text = ''.join(item for item in match if item)
                    else:
                        matched_text = match
                        
                    matched_words.update(re.findall(r'\w+', matched_text))
                
                if re.search(pattern, text):
                    score += 0.3
                
                score += len(matches) * 0.25
        
        # Calculate word coverage
        if matched_words and total_words > 0:
            matched_word_ratio = len(matched_words) / total_words
            score += matched_word_ratio * 0.3
            
        # Handle special cases - direct questions untuk SEMUA intent
        if intent == "jadwal_kunjungan" and re.search(r"(jadwal|jam) (besuk|kunjungan)", text):
            score += 0.4
        elif intent == "persyaratan_kunjungan" and re.search(r"syarat (besuk|kunjungan)", text):
            score += 0.4
        elif intent == "layanan_kesehatan" and re.search(r"(layanan|dokter) (kesehatan|medis)", text):
            score += 0.4
        elif intent == "kontak_info" and re.search(r"(kontak|nomor|alamat) (lapas|petugas)", text):
            score += 0.4
        elif intent == "program_rehabilitasi" and re.search(r"(program|kegiatan) (rehabilitasi|pembinaan)", text):
            score += 0.4
        
        intent_scores[intent] = min(score, 1.0)
    
    # Find best intent match - ambil yang confidence tertinggi
    if not intent_scores or max(intent_scores.values()) == 0:
        return "unknown", 0.0
    
    best_intent = max(intent_scores.items(), key=lambda x: x[1])
    
    # Threshold minimum untuk menganggap intent valid
    if best_intent[1] < 0.2:  # Threshold minimum
        return "unknown", 0.0
    
    return best_intent[0], best_intent[1]

def detect_intent(text):
    """Detect the intent of the user's message with improved input validation"""
    # Cek dulu apakah input bermakna
    if not is_meaningful_input(text):
        return "unknown", 0.0
    
    # Normalize text
    text = text.lower().strip()
    
    
    # Enhanced intent patterns with expanded keyword recognition
    intent_patterns = {
        "jadwal_kunjungan": [
            r"(jadwal|jam|waktu|kapan|bisa|boleh|hari|info).*(kunjung|besuk|jenguk|datang|bertemu|berkunjung)",
            r"(kunjung|besuk|jenguk|datang|bertemu|ketemu).*(jam|waktu|jadwal|kapan|bisa|boleh|hari)",
            r"(buka|tutup|bisa).*(kunjungan|besuk|jenguk)",
            r"(hari|waktu|jam).*(apa|kapan).*(kunjungan|besuk|jenguk)",
            r"(berkunjung|mengunjungi|menjenguk|bertemu|ketemu|datang).*(kapan|jam|hari|waktu)",
            r"(bisa|boleh|jadwal|kapan).*(ketemu|bertemu|jumpa|kunjung)"
        ],
        "persyaratan_kunjungan": [
            r"(syarat|persyarat|dokumen|bawa|perlu|butuh|perlukan|diperlukan).*(kunjung|besuk|jenguk|datang|bertemu)",
            r"(apa).*(syarat|persyarat|dokumen|bawa|perlu|butuh|perlukan).*(kunjung|besuk|jenguk)",
            r"(kunjung|besuk|jenguk).*(syarat|persyarat|dokumen|bawa|perlu|butuh)",
            r"(bawa|membawa|perlu|butuh).*(apa).*(kunjung|besuk|jenguk)",
            r"(identitas|ktp|kartu|dokumen|surat).*(kunjung|besuk|jenguk|bertemu)",
            r"(prosedur|proses|tata cara|cara).*(kunjung|besuk|jenguk|bertemu)",
            r"(ketentuan|aturan).*(kunjung|besuk|jenguk|bertemu)"
        ],
        "layanan_kesehatan": [
            r"(layanan|pelayanan|fasilitas).*(sehat|sakit|obat|dokter|medis|berobat|periksa)",
            r"(sakit|obat|dokter|klinik|medis|kesehatan|penyakit|perawatan|berobat|periksa)",
            r"(bagaimana|apa|kalau|jika|apabila).*(sakit|obat|kesehatan|rawat|periksa).*(tahanan|napi|narapidana|wbp)",
            r"(tahanan|napi|narapidana|wbp).*(sakit|obat|kesehatan|rawat|periksa)",
            r"(jadwal|jam|kapan).*(dokter|klinik|kesehatan|periksa|berobat)",
            r"(fasilitas|layanan).*(medis|kesehatan|dokter)"
        ],
        "kontak_info": [
            r"(kontak|hubung|telepon|telp|telpon|nomor|hp|email|alamat|lokasi|tempat|dimana)",
            r"(bagaimana|gimana|cara).*(hubung|kontak|telepon).*(petugas|lapas|penjara)",
            r"(nomor|telepon|telp|telpon|hp|email|alamat|whatsapp|wa).*(lapas|petugas|penjara)",
            r"(informasi|info).*(kontak|hubung|telepon|alamat)",
            r"(letak|lokasi|alamat|dimana).*(lapas|penjara)"
        ],
        "program_rehabilitasi": [
            r"(program|kegiatan|aktivitas|rehabilitasi|pembinaan|binaan)",
            r"(rehabilitasi|pembinaan|binaan|pelatihan|pendidikan|keterampilan).*(program|kegiatan|aktivitas)",
            r"(apa saja|apa|ada).*(program|kegiatan|aktivitas|rehabilitasi|pembinaan|binaan|pelatihan)",
            r"(kegiatan|aktivitas|program).*(tahanan|napi|narapidana|wbp)",
            r"(pelatihan|pendidikan|keterampilan|bakat|minat)",
            r"(bina|pembinaan|binaan).*(mental|spiritual|keagamaan|agama)"
        ]
    }
    
    # Advanced scoring logic with contextual awareness
    intent_scores = {}
    words = text.split()
    total_words = len(words)
    
    # Jika hanya ada 1 kata dan terlalu pendek, kembalikan unknown
    if total_words == 1 and len(text) < 3:
        return "unknown", 0.0
    
    # Cek apakah ada kata bermakna
    meaningful_words = [word for word in words if len(word) > 1]
    if not meaningful_words:
        return "unknown", 0.0
    
    for intent, patterns in intent_patterns.items():
        score = 0
        matched_words = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        matched_text = ''.join(item for item in match if item)
                    else:
                        matched_text = match
                        
                    matched_words.update(re.findall(r'\w+', matched_text))
                
                if re.search(pattern, text):
                    score += 0.3
                
                score += len(matches) * 0.25
        
        # Calculate word coverage
        if matched_words and total_words > 0:
            matched_word_ratio = len(matched_words) / total_words
            score += matched_word_ratio * 0.3
            
        # Handle special cases - direct questions untuk SEMUA intent
        if intent == "jadwal_kunjungan" and re.search(r"(jadwal|jam) (besuk|kunjungan)", text):
            score += 0.4
        elif intent == "persyaratan_kunjungan" and re.search(r"syarat (besuk|kunjungan)", text):
            score += 0.4
        elif intent == "layanan_kesehatan" and re.search(r"(layanan|dokter) (kesehatan|medis)", text):
            score += 0.4
        elif intent == "kontak_info" and re.search(r"(kontak|nomor|alamat) (lapas|petugas)", text):
            score += 0.4
        elif intent == "program_rehabilitasi" and re.search(r"(program|kegiatan) (rehabilitasi|pembinaan)", text):
            score += 0.4
        
        intent_scores[intent] = min(score, 1.0)
    
    # Find best intent match - ambil yang confidence tertinggi
    if not intent_scores or max(intent_scores.values()) == 0:
        return "unknown", 0.0
    
    best_intent = max(intent_scores.items(), key=lambda x: x[1])
    
    # Threshold minimum untuk menganggap intent valid
    if best_intent[1] < 0.2:  # Threshold minimum
        return "unknown", 0.0
    
    return best_intent[0], best_intent[1]

def is_thank_you(text):
    """Enhanced detection of gratitude expressions with context awareness"""
    # Validasi input bermakna terlebih dahulu
    if not is_meaningful_input(text):
        return False
        
    # Normalize text
    text = text.lower().strip()
    
    # Comprehensive patterns for thank you detection with Indonesian language variants
    thank_you_patterns = [
        r"\b(terima\s*kasih|makasih|mksh|thx|thank|thanks|tq|trims|terimakasih|trim|makasi|makaci)\b",
        r"\b(bagus|keren|mantap|mantab|hebat|baik|membantu|berguna)\b",
        r"\b(ok|oke|okay|sip|sippp|bagus|nice|good|great)\b",
        r"(👍|👌|🙏|❤️|😊)",  # Emoji support
        r"\b(thx|tq|ty|tks)\b",  # Common abbreviations
        r"\b(membantu|memecahkan|menjawab|membantu sekali)\b",
        r"\b(sangat membantu|sangat berguna)\b"
    ]
    
    # Rule-based negation detection
    negation_patterns = [
        r"\b(tidak|kurang|belum|bukan|ga|gak|nggak|ngga|enggak)\b"
    ]
    
    # Check for pattern matches with negation awareness
    for pattern in thank_you_patterns:
        if re.search(pattern, text):
            # Check if this is negated
            for neg_pattern in negation_patterns:
                neg_match = re.search(neg_pattern + r".*" + pattern, text)
                if neg_match and (neg_match.start() < re.search(pattern, text).start()):
                    return False
            
            return True
    
    return False

def handle_thank_you():
    """Enhanced gratitude response with personalization and variety"""
    # Add more natural and conversational responses
    responses = [
        "Sama-sama! Senang bisa membantu Anda.",
        "Dengan senang hati! Ada yang bisa saya bantu lagi?",
        "Terima kasih kembali. Jika ada pertanyaan lain, silakan tanyakan.",
        "Sama-sama. Semoga informasi yang diberikan bermanfaat.",
        "Senang bisa membantu! Ada hal lain yang ingin ditanyakan?",
        "Terima kasih telah menggunakan layanan chatbot Lapas 2 Ambarawa. Jangan ragu untuk bertanya lagi jika membutuhkan informasi lainnya.",
        "Tidak masalah, itulah gunanya saya ada di sini untuk membantu Anda mendapatkan informasi yang Anda butuhkan.",
        "Senang mendengarnya! Jangan ragu untuk kembali kapan saja jika membutuhkan informasi lainnya.",
        "Sama-sama! Semoga harimu menyenangkan.",
        "Senang bisa memberikan informasi yang Anda butuhkan!",
        "Terima kasih kembali. Selalu siap membantu kapan saja Anda membutuhkan informasi tentang Lapas 2 Ambarawa."
    ]
    return secrets.choice(responses)

def is_greeting(text):
    """Enhanced greeting detection with more pattern variations"""
    # Validasi input bermakna terlebih dahulu
    if not is_meaningful_input(text):
        return False
        
    # Normalize
    text = text.lower().strip()
    
    # Expanded greeting patterns with Indonesian variations
    greeting_patterns = [
        r"^(halo|hai|hi|hello|hey|hei|hay|haii|helo|hallo|selamat\s*pagi|selamat\s*siang|selamat\s*sore|selamat\s*malam)(\s|$|\.|\?)",
        r"^(pagi|siang|sore|malam|pgi|mlm)(\s|$|\.|\?)",
        r"^(assalamualaikum|assalamu'alaikum|asalamualaikum|salam|shalom)(\s|$|\.|\?)",
        r"^(permisi|maaf|excuse me|bisa\s*bantu)(\s|$|\.|\?)",
        r"^(p|test|testing|tes|ping|cek|check)(\s|$|\.|\?)"
    ]
    
    for pattern in greeting_patterns:
        if re.search(pattern, text):
            return True
    return False

def handle_greeting():
    """Enhanced greeting response with time awareness and personalization"""
    current_hour = datetime.datetime.now().hour
    
    if 5 <= current_hour < 12:
        time_greeting = "pagi"
    elif 12 <= current_hour < 15:
        time_greeting = "siang"
    elif 15 <= current_hour < 19:
        time_greeting = "sore"
    else:
        time_greeting = "malam"
    
    # More varied and natural greeting responses
    responses = [
        f"Selamat {time_greeting}! Ada yang bisa saya bantu terkait informasi Lapas 2 Ambarawa?",
        f"Halo, selamat {time_greeting}. Saya chatbot Lapas 2 Ambarawa, siap membantu Anda dengan informasi seputar lembaga pemasyarakatan kami.",
        f"Hai! Selamat {time_greeting}. Apa yang ingin Anda ketahui tentang Lapas 2 Ambarawa?",
        f"Selamat {time_greeting}! Saya di sini untuk menjawab pertanyaan seputar Lapas 2 Ambarawa seperti jadwal kunjungan, persyaratan, atau informasi lainnya.",
        f"Halo! Selamat {time_greeting}. Butuh informasi apa tentang Lapas 2 Ambarawa?",
        f"Hi, selamat {time_greeting}! Saya siap membantu dengan informasi seputar Lapas 2 Ambarawa."
    ]
    return secrets.choice(responses)

def is_goodbye(text):
    """Check if the message is a goodbye with input validation"""
    # Validasi input bermakna terlebih dahulu
    if not is_meaningful_input(text):
        return False
        
    # Normalize text
    text = text.lower().strip()
    
    goodbye_patterns = [
        r"(selamat\s*tinggal|bye|goodbye|sampai\s*jumpa|sampai\s*ketemu\s*lagi)",
        r"^(sudah|cukup|selesai)(\s|$)"
    ]
    
    for pattern in goodbye_patterns:
        if re.search(pattern, text):
            return True
    return False

def handle_goodbye():
    """Handle goodbye messages"""
    responses = [
        "Sampai jumpa kembali! Semoga harimu menyenangkan.",
        "Terima kasih telah menggunakan layanan chatbot Lapas 2 Ambarawa. Sampai jumpa!",
        "Sampai jumpa! Jika ada pertanyaan lain, silakan hubungi kembali.",
    ]
    return secrets.choice(responses)

def generate_default_response():
    """Enhanced default response with more helpful guidance"""
    responses = [
        """
        <p>Terima kasih atas pertanyaan Anda. Saya chatbot Lapas 2 Ambarawa yang dapat membantu dengan informasi tentang:</p>
        <ul style="margin-top: 10px; margin-left: 20px;">
            <li>Jadwal kunjungan (hari dan jam besuk)</li>
            <li>Persyaratan kunjungan (dokumen dan prosedur)</li>
            <li>Layanan kesehatan untuk narapidana</li>
            <li>Kontak dan lokasi Lapas</li>
            <li>Program rehabilitasi dan pembinaan</li>
        </ul>
        <p style="margin-top: 10px;">Silakan tanyakan lebih spesifik tentang topik-topik tersebut.</p>
        """,
        
        """
        <p>Saya siap membantu Anda dengan informasi seputar Lapas 2 Ambarawa. Beberapa hal yang bisa saya jelaskan:</p>
        <ul style="margin-top: 10px; margin-left: 20px;">
            <li>Kapan jadwal kunjungan (jam besuk)</li>
            <li>Apa saja syarat untuk berkunjung</li>
            <li>Informasi tentang layanan kesehatan</li>
            <li>Bagaimana cara menghubungi pihak Lapas</li>
            <li>Program pembinaan yang tersedia</li>
        </ul>
        <p style="margin-top: 10px;">Coba tanyakan misalnya "Apa saja jadwal kunjungan?" atau "Syarat apa saja untuk berkunjung?"</p>
        """
    ]
    return secrets.choice(responses)

# Route handlers
@app.route('/')
def home():
    return render_template('index.html', vapid_public_key=os.getenv('PUBLIC_VAPID_KEY'))  # Halaman utama chatbot

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact-it', methods=['GET'])
def contact_it():
    return render_template('contact_it.html')

@app.route('/service-worker.js')
def sw():
    # Pastikan service-worker.js ada di folder static
    return send_from_directory(app.static_folder, 'service-worker.js')

@app.route('/favicon.ico')
def favicon():
    # Mengembalikan favicon.ico dengan MIME type yang tepat
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/admin/send_notification', methods=['POST'])
def admin_send_notification():
    # Validasi autentikasi admin
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    # Ambil dan validasi payload
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    body = data.get('body', '').strip()
    url = data.get('url', '/').strip()

    if not title or not body:
        return jsonify({'error': 'Title dan body wajib diisi'}), 400

    payload = {'title': title, 'body': body, 'url': url}
    
    # Ambil semua token dari database
    conn = get_db_connection()
    rows = conn.execute('SELECT id, token FROM device_tokens').fetchall()
    
    sent_count = 0
    expired_tokens = []
    
    # Kirim notifikasi ke setiap device
    for row in rows:
        try:
            subscription_info = json.loads(row['token'])
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            sent_count += 1
            
        except WebPushException as ex:
            # Tangani token yang expired atau invalid
            status = getattr(ex.response, 'status_code', None) if hasattr(ex, 'response') else None
            
            if status in (404, 410) or 'expired' in str(ex).lower():
                expired_tokens.append(row['id'])
            else:
                print(f"[SendNotif] Error for device {row['id']}: {str(ex)[:100]}")
    
    # Hapus token yang expired dalam satu operasi
    if expired_tokens:
        conn.execute('DELETE FROM device_tokens WHERE id IN ({})'.format(
            ','.join('?' * len(expired_tokens))
        ), expired_tokens)
        conn.commit()
        print(f"[SendNotif] Removed {len(expired_tokens)} expired tokens")
    
    conn.close()
    
    return jsonify({'sent_to': sent_count})

@app.route('/admin/reset-password', methods=['GET'])
def admin_reset_password():
    return render_template('reset_password.html')

@app.route('/api/v1/reset-password', methods=['POST'])
def api_reset_password():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify(success=False, message="Email wajib diisi"), 400

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify(success=False, message="Email tidak terdaftar di database"), 404

    # Buat token unik dan simpan di DB
    token = secrets.token_urlsafe(32)
    cursor.execute("UPDATE users SET token = ? WHERE id = ?", (token, user['id']))
    conn.commit()
    conn.close()

    # Kirim email dengan link reset (gunakan Flask-Mail, smtplib, dsb.)
    reset_link = url_for('admin_reset_with_token', token=token, _external=True)
    send_reset_email(to=email, link=reset_link)

    return jsonify(success=True, message="Link reset password telah dikirim ke email Anda")

@app.route('/admin/reset-password/<token>', methods=['GET', 'POST'])
def admin_reset_with_token(token):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE token = ?", (token,))
    user = c.fetchone()

    if request.method == 'GET':
        if not user:
            # Token tidak valid untuk GET request - redirect ke login
            conn.close()
            flash("Token tidak valid atau sudah digunakan.", "info")
            return redirect(url_for('admin_login'))
        
        # Token valid, tampilkan form
        conn.close()
        return render_template('set_new_password.html', token=token)

    # POST request
    if not user:
        conn.close()
        if request.is_json:
            return jsonify({"error": "Token tidak valid atau sudah kadaluwarsa."}), 400
        else:
            flash("Token tidak valid atau sudah kadaluwarsa.", "danger")
            return redirect(url_for('admin_login'))

    # Handle JSON request
    if request.is_json:
        data = request.get_json()
        new_pass = data.get('password', '').strip()
    else:
        new_pass = request.form.get('password', '').strip()
    
    if len(new_pass) < 6:
        if request.is_json:
            return jsonify({"error": "Password minimal 6 karakter."}), 400
        else:
            flash("Password minimal 6 karakter.", "warning")
            return render_template('set_new_password.html', token=token)

    pw_hash = generate_password_hash(new_pass)
    c.execute(
        "UPDATE users SET password_hash = ?, token = NULL WHERE id = ?",
        (pw_hash, user['id'])
    )
    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({"message": "Password berhasil diubah. Silakan login.", "redirect": "/admin/login"}), 200
    else:
        flash("Password berhasil diubah. Silakan login.", "success")
        return redirect(url_for('admin_login'))

@app.route('/api/v1/validate-reset-token', methods=['POST'])
def api_validate_reset_token():
    data = request.json
    token = data.get('token')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
    conn.close()
    
    if user:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False}), 400

# Tambahkan decorator pada endpoint API
@app.route('/api/ask', methods=['POST'])
@limiter.limit("15 per minute")
def api_ask():
    """API endpoint for mobile app chat queries"""
    data = request.json
    question = data.get('question', '')
    session_id = data.get('session_id', secrets.token_hex(8))
    
    # Process the question
    answer, source = process_question(question)
    
    # Log the conversation
    log_conversation(question, answer, request.remote_addr, session_id, source)
    
    return jsonify({
        "answer": answer,
        "source": source,
        "session_id": session_id
    })

@app.route('/api/v1/chat/session', methods=['POST'])
def mobile_chat_session():
    """Enhanced mobile chat API with session management and better response structure"""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request', 'message': 'Message content required'}), 400
    
    # Extract data with defaults for flexible mobile usage
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', secrets.token_hex(8))
    
    # Empty message guard
    if not user_message:
        return jsonify({
            'success': False,
            'error': 'Empty message',
            'session_id': session_id
        }), 400
    
    # Process user message
    response, source = process_question(user_message)
    
    # Enhance response with metadata for mobile display
    is_greeting_msg = is_greeting(user_message)
    is_thank_you_msg = is_thank_you(user_message)
    is_goodbye_msg = is_goodbye(user_message)
    
    # Get intent for UI enhancements
    intent, confidence = detect_intent(user_message)
    
    # Log conversation with enhanced metadata
    log_conversation(user_message, response, request.remote_addr, session_id, source)
    
    # Structure response in mobile-friendly JSON
    return jsonify({
        'success': True,
        'response': {
            'message': response,
            'source': source,
            'timestamp': datetime.datetime.now().isoformat(),
            'metadata': {
                'intent': intent if confidence > 0.6 else 'general',
                'is_greeting': is_greeting_msg,
                'is_gratitude': is_thank_you_msg,
                'is_goodbye': is_goodbye_msg,
                'has_links': '<a href' in response,
                'has_table': '<table' in response
            }
        },
        'session_id': session_id
    })
@app.route('/api/v1/chat', methods=['POST'])
def mobile_chat_api():
    """API endpoint for mobile chat app"""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    question = data.get('message', '')
    session_id = data.get('session_id', secrets.token_hex(8))
    
    # Process the question
    answer, source = process_question(question)
    
    # Log the conversation
    log_conversation(question, answer, request.remote_addr, session_id, source)
    
    # Format output for mobile
    return jsonify({
        "success": True,
        "response": {
            "message": answer,
            "source": source,
            "timestamp": datetime.datetime.now().isoformat()
        },
        "session_id": session_id
    })

@app.route('/api/admin/chat_analytics', methods=['GET'])
def api_admin_chat_analytics():
    """API endpoint to get chat analytics for admin panel"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    
    # Get total chat count
    total_chats = conn.execute('SELECT COUNT(*) as count FROM chat_history').fetchone()['count']
    
    # Get chats per day (last 7 days)
    date_counts = conn.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count 
        FROM chat_history 
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date ASC
    ''').fetchall()
    
    # Get most common questions (top 5)
    common_questions = conn.execute('''
        SELECT user_message, COUNT(*) as count 
        FROM chat_history 
        GROUP BY user_message
        ORDER BY count DESC
        LIMIT 5
    ''').fetchall()
    
    # Get source distribution
    source_dist = conn.execute('''
        SELECT response_quality AS response, COUNT(*) AS count
        FROM chat_history
        GROUP BY response_quality
        ORDER BY count DESC
    ''').fetchall()
    
    conn.close()
    
    # Format results
    date_result = [{'date': item['date'], 'count': item['count']} for item in date_counts]
    questions_result = [{'message': item['user_message'], 'count': item['count']} for item in common_questions]
    
    # Tambahkan ke respons JSON
    return jsonify({
        'total_chats': total_chats,
        'chats_by_date': date_result,
        'common_questions': questions_result,
        'source_distribution': [{'response': item['response'], 'count': item['count']} for item in source_dist]
    })

@app.route('/api/admin/chat_metrics', methods=['GET'])
def api_admin_chat_metrics():
    if not check_admin_auth():
        return jsonify({'error':'Unauthorized'}), 401
    conn = get_db_connection()
    rows = conn.execute('SELECT date, total_chats, ai_responses, successful_responses, failed_responses FROM chat_metrics ORDER BY date DESC').fetchall()
    conn.close()
    data = [dict(r) for r in rows]
    return jsonify({'data': data})

@app.route('/api/admin/chat_metrics_summary', methods=['GET'])
def api_chat_metrics_summary():
    # pastikan Anda sudah mengecek autentikasi admin di sini
    conn = get_db_connection()
    row = conn.execute(
        'SELECT total_chats, successful_responses, ai_responses, failed_responses '
        'FROM chat_metrics '
        'ORDER BY date DESC LIMIT 1'
    ).fetchone()
    conn.close()

    if row is None:
        # jika belum ada data, kembalikan nol semua
        result = {
            'total_chats': 0,
            'successful_responses': 0,
            'ai_responses': 0,
            'failed_responses': 0
        }
    else:
        result = {
            'total_chats': row['total_chats'],
            'successful_responses': row['successful_responses'],
            'ai_responses': row['ai_responses'],
            'failed_responses': row['failed_responses']
        }
    return jsonify(result)


# Untuk CORS yang lebih spesifik
@app.after_request
def add_cors_headers(response):
    """Add CORS headers for mobile app"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Endpoint untuk push notification
@app.route('/api/v1/register_device', methods=['POST'])
def register_device():
    """Register mobile device for push notifications"""
    data = request.json
    if not data or 'device_token' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    device_token = data.get('device_token')
    platform = data.get('platform', 'android')  # default to android
    
    conn = get_db_connection()
    
    # Check if token exists
    existing = conn.execute('SELECT id FROM device_tokens WHERE token = ?', 
                           (device_token,)).fetchone()
    
    if existing:
        conn.execute('UPDATE device_tokens SET last_seen = CURRENT_TIMESTAMP WHERE token = ?',
                    (device_token,))
    else:
        conn.execute('INSERT INTO device_tokens (token, platform) VALUES (?, ?)',
                    (device_token, platform))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/v1/unregister_device', methods=['POST'])
def unregister_device():
    """Unregister mobile device from push notifications"""
    data = request.json
    if not data or 'device_token' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    device_token = data.get('device_token')
    platform = data.get('platform', 'android')  # default to android

    conn = get_db_connection()
    
    try:
        # Check if token exists
        existing = conn.execute('SELECT id FROM device_tokens WHERE token = ?', 
                               (device_token,)).fetchone()
        
        if not existing:
            return jsonify({'error': 'Device token not found'}), 404
        
        # Delete the device token
        conn.execute('DELETE FROM device_tokens WHERE token = ?', (device_token,))
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Device unregistered successfully'})
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Failed to unregister device'}), 500
        
    finally:
        conn.close()

def update_chat_metrics(source, is_successful=True):
    """
    Update tabel chat_metrics dengan data chat baru
    
    Args:
        source (str): Sumber response ('ai', 'database', 'default')
        is_successful (bool): Apakah response berhasil atau tidak
    """
    conn = get_db_connection()
    today = datetime.datetime.now().date()
    
    try:
        # Cek apakah sudah ada record untuk hari ini
        existing = conn.execute(
            'SELECT * FROM chat_metrics WHERE date = ?', 
            (today,)
        ).fetchone()
        
        if existing:
            # Update record yang sudah ada
            total_chats = existing['total_chats'] + 1
            ai_responses = existing['ai_responses'] + (1 if source == 'ai' else 0)
            successful_responses = existing['successful_responses'] + (1 if is_successful else 0)
            failed_responses = existing['failed_responses'] + (0 if is_successful else 1)
            
            conn.execute('''
                UPDATE chat_metrics 
                SET total_chats = ?, ai_responses = ?, successful_responses = ?, failed_responses = ?
                WHERE date = ?
            ''', (total_chats, ai_responses, successful_responses, failed_responses, today))
        else:
            # Buat record baru untuk hari ini
            ai_responses = 1 if source == 'ai' else 0
            successful_responses = 1 if is_successful else 0
            failed_responses = 0 if is_successful else 1
            
            conn.execute('''
                INSERT INTO chat_metrics (date, total_chats, ai_responses, successful_responses, failed_responses)
                VALUES (?, 1, ?, ?, ?)
            ''', (today, ai_responses, successful_responses, failed_responses))
        
        conn.commit()
    except Exception as e:
        print(f"Error updating chat metrics: {e}")
    finally:
        conn.close()

def log_conversation(question, answer, ip_address, session_id, source="database"):
    """Log each conversation to the database"""
    conn = get_db_connection()
    if source == 'default':
        quality = 'default'
    elif source == 'ai':
        quality = 'ai'
    elif source == 'database':
        quality = 'database'
    elif source == 'meaningless':
        quality = 'meaningless'
    elif source == 'fallback':
        quality = 'fallback'
    else:
        quality = 'unknown'
    conn.execute(
        'INSERT INTO chat_history (user_message, bot_response, ip_address, session_id, response_quality) VALUES (?, ?, ?, ?, ?)',
        (question, answer, ip_address, session_id, quality)
    )
    conn.commit()
    conn.close()
    # Tentukan apakah response berhasil atau tidak
    is_successful = answer and answer.strip() != "" and answer != generate_default_response()
    
    # Update chat metrics
    update_chat_metrics(source, is_successful)

def _render_error(msg):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': False, 'error': msg})
    return render_template('admin_login.html', error=msg)

@app.route('/admin')
def admin_home():
    return redirect(url_for('admin_login'))

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        # 1) Username tidak ditemukan
        if not user:
            conn.close()
            return _render_error("Username tidak ditemukan.")

        # 2) Cek lockout
        now = datetime.datetime.utcnow()
        locked_until = user['locked_until']
        if locked_until:
            locked_dt = datetime.datetime.fromisoformat(locked_until)
            if now < locked_dt:
                remaining = (locked_dt - now).seconds
                minutes = remaining // 60 or 1
                conn.close()
                return _render_error(f"Akun terkunci. Coba lagi dalam {minutes} menit.")

        # 3) Validasi password
        if check_password_hash(user['password_hash'], password):
            # Reset counter & lock
            conn.execute(
                "UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE username = ?",
                (username,)
            )
            conn.commit()
            conn.close()

            # --- Lanjutkan sesi sukses ---
            session['admin_logged_in'] = True
            session['username'] = username
            session['role'] = user['role']  # misal: 'admin'
            # Bila login via AJAX, kirim success JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
            # Bila normal form submit, redirect ke dashboard
            return redirect(url_for('admin_dashboard'))

        # 4) Password salah → increment & atur lockout
        attempts = user['failed_attempts'] + 1
        lock_until = None

        if attempts >= 10:
            # kunci permanen
            lock_until = (now + datetime.timedelta(days=365*100)).isoformat()
        elif attempts >= 4:
            # kunci 1 menit setelah 5 kali salah
            lock_until = (now + datetime.timedelta(minutes=1)).isoformat()

        conn.execute(
            "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE username = ?",
            (attempts, lock_until, username)
        )
        conn.commit()
        conn.close()

        # Buat pesan error sesuai sisa percobaan
        if attempts < 10:
            remaining = 10 - attempts
            msg = f"Password salah. Sisa {remaining} percobaan."
        else:
            msg = "Akun dikunci permanen. Silakan reset password melalui link Lupa Password."

        return _render_error(msg)

    # GET request → tampilkan halaman login
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', username=session.get('username'))

@app.route('/admin/profile')
def admin_profile():
    return render_template('profile.html')

def check_admin_auth():
    """Helper function to verify admin authentication consistently"""
    # Check session first (for web interface)
    if session.get('admin_logged_in'):
        return True
    
    # Check Authorization header (for API)
    token = request.headers.get('Authorization')
    # Periksa token dengan format Bearer
    if token:
        # Hapus prefix 'Bearer ' jika ada
        if token.startswith('Bearer '):
            token = token[7:]
        if validate_token(token):
            return True
        
    return False

@app.route('/api/admin/chat_history', methods=['GET'])
def api_admin_chat_history():
    """API endpoint to get chat history for admin panel"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    conn = get_db_connection()
    history = conn.execute(
        'SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ? OFFSET ?', 
        (limit, offset)
    ).fetchall()
    
    # Count total records for pagination
    total = conn.execute('SELECT COUNT(*) as count FROM chat_history').fetchone()['count']
    
    conn.close()
    
    result = []
    for item in history:
        result.append({
            "id": item['id'],
            "user_message": item['user_message'],
            "bot_response": item['bot_response'],
            'response_quality': item['response_quality'],
            "timestamp": item['timestamp'],
            "session_id": item['session_id']
        })
    
    return jsonify({
        "data": result,
        "total": total,
        "limit": limit,
        "offset": offset
    })
    

# FAQ Routes - RESTful pattern
@app.route('/api/admin/faq', methods=['GET'])
def api_admin_faq_get():
    """API endpoint to get all FAQs for admin panel"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    faqs = conn.execute('SELECT * FROM faq ORDER BY id').fetchall()
    conn.close()
    
    result = []
    for faq in faqs:
        result.append({
            "id": faq['id'],
            "question": faq['question'],
            "answer": faq['answer'],
            "category": faq['category'],
            "keywords": faq['keywords']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/faq', methods=['POST'])
def api_admin_faq_post():
    """API endpoint to create new FAQ"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['question', 'answer', 'category', 'keywords']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO faq (question, answer, category, keywords) VALUES (?, ?, ?, ?)',
        (data['question'], data['answer'], data['category'], data['keywords'])
    )
    faq_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': faq_id, 'success': True})

@app.route('/api/admin/faq/<int:faq_id>', methods=['GET'])
def api_admin_faq_get_one(faq_id):
    """API endpoint to get a specific FAQ"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    faq = conn.execute('SELECT * FROM faq WHERE id = ?', (faq_id,)).fetchone()
    conn.close()
    
    if not faq:
        return jsonify({'error': 'FAQ not found'}), 404
    
    result = {
        "id": faq['id'],
        "question": faq['question'],
        "answer": faq['answer'],
        "category": faq['category'],
        "keywords": faq['keywords']
    }
    
    return jsonify(result)

@app.route('/api/admin/faq/<int:faq_id>', methods=['PUT'])
def api_admin_faq_put(faq_id):
    """API endpoint to update a FAQ"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['question', 'answer', 'category', 'keywords']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE faq SET question = ?, answer = ?, category = ?, keywords = ? WHERE id = ?',
        (data['question'], data['answer'], data['category'], data['keywords'], faq_id)
    )
    conn.commit()
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'FAQ not found'}), 404
    
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/faq/<int:faq_id>', methods=['DELETE'])
def api_admin_faq_delete(faq_id):
    """API endpoint to delete a FAQ"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faq WHERE id = ?', (faq_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'FAQ not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Visiting Schedule Routes - RESTful pattern
@app.route('/api/admin/schedules', methods=['GET'])
def api_admin_schedules_get():
    """API endpoint to get all visiting schedules"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    schedules = conn.execute('SELECT * FROM visiting_schedule ORDER BY CASE day WHEN "Senin" THEN 1 WHEN "Selasa" THEN 2 WHEN "Rabu" THEN 3 WHEN "Kamis" THEN 4 WHEN "Jumat" THEN 5 WHEN "Sabtu" THEN 6 WHEN "Minggu" THEN 7 END').fetchall()
    conn.close()
    
    result = []
    for schedule in schedules:
        result.append({
            "id": schedule['id'],
            "day": schedule['day'],
            "time": schedule['time'],
            "visitor_type": schedule['visitor_type'],
            "notes": schedule['notes']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/schedules', methods=['POST'])
def api_admin_schedules_post():
    """API endpoint to create new visiting schedule"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['day', 'time', 'visitor_type']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO visiting_schedule (day, time, visitor_type, notes) VALUES (?, ?, ?, ?)',
        (data['day'], data['time'], data['visitor_type'], data.get('notes', ''))
    )
    schedule_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': schedule_id, 'success': True})

@app.route('/api/admin/schedules/<int:schedule_id>', methods=['GET'])
def api_admin_schedules_get_one(schedule_id):
    """API endpoint to get a specific visiting schedule"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM visiting_schedule WHERE id = ?', (schedule_id,)).fetchone()
    conn.close()
    
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404
    
    result = {
        "id": schedule['id'],
        "day": schedule['day'],
        "time": schedule['time'],
        "visitor_type": schedule['visitor_type'],
        "notes": schedule['notes']
    }
    
    return jsonify(result)

@app.route('/api/admin/schedules/<int:schedule_id>', methods=['PUT'])
def api_admin_schedules_put(schedule_id):
    """API endpoint to update a visiting schedule"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['day', 'time', 'visitor_type']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE visiting_schedule SET day = ?, time = ?, visitor_type = ?, notes = ? WHERE id = ?',
        (data['day'], data['time'], data['visitor_type'], data.get('notes', ''), schedule_id)
    )
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Schedule not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/schedules/<int:schedule_id>', methods=['DELETE'])
def api_admin_schedules_delete(schedule_id):
    """API endpoint to delete a visiting schedule"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM visiting_schedule WHERE id = ?', (schedule_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Schedule not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Requirements Routes - RESTful pattern
@app.route('/api/admin/requirements', methods=['GET'])
def api_admin_requirements_get():
    """API endpoint to get all visiting requirements"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    requirements = conn.execute('SELECT * FROM requirements ORDER BY id').fetchall()
    conn.close()
    
    result = []
    for req in requirements:
        result.append({
            "id": req['id'],
            "title": req['title'],
            "description": req['description'],
            "category": req['category']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/requirements', methods=['POST'])
def api_admin_requirements_post():
    """API endpoint to create new requirement"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['title', 'description', 'category']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO requirements (title, description, category) VALUES (?, ?, ?)',
        (data['title'], data['description'], data['category'])
    )
    req_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': req_id, 'success': True})

@app.route('/api/admin/requirements/<int:req_id>', methods=['GET'])
def api_admin_requirements_get_one(req_id):
    """API endpoint to get a specific requirement"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    req = conn.execute('SELECT * FROM requirements WHERE id = ?', (req_id,)).fetchone()
    conn.close()
    
    if not req:
        return jsonify({'error': 'Requirement not found'}), 404
    
    result = {
        "id": req['id'],
        "title": req['title'],
        "description": req['description'],
        "category": req['category']
    }
    
    return jsonify(result)

@app.route('/api/admin/requirements/<int:req_id>', methods=['PUT'])
def api_admin_requirements_put(req_id):
    """API endpoint to update a requirement"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['title', 'description', 'category']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE requirements SET title = ?, description = ?, category = ? WHERE id = ?',
        (data['title'], data['description'], data['category'], req_id)
    )
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Requirement not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/requirements/<int:req_id>', methods=['DELETE'])
def api_admin_requirements_delete(req_id):
    """API endpoint to delete a requirement"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM requirements WHERE id = ?', (req_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Requirement not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Health Services Routes - RESTful pattern
@app.route('/api/admin/health-services', methods=['GET'])
def api_admin_health_services_get():
    """API endpoint to get all health services"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM health_services ORDER BY id').fetchall()
    conn.close()
    
    result = []
    for service in services:
        result.append({
            "id": service['id'],
            "service_name": service['service_name'],
            "schedule": service['schedule'],
            "description": service['description']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/health-services', methods=['POST'])
def api_admin_health_services_post():
    """API endpoint to create new health service"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['service_name', 'schedule']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO health_services (service_name, schedule, description) VALUES (?, ?, ?)',
        (data['service_name'], data['schedule'], data.get('description', ''))
    )
    service_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': service_id, 'success': True})

@app.route('/api/admin/health-services/<int:service_id>', methods=['GET'])
def api_admin_health_services_get_one(service_id):
    """API endpoint to get a specific health service"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    service = conn.execute('SELECT * FROM health_services WHERE id = ?', (service_id,)).fetchone()
    conn.close()
    
    if not service:
        return jsonify({'error': 'Health service not found'}), 404
    
    result = {
        "id": service['id'],
        "service_name": service['service_name'],
        "schedule": service['schedule'],
        "description": service['description']
    }
    
    return jsonify(result)

@app.route('/api/admin/health-services/<int:service_id>', methods=['PUT'])
def api_admin_health_services_put(service_id):
    """API endpoint to update a health service"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['service_name', 'schedule']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE health_services SET service_name = ?, schedule = ?, description = ? WHERE id = ?',
        (data['service_name'], data['schedule'], data.get('description', ''), service_id)
    )
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Health service not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/health-services/<int:service_id>', methods=['DELETE'])
def api_admin_health_services_delete(service_id):
    """API endpoint to delete a health service"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM health_services WHERE id = ?', (service_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Health service not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Contacts Routes - RESTful pattern
@app.route('/api/admin/contacts', methods=['GET'])
def api_admin_contacts_get():
    """API endpoint to get all contacts"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts ORDER BY category, id').fetchall()
    conn.close()
    
    result = []
    for contact in contacts:
        result.append({
            "id": contact['id'],
            "name": contact['name'],
            "value": contact['value'],
            "category": contact['category']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/contacts', methods=['POST'])
def api_admin_contacts_post():
    """API endpoint to create new contact"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['name', 'value', 'category']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (name, value, category) VALUES (?, ?, ?)',
        (data['name'], data['value'], data['category'])
    )
    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': contact_id, 'success': True})

@app.route('/api/admin/contacts/<int:contact_id>', methods=['GET'])
def api_admin_contacts_get_one(contact_id):
    """API endpoint to get a specific contact"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,)).fetchone()
    conn.close()
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    result = {
        "id": contact['id'],
        "name": contact['name'],
        "value": contact['value'],
        "category": contact['category']
    }
    
    return jsonify(result)

@app.route('/api/admin/contacts/<int:contact_id>', methods=['PUT'])
def api_admin_contacts_put(contact_id):
    """API endpoint to update a contact"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['name', 'value', 'category']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE contacts SET name = ?, value = ?, category = ? WHERE id = ?',
        (data['name'], data['value'], data['category'], contact_id)
    )
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Contact not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/contacts/<int:contact_id>', methods=['DELETE'])
def api_admin_contacts_delete(contact_id):
    """API endpoint to delete a contact"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Contact not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Rehabilitation Programs Routes - RESTful pattern
@app.route('/api/admin/rehab-programs', methods=['GET'])
def api_admin_rehab_programs_get():
    """API endpoint to get all rehabilitation programs"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    programs = conn.execute('SELECT * FROM rehabilitation_programs ORDER BY id').fetchall()
    conn.close()
    
    result = []
    for program in programs:
        result.append({
            "id": program['id'],
            "program_name": program['program_name'],
            "description": program['description'],
            "schedule": program['schedule']
        })
    
    return jsonify({"data": result})

@app.route('/api/admin/rehab-programs', methods=['POST'])
def api_admin_rehab_programs_post():
    """API endpoint to create new rehabilitation program"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['program_name', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO rehabilitation_programs (program_name, description, schedule) VALUES (?, ?, ?)',
        (data['program_name'], data['description'], data.get('schedule', ''))
    )
    program_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': program_id, 'success': True})

@app.route('/api/admin/rehab-programs/<int:program_id>', methods=['GET'])
def api_admin_rehab_programs_get_one(program_id):
    """API endpoint to get a specific rehabilitation program"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    program = conn.execute('SELECT * FROM rehabilitation_programs WHERE id = ?', (program_id,)).fetchone()
    conn.close()
    
    if not program:
        return jsonify({'error': 'Rehabilitation program not found'}), 404
    
    result = {
        "id": program['id'],
        "program_name": program['program_name'],
        "description": program['description'],
        "schedule": program['schedule']
    }
    
    return jsonify(result)

@app.route('/api/admin/rehab-programs/<int:program_id>', methods=['PUT'])
def api_admin_rehab_programs_put(program_id):
    """API endpoint to update a rehabilitation program"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['program_name', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE rehabilitation_programs SET program_name = ?, description = ?, schedule = ? WHERE id = ?',
        (data['program_name'], data['description'], data.get('schedule', ''), program_id)
    )
    
    # Check if the record exists and was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Rehabilitation program not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/admin/rehab-programs/<int:program_id>', methods=['DELETE'])
def api_admin_rehab_programs_delete(program_id):
    """API endpoint to delete a rehabilitation program"""
    if not check_admin_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM rehabilitation_programs WHERE id = ?', (program_id,))
    
    # Check if the record exists and was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Rehabilitation program not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "message": str(e)}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error", "message": str(e)}), 500

# Helper untuk validasi input
def validate_api_input(data, required_fields):
    """Validate API input has all required fields"""
    if not data:
        return "No data provided"
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)