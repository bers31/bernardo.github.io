<div class="hero">

<h1>🧠 Property Knowledge Quiz Builder</h1>

<p>AI Quiz Generation · Structured Output · LLM-as-Judge · Interactive Assessment</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Google%20Gemini%20API-8B5CF6?style=flat-square&logo=googlegemini&logoColor=white" alt="Google Gemini API"/>
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic"/>
  <img src="https://img.shields.io/badge/LLM%20Application-6D28D9?style=flat-square" alt="LLM Application"/>
  <img src="https://img.shields.io/badge/Structured%20Output-7C3AED?style=flat-square" alt="Structured Output"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="MIT License"/>
</p>

<p>
An end-to-end AI assessment pipeline that turns a topic, target role,
difficulty, and language into a structured multiple-choice quiz —
validated programmatically, reviewed by a second LLM, automatically retried
when quality gates fail, and delivered as an interactive assessment.
</p>

</div>

---

## 📖 Project Overview

**Property Knowledge Quiz Builder** is an AI-powered assessment application designed to generate property-industry knowledge quizzes for employee learning and training.

The project was built around a simple observation:

> Generating a quiz is easy. Generating a quiz that is structurally valid, relevant, answerable, and consistent is a different engineering problem.

Instead of relying on a single LLM request, the application treats quiz generation as a **multi-stage quality pipeline**:

```text
User Configuration
      ↓
Prompt Construction
      ↓
Structured Generation
      ↓
Programmatic Validation
      ↓
AI Quality Review
      ↓
  Pass / Retry
      ↓
Interactive Quiz
      ↓
Automatic Scoring
      ↓
Feedback & Explanation
```

The result is an application that uses the LLM for what it does well—content generation and semantic judgment—while deterministic Python code handles structure, validation, orchestration, and application behavior.

> **Core philosophy:** the model generates the content, but the application decides whether that content is acceptable.

---

## 🎯 Project Objectives

### 🧠 Generate Useful Assessment Content

Turn a single topic into a complete multiple-choice assessment without requiring manual question authoring.

### 📦 Enforce Machine-Readable Output

Ensure generated quizzes conform to an explicit schema instead of depending on loosely formatted JSON-like text.

### 🛡️ Detect Structural Problems

Catch issues such as:

* incorrect question count,
* duplicate questions,
* empty options,
* duplicate options,
* malformed answer structures,
* inconsistent difficulty configuration.

### 🧑‍⚖️ Review Semantic Quality

Use a second Gemini call to evaluate generated content for problems that deterministic checks cannot reliably detect.

### 🔁 Recover From Failed Generations

Automatically regenerate the quiz when a validation or quality gate fails, rather than exposing malformed content to the end user.

### 🎮 Deliver a Real Assessment Experience

Present the generated content as an interactive quiz with scoring and question-level explanations instead of returning raw model output.

### 💰 Keep the Architecture Cost-Conscious

The project is designed to run using free-tier infrastructure where available, making it practical for experimentation, portfolio demonstration, and lightweight internal training use.

---

## ✨ Key Features

### 🧬 Schema-Constrained Generation

The application uses **Pydantic models as the source of truth for quiz structure**.

Instead of asking the LLM to "return JSON", the schema is supplied to the Gemini API through structured output configuration.

```text
Pydantic Schema
      ↓
Gemini response_schema
      ↓
Structured Model Response
      ↓
Typed Python Object
```

This moves part of the reliability problem from prompt wording into the application architecture.

---

### 🛡️ Two-Stage Quality Gate

The generated quiz passes through two different validation mechanisms.

**Programmatic validation** handles deterministic requirements such as:

* question count,
* duplicate detection,
* option integrity,
* empty values,
* configured difficulty,
* basic structural consistency.

**AI quality assurance** handles semantic checks such as:

* topic relevance,
* distractor quality,
* ambiguity,
* explanation consistency,
* factual plausibility.

The important architectural distinction is:

```text
Code guarantees structure.
LLM evaluates semantic quality.
```

