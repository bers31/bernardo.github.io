import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def generate_text(prompt: str, model: str = "gemini-3.6-flash") -> str:
    """
    Kirim prompt ke Gemini, kembalikan teks responnya (plain text, bukan JSON).
    Dipakai di Phase 6 untuk test koneksi dasar.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan. Cek file .env Anda.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text


def generate_structured(prompt: str, schema, model: str = "gemini-3.6-flash"):
    """
    Kirim prompt ke Gemini, minta hasil dalam bentuk terstruktur sesuai `schema`
    (class Pydantic, misal Quiz dari src/schemas.py).

    SDK otomatis mengubah JSON dari Gemini jadi object Python asli lewat
    response.parsed - sudah tervalidasi tipe datanya, tidak perlu json.loads() manual.

    Return: instance dari `schema`, atau None kalau Gemini gagal menghasilkan
    sesuatu yang bisa di-parse.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan. Cek file .env Anda.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )
    return response.parsed