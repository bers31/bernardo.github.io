<div align="center">

# 🛍️ TF-IDF vs SBERT — Aspect Sentiment Classification
### on Indonesian E-Commerce Reviews (Shopee Case Study)

<em>Comparative NLP Research · Aspect-Based Sentiment Analysis · Text Representation Paradigms</em>

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-SBERT-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/sentence-transformers)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Thesis](https://img.shields.io/badge/Skripsi-Undip%202026-1D4ED8?style=for-the-badge)](https://undip.ac.id)
[![Status](https://img.shields.io/badge/Status-Completed-22C55E?style=for-the-badge)]()
[![Kappa](https://img.shields.io/badge/Fleiss%20Kappa-%3E%200.9-purple?style=for-the-badge)]()

</div>

---

## 📖 Project Overview

This repository contains the full implementation of my undergraduate thesis at **Universitas Diponegoro**, which investigates how different text representation paradigms affect the performance of Aspect Sentiment Classification (ASC) — a core subtask of Aspect-Based Sentiment Analysis (ABSA) — on real-world Indonesian e-commerce reviews from **Shopee**.

The study systematically compares two foundational yet contrasting approaches to text representation:

- **TF-IDF** (Term Frequency–Inverse Document Frequency) — a *sparse*, frequency-based representation that encodes statistical word importance across a corpus.
- **SBERT** (Sentence-BERT) — a *dense*, transformer-based contextual embedding model that captures deep semantic meaning at the sentence level.

Both representations are paired with **Logistic Regression** as the unified classifier, allowing for a clean, controlled comparison of text representation quality in isolation. The study covers the full NLP pipeline: data acquisition, aspect discovery, human annotation, model training, and rigorous statistical evaluation via **McNemar's Test**.

> **Key Finding:** SBERT consistently and significantly outperforms TF-IDF across all evaluation settings, with a combined test-set accuracy of **0.9444 vs. 0.9130**, confirming that Indonesian e-commerce reviews are predominantly context-driven and benefit greatly from semantic embedding.

---

## 🎯 Research Objectives

1. Build a labeled ABSA dataset for Shopee reviews in Indonesian, covering seven distinct service aspects.
2. Compare TF-IDF and SBERT under two hyperparameter scenarios: **best-per-aspect** and **universal** settings.
3. Evaluate both models using accuracy, precision, recall, F1-score, ROC-AUC, PR-AUC, and McNemar's statistical significance test.
4. Provide actionable insights for practitioners building sentiment analysis systems for Indonesian e-commerce platforms.

---

## 🏗️ Research Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                      RESEARCH PIPELINE                              │
├─────────────────┬───────────────────┬───────────────────────────────┤
│  DATA           │  ASPECT           │  MODELING &                   │
│  ACQUISITION    │  DISCOVERY        │  EVALUATION                   │
│                 │                   │                               │
│ ▸ Web Scraping  │ ▸ TF-IDF Features │ ▸ TF-IDF + Logistic Reg.      │
│   (1,000 raw    │ ▸ Truncated SVD   │ ▸ SBERT + Logistic Reg.       │
│   reviews)      │ ▸ PCA             │ ▸ Grid Search (CV=5)          │
│                 │ ▸ Hierarchical    │ ▸ Per-Aspect Hyperparams       │
│ ▸ Targeted      │   Clustering      │ ▸ Universal Hyperparams        │
│   Scraping      │   (Ward Linkage)  │ ▸ Accuracy / Precision /      │
│   (≥100/aspect) │ ▸ Keyword Extract │   Recall / F1 / AUC           │
│                 │ ▸ Manual Review   │ ▸ McNemar's Test               │
├─────────────────┴───────────────────┴───────────────────────────────┤
│  ANNOTATION: 3 Annotators · Fleiss' Kappa > 0.9 · Adjudication     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset & Aspects

Reviews were collected from the **Shopee Play Store** page using web scraping. After exploratory collection (1,000 reviews), **aspect discovery** was performed via hierarchical clustering to identify the seven dominant service aspects. Targeted scraping then ensured a minimum of **100 annotated reviews per aspect**.

| # | Aspect | Description |
|---|--------|-------------|
| 1 | 📱 **Aplikasi** | App performance, bugs, UI/UX |
| 2 | 🚚 **Pengiriman** | Delivery speed, courier quality |
| 3 | 📦 **Produk** | Product quality and accuracy |
| 4 | 💰 **Harga** | Pricing, discounts, vouchers |
| 5 | 💳 **Pembayaran** | Payment methods, transaction issues |
| 6 | 🎧 **Layanan Pelanggan** | CS responsiveness and resolution |
| 7 | 🏪 **Penjual** | Seller responsiveness and reliability |

**Annotation Quality:**

| Metric | Score | Interpretation |
|--------|-------|----------------|
| Fleiss' Kappa (all 3 annotators) | **> 0.90** | Almost Perfect Agreement |
| Cohen's Kappa (pairwise) | **> 0.90** | Almost Perfect Agreement |

---

## 🧠 Models & Methodology

### Text Representation

**TF-IDF (Sparse)**
- Vectorizes review text based on term frequency weighted against inverse document frequency.
- Produces high-dimensional, interpretable sparse vectors.
- Preprocessing: text cleaning → slang normalization (Aho-Corasick automaton) → stopword removal → stemming.

**SBERT (Dense)**
- Utilizes Sentence-BERT to generate fixed-size 768-dimensional contextual embeddings.
- Captures semantic similarity, paraphrasing, and syntactic context that TF-IDF cannot represent.
- Model: `paraphrase-multilingual-mpnet-base-v2` (multilingual, optimized for semantic similarity).

### Classifier: Logistic Regression

Logistic Regression was chosen as the shared classifier to isolate the contribution of text representation quality without introducing confounding variation from the classifier architecture.

### Evaluation Scenarios

| Scenario | Description |
|----------|-------------|
| **Best-Per-Aspect Hyperparameters** | Separate optimal hyperparameter configurations per aspect, found via Grid Search + Stratified 5-Fold CV |
| **Universal Hyperparameters** | A single optimal configuration applied across all aspects |
| **Combined Dataset** | Training on all aspects combined to evaluate cross-aspect generalization |

---

## 📈 Results

### Combined Test Set Performance (McNemar's Test)

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|-------|----------|-----------|--------|----------|---------|--------|
| TF-IDF + LR | 0.9130 | — | — | — | — | — |
| **SBERT + LR** | **0.9444** | — | — | — | — | — |

> McNemar's Test confirms that the performance difference between SBERT and TF-IDF is **statistically significant** across all evaluation scenarios.

### Key Takeaways

- **SBERT outperforms TF-IDF** consistently across all seven aspects and both hyperparameter scenarios, with no exceptions.
- The advantage of SBERT is most pronounced on aspects with high linguistic variability and implicit sentiment (e.g., *Layanan Pelanggan*, *Penjual*).
- **Universal hyperparameters** yield competitive results compared to per-aspect tuning, demonstrating that SBERT embeddings are robust enough for a one-size-fits-all configuration.
- Indonesian e-commerce reviews exhibit strong **context-dependency**, validating the use of contextual embeddings over statistical bag-of-words representations.

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.10+ |
| **ML Framework** | scikit-learn, NumPy, SciPy |
| **NLP / Embeddings** | sentence-transformers (HuggingFace), NLTK, Sastrawi |
| **Text Representation** | TF-IDF (sklearn), SBERT (paraphrase-multilingual-mpnet-base-v2) |
| **Clustering** | scipy.cluster.hierarchy (Ward Linkage), sklearn TruncatedSVD, PCA |
| **Annotation** | Manual (3 annotators) + Fleiss' Kappa via statsmodels |
| **Evaluation** | sklearn metrics, McNemar's Test (statsmodels) |
| **Visualization** | Matplotlib, Seaborn |
| **Data Handling** | Pandas, openpyxl |
| **Notebook** | Jupyter Notebook |

</div>

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or conda package manager
- ~4 GB disk space (for SBERT model download)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bers31/shopee-absa-tfidf-sbert.git
cd shopee-absa-tfidf-sbert

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Core Dependencies

```txt
scikit-learn>=1.3.0
sentence-transformers>=2.2.2
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
sastrawi>=1.0.1
nltk>=3.8.1
statsmodels>=0.14.0
openpyxl>=3.1.0
jupyter>=1.0.0
```

### Running the Pipeline

```bash
# Step 1 – Exploratory data collection & aspect discovery
jupyter notebook notebooks/01_aspect_discovery.ipynb

# Step 2 – Annotation quality analysis (Fleiss' Kappa)
jupyter notebook notebooks/02_annotation_quality.ipynb

# Step 3 – Preprocessing & dataset preparation
jupyter notebook notebooks/03_preprocessing.ipynb

# Step 4 – TF-IDF model training & evaluation
jupyter notebook notebooks/04_tfidf_model.ipynb

# Step 5 – SBERT model training & evaluation
jupyter notebook notebooks/05_sbert_model.ipynb

# Step 6 – Comparative analysis (McNemar's Test)
jupyter notebook notebooks/06_comparison_mcnemar.ipynb
```

---

## 📁 Project Structure

```
shopee-absa-tfidf-sbert/
│
├── 📂 data/
│   ├── raw/                    # Raw scraped reviews
│   ├── exploratory/            # Initial 1,000-review sample
│   ├── targeted/               # Aspect-targeted scraping results
│   └── final/                  # Annotated & cleaned final datasets per aspect
│
├── 📂 notebooks/
│   ├── 01_aspect_discovery.ipynb
│   ├── 02_annotation_quality.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_tfidf_model.ipynb
│   ├── 05_sbert_model.ipynb
│   └── 06_comparison_mcnemar.ipynb
│
├── 📂 src/
│   ├── preprocessing.py        # Text cleaning, normalization, stemming
│   ├── clustering.py           # Hierarchical clustering for aspect discovery
│   ├── annotation.py           # Kappa computation utilities
│   ├── tfidf_pipeline.py       # TF-IDF vectorization + LR training
│   ├── sbert_pipeline.py       # SBERT embedding + LR training
│   ├── evaluation.py           # Metrics: accuracy, F1, AUC, McNemar
│   └── utils.py                # Shared helpers
│
├── 📂 results/
│   ├── figures/                # Dendrogram, cluster plots, ROC/PR curves
│   ├── per_aspect/             # Per-aspect hyperparameter results
│   ├── universal/              # Universal hyperparameter results
│   └── combined/               # Combined dataset results
│
├── 📂 assets/
│   └── slang_dict.csv          # Indonesian slang normalization dictionary
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔬 Research Contributions

1. **Curated ABSA dataset** for Shopee reviews in Indonesian with high-quality annotations (Fleiss' Kappa > 0.9) covering 7 aspects and 700+ labeled samples.
2. **Rigorous empirical comparison** of sparse vs. dense text representation under controlled conditions using a shared classifier.
3. **Statistical validation** via McNemar's Test confirming that SBERT's advantage over TF-IDF is not due to random variation.
4. **Practical recommendation** for NLP practitioners: for context-heavy, informal Indonesian e-commerce text, contextual embeddings (SBERT) are the clearly superior choice over frequency-based representations.

---

## 📚 Citation

If you use this work or dataset in your research, please cite:

```bibtex
@thesis{sunia2026absa,
  author    = {Bernardo Nandaniar Sunia},
  title     = {Perbandingan TF-IDF dan SBERT dengan Logistic Regression
               untuk Aspect Sentiment Classification pada Ulasan E-Commerce
               (Studi Kasus: Aplikasi Shopee)},
  school    = {Universitas Diponegoro},
  year      = {2026},
  type      = {Undergraduate Thesis (Skripsi)},
  address   = {Semarang, Indonesia},
  note      = {Departemen Informatika, Fakultas Sains dan Matematika}
}
```

---

## 🤝 Acknowledgements

This research was completed under the supervision of:

- **Khadijah, S.Kom., M.Cs.** — Supervisor I, Departemen Informatika, Universitas Diponegoro
- **Henri Tantyoko, S.Kom., M.Kom.** — Supervisor II, Departemen Informatika, Universitas Diponegoro

Special thanks to the three annotators who contributed to the manual labeling process, and to all reviewers who provided constructive feedback during the thesis defense.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

---

## 📫 Contact

<div align="center">

**Bernardo Nandaniar Sunia**
*Computer Science Graduate · Universitas Diponegoro 🎓*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/bernardo-sunia/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:suniabernardo@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/bers31)
[![Portfolio](https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white)](https://bit.ly/bernardo-my_portfolio)

---

*If this project was useful to you, please consider giving it a ⭐ — it helps others find the work.*

*Made with 💙 and a lot of cross-validation by [Bernardo](https://github.com/bers31) at Universitas Diponegoro*

</div>