Neither mechanism is expected to replace the other.

---

### 🔁 Self-Healing Retry Pipeline

When a quiz fails validation or AI quality review, the pipeline does not immediately expose the failure to the user.

Instead:

```text
Generation
    ↓
Validation / QA
    ↓
Failed?
    ├── No → Continue
    │
    └── Yes
          ↓
      Log Reason
          ↓
      Retry
          ↓
     Up to 3 Attempts
```

Each attempt is recorded so that the generation process remains inspectable.

---

### 🎛️ Configurable Assessment Generation

The interface supports configurable inputs including:

| Input              | Supported Configuration                                          |
| ------------------ | ---------------------------------------------------------------- |
| **Topic**          | Free-text property knowledge topic                               |
| **Target Role**    | Property Agent, Sales, Marketing, Customer Support, New Employee |
| **Question Count** | User-defined assessment size                                     |
| **Difficulty**     | Beginner, Intermediate, Advanced                                 |
| **Language**       | Configurable quiz language                                       |

The same generation pipeline can therefore be reused for different employee groups without changing the underlying application architecture.

---

### 🎮 Interactive Assessment Experience

The final output is rendered as an interactive Streamlit application rather than raw generated text.

The user can:

* answer individual questions,
* submit the assessment,
* receive an immediate score,
* inspect per-question results,
* read explanations,
* review the generation process through the log panel.

The application uses **Streamlit session state** to preserve quiz interaction across Streamlit reruns.

---

### 📜 Transparent Generation Log

Every generation attempt can surface:

* attempt number,
* validation result,
* AI QA result,
* failure reason,
* retry state,
* final outcome.

This makes the application more transparent than a typical black-box AI interface.

Instead of:

> "The AI generated something."

the system can expose:

> "Attempt 1 failed semantic QA because two distractors were too obviously incorrect. The pipeline regenerated the quiz and passed on Attempt 2."

---

## 🧠 AI Workflow

```text
┌───────────────────────┐
│      USER INPUT       │
│ Topic / Role / Level  │
│ Question Count / Lang │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│   PROMPT BUILDER      │
│ Context + Constraints │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│     GEMINI API        │
│ Structured Generation │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│ PROGRAMMATIC CHECKS   │
│ Pydantic + Python     │
└───────────┬───────────┘
            ↓
        Valid?
       /      \
     No        Yes
     ↓          ↓
   Retry    AI QUALITY
             REVIEW
               ↓
            Pass?
           /    \
         No      Yes
         ↓        ↓
       Retry   PRESENT
                  ↓
               SCORE
                  ↓
              EXPLAIN
```

---

## 🏗️ System Architecture

### 🖥️ 1. Input Layer

Streamlit provides the user-facing interface for configuring the assessment.

Inputs include topic, audience, question count, difficulty, and language.

### 🤖 2. Generation Layer

The prompt builder transforms user configuration into a structured generation request.

The Gemini client handles communication with the Google Gemini API and structured output configuration.

### 🛡️ 3. Assurance Layer

The assurance layer is where most of the reliability engineering lives:

```text
Generated Quiz
     ↓
Pydantic / Python Validation
     ↓
AI Quality Review
     ↓
Pass / Retry Decision
```

### 🎮 4. Presentation Layer

A valid quiz is transformed into an interactive assessment containing:

* multiple-choice questions,
* answer selection,
* scoring,
* explanations,
* generation status.

---

## 🧩 Core Components

| Component                    | Responsibility                                        |
| ---------------------------- | ----------------------------------------------------- |
| 📋 **Prompt Builder**        | Constructs generation prompts from user configuration |
| 🤖 **Gemini Client**         | Handles API communication and structured generation   |
| 🧩 **Pydantic Schemas**      | Define the expected shape of generated data           |
| ✅ **Programmatic Validator** | Performs deterministic structural checks              |
| 🧑‍⚖️ **AI QA Checker**      | Performs semantic review using a second LLM call      |
| 🔁 **Quiz Pipeline**         | Orchestrates generation, validation, QA, and retry    |
| 🎮 **Interactive UI**        | Handles quiz rendering, state, scoring, and feedback  |

