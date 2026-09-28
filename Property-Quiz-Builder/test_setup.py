import os
from dotenv import load_dotenv

print("Testing environment setup...")

# Test 1: cek semua package ke-import dengan benar
try:
    import streamlit
    import pydantic
    from google import genai
    print("[OK] streamlit, pydantic, dan google-genai berhasil di-import")
except ImportError as e:
    print("[GAGAL] ada package belum terinstall dengan benar:", e)

# Test 2: cek .env terbaca
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"[OK] GEMINI_API_KEY ditemukan ({len(api_key)} karakter)")
else:
    print("[GAGAL] GEMINI_API_KEY tidak ditemukan - cek lagi isi file .env")