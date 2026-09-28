from typing import Literal
from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str = Field(description="Teks pertanyaan quiz")
    option_a: str = Field(description="Pilihan jawaban A")
    option_b: str = Field(description="Pilihan jawaban B")
    option_c: str = Field(description="Pilihan jawaban C")
    option_d: str = Field(description="Pilihan jawaban D")
    correct_answer: Literal["A", "B", "C", "D"] = Field(
        description="Huruf jawaban yang benar, harus salah satu dari A/B/C/D"
    )
    explanation: str = Field(description="Penjelasan kenapa correct_answer itu benar")
    learning_objective: str = Field(description="Apa yang dipelajari user dari soal ini")
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]


class Quiz(BaseModel):
    topic: str
    target_role: str
    language: str
    questions: list[QuizQuestion]