---

## 🔬 Technical Implementation

### Structured Output

The system uses schema-driven generation rather than relying exclusively on prompt instructions.

```text
Pydantic Model
      ↓
JSON / Schema Definition
      ↓
Gemini response_schema
      ↓
Structured Response
      ↓
Typed Python Object
```

The architectural advantage is that the application's expected data contract is defined explicitly before content generation takes place.

---

### LLM-as-Judge

A second Gemini request is used exclusively for **quality review**.

The reviewer receives an already-generated quiz and evaluates it against criteria such as:

| Criterion                   | Question                                                              |
| --------------------------- | --------------------------------------------------------------------- |
| **Relevance**               | Does the question actually match the requested topic?                 |
| **Distractor Quality**      | Are incorrect answers plausible enough to test understanding?         |
| **Ambiguity**               | Could multiple answers reasonably appear correct?                     |
| **Explanation Consistency** | Does the explanation match the intended answer?                       |
| **Factual Plausibility**    | Does the generated content appear logically and factually defensible? |

The reviewer is not responsible for regenerating the quiz. Its role is to **judge quality and return a decision**.

---

### 🔁 Retry Strategy

A failed generation follows a controlled retry path.

```text
Attempt 1
   ↓
Validation
   ↓
AI QA
   ↓
Failure
   ↓
Reason Logged
   ↓
Retry
   ↓
Attempt 2
   ↓
...
   ↓
Maximum 3 Attempts
```

This keeps the user experience simple while maintaining observability during generation.

---

## 🛡️ Quality Assurance Framework

```text
                       QUIZ REQUEST
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
        STRUCTURAL       SEMANTIC     CONFIGURATION
          CHECKS           QA           RULES
        Python +        Second LLM    Role / Level /
        Pydantic         Reviewer      Count / Lang
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                   PASS / RETRY DECISION
                            ↓
                    INTERACTIVE QUIZ
```

The key design principle is **defense in depth**: no single validation mechanism is expected to catch every possible failure mode.

---

## 🧪 Testing & Iteration

During development, the application was manually exercised against multiple property-industry topics, including:

* **Property Market Updates in Jakarta**
* **Basic KPR Knowledge**
* **Top Skills of a Property Agent**

These scenarios were tested across different roles, difficulty levels, and languages to verify the end-to-end behavior of:

```text
Generate
   ↓
Validate
   ↓
Review
   ↓
Retry if Needed
   ↓
Present
   ↓
Score
```

The runtime validation and retry loop provides **automated quality control for each generation**.

It should not, however, be described as a substitute for a comprehensive offline test suite or a formal benchmark.

> **Honesty note:** this project intentionally does not claim a numerical accuracy or hallucination rate without a controlled evaluation dataset.

---

## 📈 From Prompt to Assessment

```text
Topic
  ↓
User Configuration
  ↓
Structured Prompt
  ↓
Constrained Generation
  ↓
Programmatic Validation
  ↓
AI Quality Review
  ↓
Verified Quiz
  ↓
Human Interaction
  ↓
Automatic Scoring
  ↓
Instant Feedback
```

The important transformation is:

> **Unstructured user intent → validated assessment artifact**

---

## 🛠️ Technology Stack

| Layer                   | Technology                | Role                                          |
| ----------------------- | ------------------------- | --------------------------------------------- |
| 🖥️ **Application**     | Streamlit                 | UI, state management, and application runtime |
| 🧠 **LLM**              | Google Gemini API         | Quiz generation and semantic quality review   |
| 📦 **Model**            | `gemini-2.5-flash`        | Structured generation and QA                  |
| 🧩 **Validation**       | Pydantic                  | Schema definition and type validation         |
| 🐍 **Language**         | Python                    | Application and orchestration logic           |
| 🔐 **Configuration**    | `python-dotenv`           | Environment variable management               |
| 🗂️ **Version Control** | Git + GitHub              | Source control and project history            |
| ☁️ **Deployment**       | Streamlit Community Cloud | Public application hosting                    |

