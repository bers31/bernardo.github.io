from src.schemas import Quiz


def validate_quiz(quiz: Quiz, expected_count: int, expected_difficulty: str) -> tuple[bool, list[str]]:
    """
    Programmatic validation - cek yang bisa dipastikan pakai logika biasa,
    tanpa AI. Return (is_valid, daftar_masalah).
    """
    errors = []

    if len(quiz.questions) != expected_count:
        errors.append(f"Jumlah soal salah: diminta {expected_count}, dapat {len(quiz.questions)}")

    seen_questions = set()
    for i, q in enumerate(quiz.questions, start=1):
        normalized = q.question.strip().lower()
        if normalized in seen_questions:
            errors.append(f"Soal #{i} duplicate: '{q.question}'")
        seen_questions.add(normalized)

        options = [q.option_a, q.option_b, q.option_c, q.option_d]
        if any(not opt.strip() for opt in options):
            errors.append(f"Soal #{i} punya pilihan jawaban kosong")
        if len(set(opt.strip().lower() for opt in options)) < 4:
            errors.append(f"Soal #{i} punya pilihan jawaban yang isinya sama")

        if q.difficulty != expected_difficulty:
            errors.append(f"Soal #{i} difficulty '{q.difficulty}', diminta '{expected_difficulty}'")

    return (len(errors) == 0, errors)