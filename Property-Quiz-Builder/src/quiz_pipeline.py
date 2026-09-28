import time
from src.prompt_builder import build_quiz_prompt
from src.gemini_client import generate_structured
from src.schemas import Quiz
from src.validation import validate_quiz
from src.qa_checker import run_ai_qa

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def generate_valid_quiz(topic: str, role: str, num_questions: int, difficulty: str, language: str):
    """
    generate -> validasi programmatic -> AI QA -> retry kalau gagal di step manapun.
    Return: {"success": bool, "quiz": Quiz | None, "log": list[str]}
    `log` = jejak tiap percobaan, ini bukti testing/iteration untuk evaluator.
    """
    log = []
    prompt = build_quiz_prompt(topic, role, num_questions, difficulty, language)

    for attempt in range(1, MAX_RETRIES + 1):
        log.append(f"Percobaan {attempt}/{MAX_RETRIES}: generate quiz...")
        try:
            quiz = generate_structured(prompt, Quiz)

            if quiz is None:
                log.append(f"Percobaan {attempt}: Gemini gagal mengembalikan hasil yang bisa di-parse.")
            else:
                is_valid, val_errors = validate_quiz(quiz, num_questions, difficulty)
                if not is_valid:
                    log.append(f"Percobaan {attempt}: gagal programmatic validation - {'; '.join(val_errors)}")
                else:
                    log.append(f"Percobaan {attempt}: lolos programmatic validation. Menjalankan AI QA...")
                    qa_result = run_ai_qa(quiz)

                    if qa_result is None:
                        log.append(f"Percobaan {attempt}: AI QA gagal dijalankan.")
                    elif not qa_result.passed:
                        log.append(f"Percobaan {attempt}: gagal AI QA - {'; '.join(qa_result.issues)}")
                    else:
                        log.append(f"Percobaan {attempt}: lolos semua pengecekan.")
                        return {"success": True, "quiz": quiz, "log": log}

        except Exception as e:
            log.append(f"Percobaan {attempt}: error tak terduga - {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    log.append(f"Menyerah setelah {MAX_RETRIES} percobaan.")
    return {"success": False, "quiz": None, "log": log}