---

## 🗂️ Repository Structure

```text
99group-quiz-generator/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
│
├── prompts/
│   └── quiz_generation_prompt.md
│
├── src/
│   ├── schemas.py
│   ├── prompt_builder.py
│   ├── gemini_client.py
│   ├── validation.py
│   ├── qa_checker.py
│   └── quiz_pipeline.py
│
├── examples/
│
├── docs/
│
└── LICENSE
```

The intended architecture keeps **generation, validation, AI review, and orchestration separate**, making individual components easier to inspect and test.

---

## 🗺️ Project Scope

| Capability                                            | Status                                           |
| ----------------------------------------------------- | ------------------------------------------------ |
| 🎛️ Configurable topic / role / difficulty / language | ✅ Implemented                                    |
| 🤖 Structured AI quiz generation                      | ✅ Implemented                                    |
| 🧩 Pydantic schema validation                         | ✅ Implemented                                    |
| ✅ Programmatic validation                             | ✅ Implemented                                    |
| 🧑‍⚖️ AI quality review                               | ✅ Implemented                                    |
| 🔁 Automatic retry                                    | ✅ Implemented                                    |
| 🎮 Interactive quiz interface                         | ✅ Implemented                                    |
| 🧮 Automatic scoring                                  | ✅ Implemented                                    |
| 📜 Generation log                                     | ✅ Implemented                                    |
| ☁️ Streamlit deployment                               | 🚧 Deployment status depends on live environment |

---

## 🎥 Demo

### 🖥️ Live Application

<div align="center">

<p><strong>🧠 99 Group AI Property Knowledge Quiz Builder</strong></p>

<p>
<a href="https://your-app-name.streamlit.app">
<strong>► View Live Application</strong>
</a>
</p>

</div>

> Replace the URL above with the actual Streamlit Community Cloud deployment before publishing.

### 📸 Preview

![Quiz Builder Preview](images/quiz-builder-preview.png)

*Topic configuration, AI-generated assessment, scoring, and feedback within a single Streamlit application.*

---

## 🚀 Getting Started

### 1. Clone the Repository

```text
git clone https://github.com/<your-username>/99group-quiz-generator.git
cd 99group-quiz-generator
```

### 2. Create a Virtual Environment

```text
python -m venv .venv
```

Activate it:

