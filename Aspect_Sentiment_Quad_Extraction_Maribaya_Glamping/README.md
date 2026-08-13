<div align="center">
  <h1>🧠 Aspect Sentiment Quad Extraction (ASQE) for Maribaya & Glamping Reviews</h1>
  <h3>Beyond Star Ratings · Aspect-Level Sentiment Understanding · Custom Indonesian Review Dataset</h3>

  <br/>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NLP-Aspect%20Based%20Sentiment-FFD21E?style=for-the-badge" alt="ABSA">
  <img src="https://img.shields.io/badge/Task-Quad%20Extraction-8B5CF6?style=for-the-badge" alt="ASQE">
  <img src="https://img.shields.io/badge/Dataset-1%2C000%2B%20Custom%20Labeled-1D4ED8?style=for-the-badge" alt="Dataset">
  <img src="https://img.shields.io/badge/Status-Active%20Development-F59E0B?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Project-Client%20%2F%20Confidential-1D4ED8?style=for-the-badge" alt="Client Project">

  <br/><br/>

  <sub>Part of my <a href="https://bers31.github.io/bernardo.github.io/">Data Analyst portfolio</a> · Flagship NLP project</sub>
</div>

---

## 📖 Project Overview

Star ratings are convenient, but they hide as much as they reveal. A guest can leave a rating of 3 after writing that the pool was excellent but parking was cramped. The number alone can't tell you *which part* of the experience actually needs attention. This project builds an **Aspect Sentiment Quad Extraction (ASQE)** pipeline for Maribaya and Glamping visitor reviews to close that gap: instead of one aggregate score, every review is broken down into the specific aspects mentioned, the opinion expressed about each one, and the sentiment polarity behind it.

> **Why quad extraction, specifically:** rating- and label-based analysis can only answer *how satisfied* (magnitude). Extracting aspect and opinion terms answers *about what, specifically, and why* (content), the part that actually drives operational decisions.

---

## ❓ The Problem with Conventional Ratings

| Misalignment Source | Example |
|----------------------|---------|
| **Sub-experience aggregation** | A rating of 3 given despite the review praising the pool and only criticizing parking |
| **Inconsistent personal scale calibration** | A "3" means "decent" to one guest and "disappointing" to another |
| **Rated-but-unmentioned aspects (or vice versa)** | An aspect is scored in the rating widget but never appears in the written review, or discussed in text but never separately rated |
| **Impression-based rather than aspect-based scoring** | The overall rating reflects a general impression rather than a logical breakdown per aspect |

---

## 🧩 What ASQE Extracts

From a single review, the pipeline runs **four ABSA subtasks simultaneously**, each with its own confidence score:

| # | Subtask | Output |
|---|---------|--------|
| 1 | Aspect Term Extraction | The specific aspect mentioned (e.g. *tempat*, *parkir*) |
| 2 | Opinion Term Extraction | The opinion word tied to that aspect (e.g. *bagus*, *sempit*) |
| 3 | Aspect Category Detection | The broader category the aspect belongs to (e.g. *fasilitas*) |
| 4 | Sentiment Polarity Labeling | Positive / negative / neutral, per opinion term |

### Sample Output

**Review:** *"Tempatnya bagus, tapi parkirannya sempit"*

| Component | Result |
|-----------|--------|
| Aspect | `tempat` (0.9), `parkir` (0.9) |
| Opinion | tempat → `bagus` (0.9), parkir → `sempit` (0.9) |
| Category | tempat → `tempat` (1.0), parkir → `fasilitas` (0.9) |
| Sentiment | bagus → `positive` (1.0), sempit → `negative` (0.9) |

---

## 📊 Dataset

| Source | Description |
|--------|-------------|
| **Airyroom** (public hotel review dataset) | Originally built for aspect–sentiment *pair* extraction; re-labeled and restructured for aspect–sentiment *quad* extraction. Machine-labeled, pending manual verification. |
| **Maribaya-specific dataset** (self-built, 1,000+ reviews) | Built independently to teach the model Maribaya-specific aspect vocabulary that a general-domain dataset wouldn't recognize |

**The custom dataset deliberately targets difficult review patterns** that general-domain models typically fail on:

- Sarcasm and complex/double negation
- Dense, multi-aspect reviews
- Informal language, slang, abbreviations, typos
- Code-mixing (Indonesian–English)
- Ambiguity
- Implicit aspect–sentiment expression
- Emoji used as sentiment markers
- Conditional, comparative, and temporal sentence structures
- Deliberate word repetition as an intensifier (e.g. *"jelekkk bangettt"*)
- Internet culture expressions (e.g. *"wkwkwk"*)
- Mixed positive–negative sentiment within a single aspect

---

## 🔭 Roadmap

- **Timeline-based aspect mapping**: surface which aspects are discussed most in a given period, as a signal of what matters most to guests right now
- **Emerging issue detection**: track topic activity over time to catch a complaint spike on a specific aspect before it becomes entrenched
- **Aspect category clustering**: manual clustering and zero-shot clustering via **BERTopic**: text is first matched against a predefined topic list by similarity threshold, and unmatched text is routed into a clustering pipeline to surface new topics
- **Business-outcome-weighted clustering**: weighting clusters by their correlation with overall rating, repeat booking, and cancellation rate, since a frequently-mentioned cluster isn't necessarily the most business-critical one; a rare but high-churn-correlated complaint can matter more than a common but minor one
- **Fast positive/negative aspect scan**: a quick view of which aspects are dominated by positive vs. negative sentiment, as an evaluation aid

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python |
| **Core Task** | Aspect-Based Sentiment Analysis, Aspect Sentiment Quad Extraction (ASQE) |
| **Representation** | Transformer-based sentence/token embeddings |
| **Dataset Engineering** | Custom Indonesian review annotation, public dataset re-labeling (Airyroom) |
| **Planned Extension** | BERTopic (zero-shot topic clustering) |

---

## 🔬 Why This Project Matters

This is the flagship NLP project of my time at PT Wiraky Nusa Telekomunikasi. It moves review analysis from *"how happy are guests, on average"* to *"what specifically is working, what specifically isn't, and how confident are we in that read."* The custom dataset work targets the exact patterns (sarcasm, code-mixing, informal slang) that make Indonesian-language ABSA meaningfully harder than English-language ABSA, which most public datasets and pretrained models aren't built to handle well.

---

## 📄 Project Ownership

This project was developed during my tenure as **Data Analyst at PT Wiraky Nusa Telekomunikasi** for the Maribaya & Glamping properties. It is documented here as a professional portfolio case study; the underlying dataset and production model remain the property of PT Wiraky Nusa Telekomunikasi / Maribaya.

## 📫 Contact & Connect

<p align="center">
<strong>👨‍💻 Bernardo Nandaniar Sunia, Data Analyst</strong><br/>
Universitas Diponegoro 🎓
</p>

<p align="center">
<a href="https://linkedin.com/in/bernardo-sunia/">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=suniabernardo@gmail.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
</a>
<a href="https://github.com/bers31">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
<a href="https://bit.ly/bernardo-my_portfolio">
<img src="https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white" alt="Portfolio">
</a>
</p>
