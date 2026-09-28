import streamlit as st
from src.quiz_pipeline import generate_valid_quiz

st.set_page_config(page_title="99 Group AI Property Knowledge Quiz Builder")
st.title("99 Group AI Property Knowledge Quiz Builder")
st.caption("Generate quiz otomatis untuk topik knowledge industri property.")

if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "generation_log" not in st.session_state:
    st.session_state.generation_log = []
if "answers_submitted" not in st.session_state:
    st.session_state.answers_submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

with st.form("quiz_input_form"):
    topic = st.text_input("Topic", placeholder="Contoh: Property Market Updates in Jakarta")
    role = st.selectbox("Target role / audience", ["Property Agent", "Sales", "Marketing", "Customer Support", "New Employee"])
    num_questions = st.number_input("Jumlah soal (number of questions)", min_value=1, max_value=20, value=5, step=1)
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    language = st.selectbox("Bahasa (language)", ["Bahasa Indonesia", "English"])
    submitted = st.form_submit_button("Generate Quiz")

if submitted:
    if not topic.strip():
        st.error("Topic tidak boleh kosong. Isi dulu, baru klik Generate Quiz lagi.")
    else:
        with st.spinner("Generate quiz dengan Gemini (bisa beberapa kali percobaan)..."):
            try:
                result = generate_valid_quiz(
                    topic=topic, role=role, num_questions=int(num_questions),
                    difficulty=difficulty, language=language,
                )
                st.session_state.generation_log = result["log"]
                if result["success"]:
                    st.session_state.quiz = result["quiz"]
                    st.session_state.answers_submitted = False
                    st.session_state.user_answers = {}
                else:
                    st.session_state.quiz = None
                    st.error("Gagal generate quiz yang valid setelah beberapa percobaan. Lihat log di bawah.")
            except Exception as e:
                st.error(f"Terjadi error tak terduga: {e}")

if st.session_state.generation_log:
    with st.expander("Lihat log generation (bukti proses validasi/retry)"):
        for line in st.session_state.generation_log:
            st.text(line)

quiz = st.session_state.quiz

if quiz and not st.session_state.answers_submitted:
    st.divider()
    st.subheader(f"Quiz: {quiz.topic}")
    with st.form("quiz_answer_form"):
        user_answers = {}
        for i, q in enumerate(quiz.questions):
            st.write(f"**{i + 1}. {q.question}**")
            user_answers[i] = st.radio(
                label=f"Jawaban soal {i + 1}",
                options=["A", "B", "C", "D"],
                format_func=lambda letter, q=q: f"{letter}. " + {
                    "A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d
                }[letter],
                key=f"answer_{i}",
                label_visibility="collapsed",
            )
        answer_submitted = st.form_submit_button("Submit Jawaban")

    if answer_submitted:
        st.session_state.user_answers = user_answers
        st.session_state.answers_submitted = True
        st.rerun()

if quiz and st.session_state.answers_submitted:
    st.divider()
    user_answers = st.session_state.user_answers
    correct_count = sum(1 for i, q in enumerate(quiz.questions) if user_answers.get(i) == q.correct_answer)
    total = len(quiz.questions)
    score_percent = round((correct_count / total) * 100) if total else 0

    st.subheader(f"Hasil: {correct_count}/{total} benar ({score_percent}%)")

    for i, q in enumerate(quiz.questions):
        user_choice = user_answers.get(i)
        icon = "✅" if user_choice == q.correct_answer else "❌"
        with st.expander(f"{icon} Soal {i + 1}: {q.question}"):
            st.write(f"Jawaban Anda: **{user_choice}**")
            st.write(f"Jawaban benar: **{q.correct_answer}**")
            st.write(f"Explanation: {q.explanation}")

    if st.button("Buat Quiz Baru"):
        st.session_state.quiz = None
        st.session_state.answers_submitted = False
        st.session_state.user_answers = {}
        st.rerun()