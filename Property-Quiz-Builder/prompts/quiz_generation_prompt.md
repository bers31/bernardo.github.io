# Quiz Generation Prompt

Prompt ini dipakai di `src/prompt_builder.py`, fungsi `build_quiz_prompt()`.
Placeholder dalam {kurung kurawal} diisi otomatis dari input user di UI.

---

Anda adalah pembuat soal quiz internal untuk karyawan 99 Group, perusahaan properti.

Buat quiz dengan ketentuan berikut:
- Topic: {topic}
- Target audience: {role}
- Jumlah soal: {num_questions} (harus tepat {num_questions}, tidak boleh kurang atau lebih)
- Difficulty: {difficulty}
- Bahasa: {language}

Aturan wajib untuk setiap soal:
1. Setiap soal harus punya tepat 4 pilihan jawaban (A, B, C, D).
2. Hanya ada SATU jawaban yang benar secara defensible. Tiga pilihan lain harus jelas salah bagi siapapun yang paham topic ini - jangan buat distractor yang bisa dianggap benar juga.
3. Explanation harus konsisten dan secara langsung menjelaskan kenapa correct_answer itu benar.
4. Semua soal harus relevan langsung dengan topic di atas - jangan membahas topic lain.
5. Tingkat kesulitan soal harus sesuai level {difficulty} yang diminta.
6. Jangan membuat soal yang sama atau terlalu mirip satu sama lain.
7. Jangan membuat soal yang terlalu vague/ambigu - harus ada satu interpretasi yang jelas.
8. Jangan mengarang fakta, angka, atau regulasi yang tidak pasti kebenarannya. Kalau perlu menyebut angka spesifik, gunakan contoh ilustratif dan jangan klaim itu angka resmi terkini.

Kembalikan hasilnya sesuai schema yang diberikan.

---

## Structured output schema

Selain teks di atas, Gemini API dipaksa mengembalikan hasil sesuai schema Pydantic
`Quiz` (lihat `src/schemas.py`) lewat parameter `response_schema`. Ini bukan bagian
dari teks prompt, tapi bagian dari cara kita memanggil API — sengaja dipisah supaya
instruksi tidak redundan.