```text
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```text
pip install -r requirements.txt
```

### 4. Configure the API Key

Copy the example environment file:

```text
cp .env.example .env
```

Then add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not commit `.env` or any secret credentials to the repository.

### 5. Run the Application

```text
streamlit run app.py
```

The application will then be available through the local Streamlit server.

---

## 💼 Portfolio Alignment

| Skill                           | Demonstrated Through                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| **LLM Application Engineering** | Multi-stage generation, validation, review, and retry pipeline                        |
| **Structured Generation**       | Gemini structured output + Pydantic schemas                                           |
| **LLM-as-Judge**                | Independent second model call for semantic quality review                             |
| **Defensive Programming**       | Deterministic validation before AI assessment                                         |
| **Python Architecture**         | Separated schema, prompt, API, validation, QA, and pipeline modules                   |
| **Stateful UI Development**     | Streamlit `session_state` for multi-step quiz interaction                             |
| **Prompt Engineering**          | Structured prompts with explicit context and constraints                              |
| **Error Handling**              | Controlled retry loop with graceful failure behavior                                  |
| **Cost-Aware Engineering**      | Free-tier oriented architecture                                                       |
| **Technical Documentation**     | Architecture, limitations, workflow, and implementation documented alongside the code |

> **Portfolio positioning:** the main engineering challenge is not making an LLM generate questions. It is designing the surrounding system so that a non-deterministic model becomes part of a predictable application workflow.

---

## ⚠️ Known Limitations

The current implementation has several intentional limitations.

### No Persistent Quiz Storage

Quiz state is session-based and can be lost when the application is refreshed or the session ends.

### Runtime Validation Is Not a Formal Benchmark

The validation and AI QA layers improve generation reliability, but they do not establish a statistically measured accuracy rate or guarantee factual correctness.

### LLM Judgment Can Still Be Imperfect

The AI reviewer is another probabilistic model. It can identify semantic problems that code cannot, but it can also miss subtle issues or make an incorrect judgment.

### Difficulty Is Prompt-Driven

`Beginner`, `Intermediate`, and `Advanced` are treated as generation constraints rather than empirically calibrated difficulty levels.

### Free-Tier Constraints

High-frequency generation can encounter provider rate limits or other free-tier restrictions.

---

## 🔭 Future Development

Potential extensions include:

* Persistent quiz history
* Employee-level assessment tracking
* Aggregate performance dashboards
* PDF and Word export
* Question bank storage
* Retrieval-augmented generation using internal training material
* Evaluation datasets for measurable quality benchmarking
* Automated regression testing for prompt and model changes
* Adaptive difficulty based on historical performance
* More granular model-based scoring and confidence estimation

A particularly valuable future step would be establishing a **fixed evaluation dataset** so that prompt, model, and validation changes can be compared quantitatively instead of relying only on manual inspection.

---

## 🧠 Key Engineering Takeaways

This project demonstrates several principles relevant to production-oriented LLM applications:

### 1. Let Code Guarantee What Code Can Guarantee

Schema validation, required fields, duplicates, and structural consistency should not depend entirely on model instructions.

### 2. Use the LLM Where Semantic Judgment Is Required

Relevance, ambiguity, distractor quality, and explanation consistency are much harder to validate with simple deterministic rules.

### 3. Separate Generation From Evaluation

Asking one model call to generate and self-certify its own output creates unnecessary blind spots. A separate QA stage creates a clearer quality boundary.

### 4. Build Recovery Into the Pipeline

A model failure should be treated as an expected operational condition, not an exceptional event that crashes the entire application.

### 5. Measure Before Making Strong Claims

Without a benchmark dataset, claims such as "95% accurate" or "hallucination-free" would be misleading. This project therefore focuses on architecture and observable validation behavior rather than invented performance numbers.

---

## 📄 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

The MIT License permits reuse, modification, and distribution subject to the conditions stated in the license.

---

<div class="contact-hero">

<p><strong>Interested in the engineering behind this project?</strong></p>

<p>
👨‍💻 <strong>Bernardo Nandaniar Sunia</strong><br/>
Data Analyst · Bachelor of Computer Science<br/>
Python · Data Analytics · LLM Applications · NLP
</p>

<p>
<a href="https://linkedin.com/in/bernardo-sunia/">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>
<a href="mailto:suniabernardo@gmail.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
</a>
<a href="https://github.com/bers31">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
<a href="https://bit.ly/bernardo-my_portfolio">
<img src="https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white" alt="Portfolio">
</a>
</p>

<p>
<em>Python · Streamlit · Google Gemini API · Pydantic · LLM Application Engineering</em>
</p>

</div>

---

### 📸 Application Preview

![Screenshot 1](images/Picture1.png)
![Screenshot 2](images/Picture2.png)
![Screenshot 3](images/Picture3.png)
![Screenshot 4](images/Picture4.png)
![Screenshot 5](images/Picture5.png)
![Screenshot 6](images/Picture6.png)
![Screenshot 7](images/Picture7.png)

---

## 📌 Conclusion

The core lesson of this project is simple:

> **The difficult part of an LLM application is not generating text. It is building the system around the model so that the generated result becomes useful, validated, recoverable, and observable.**

Property Knowledge Quiz Builder applies that principle through:

```text
Structured Generation
        +
Deterministic Validation
        +
Independent AI Quality Review
        +
Automatic Retry
        +
Interactive Delivery
        =
More Reliable LLM Application
```

The application therefore serves as more than a quiz generator. It is a practical example of how **software engineering discipline can be applied around a probabilistic model** to create a more controlled and maintainable AI workflow.