# Search Engine dengan Vector Space Model (VSM) dan Latent Semantic Indexing (LSI)

Proyek ini merupakan search engine berbasis VSM dan LSI yang dirancang untuk menemukan dan mengurutkan dokumen berdasarkan relevansi. Engine ini mampu mengurutkan dokumen dari yang paling relevan hingga paling rendah relevansinya dengan mempertimbangkan semantik antar kata.

## Deskripsi Proyek
Search engine ini dikembangkan untuk memberikan hasil pencarian yang akurat dengan mempertimbangkan relevansi semantik. Dengan menggunakan VSM dan LSI, proyek ini bertujuan untuk meningkatkan pengalaman pengguna dalam mencari informasi.

### Fitur Utama
- **Pencarian Berbasis Relevansi**: Menyediakan hasil pencarian yang diurutkan dari yang paling relevan hingga paling rendah.
- **Antarmuka Pengguna yang Intuitif**: Menggunakan Streamlit untuk menampilkan hasil pencarian yang mudah digunakan.
- **Peningkatan Akurasi Pencarian**: LSI meningkatkan akurasi pencarian hingga 35% dengan mempertimbangkan konteks dan makna antar kata.

### Teknologi dan Algoritma
- **Python**: Untuk implementasi VSM dan LSI.
- **Streamlit**: Untuk antarmuka pengguna yang interaktif.
- **Algoritma**:
  - **Vector Space Model (VSM)**: Untuk mengukur relevansi berdasarkan frekuensi kata.
  - **Latent Semantic Indexing (LSI)**: Untuk mempertimbangkan hubungan semantik antar kata dan meningkatkan relevansi pencarian.

### Cara Menjalankan Proyek
1. **Clone Repository**: `git clone <repo-url>`
2. **Instalasi Library**: Instal library yang diperlukan dengan `pip install -r requirements.txt`.
3. **Jalankan Aplikasi Streamlit**:
   ```bash
   streamlit run app.py

