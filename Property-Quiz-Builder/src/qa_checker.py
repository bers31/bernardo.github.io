from pydantic import BaseModel, Field
from src.schemas import Quiz
from src.gemini_client import generate_structured


class QAResult(BaseModel):
    passed: bool = Field(description="True kalau quiz layak dipakai, False kalau ada masalah")
    issues: list[str] = Field(description="Daftar masalah spesifik, kosong kalau passed=True")


def run_ai_qa(quiz: Quiz) -> QAResult:
    """
    Cek hal yang TIDAK bisa dicek logika biasa: relevansi ke topic,
    distractor yang terlalu jelas benar, ambiguitas, konsistensi explanation.
    """
    qa_prompt = f"""Anda adalah reviewer kualitas soal quiz. Review quiz JSON di bawah ini
dengan topic "{quiz.topic}" untuk audience "{quiz.target_role}".

Quiz yang direview:
{quiz.model_dump_json(indent=2)}

Cek untuk setiap soal:
1. Apakah soal relevan langsung dengan topic di atas?
2. Apakah ada distractor (pilihan salah) yang sebenarnya bisa dianggap benar juga?
3. Apakah soal terlalu ambigu/vague, punya lebih dari satu interpretasi?
4. Apakah explanation benar-benar konsisten menjelaskan correct_answer?
5. Apakah ada fakta yang terlihat dikarang/tidak masuk akal?

Kalau SEMUA soal lolos, set passed=true dan issues kosong.
Kalau ADA masalah, set passed=false, sebutkan nomor soal + masalah spesifiknya di issues."""

    return generate_structured(qa_prompt, QAResult)