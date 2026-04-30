<div align="center">
<h1>🔍 Custom Search Engine with VSM & LSI</h1>
</div>

<div align="center">
<em>Comprehensive comparison of VSM, LSI, and Neural IR approaches using mBERT</em>

<br>

<img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
<img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge" alt="Build">
<img src="https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge" alt="Version">

</div>

---

## 📖 Project Overview

Traditional Information Retrieval (IR) systems like **Vector Space Model (VSM)** and **Latent Semantic Indexing (LSI)** have proven their worth but are limited to term-frequency and linear statistical representations. Modern **Transformer-based models** like **mBERT** leverage cross-lingual context to significantly enhance relevance matching.

This project provides a comprehensive benchmark framework that implements and compares three distinct IR approaches, offering end-to-end pipeline from data extraction to performance evaluation with precision, recall, and F1-score metrics.

**🎯 Perfect for:** Researchers, Data Scientists, IR Engineers, and Academic Projects

---

## ✨ Key Features

- 🔄 **End-to-End Pipeline**: Complete workflow from raw data to evaluation metrics
- 🧠 **Three IR Approaches**: VSM, LSI, and Neural IR with mBERT
- 📊 **Comprehensive Evaluation**: Precision@k, Recall@k, F1-score with macro averaging
- 📈 **Advanced Visualizations**: Precision-Recall curves and Mean Average Precision
- 🔧 **Modular Architecture**: Easy to extend with new models or datasets
- 🌐 **Cross-lingual Support**: Multilingual capabilities through mBERT
- 📝 **Professional Documentation**: Detailed implementation guides and examples
- ⚡ **Performance Optimized**: Efficient processing with sparse matrices and batching

---

## 🛠️ Technologies & Tools

<div align="center">

<table>
<tr>
<th>Category</th>
<th>Technologies</th>
</tr>
<tr>
<td><strong>Language</strong></td>
<td><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></td>
</tr>
<tr>
<td><strong>Data Processing</strong></td>
<td><img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas"> <img src="https://img.shields.io/badge/numpy-013243?style=flat&logo=numpy&logoColor=white" alt="NumPy"></td>
</tr>
<tr>
<td><strong>Machine Learning</strong></td>
<td><img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white" alt="scikit-learn"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" alt="PyTorch"></td>
</tr>
<tr>
<td><strong>IR & NLP</strong></td>
<td><img src="https://img.shields.io/badge/🤗_Transformers-FFD700?style=flat" alt="Transformers"> <img src="https://img.shields.io/badge/NLTK-154f3c?style=flat" alt="NLTK"></td>
</tr>
<tr>
<td><strong>Visualization</strong></td>
<td><img src="https://img.shields.io/badge/Matplotlib-11557c?style=flat" alt="Matplotlib"> <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white" alt="Jupyter"></td>
</tr>
</table>

</div>

### Core Dependencies
```bash
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
sentence-transformers>=2.2.0
torch>=1.9.0
ir-datasets>=0.5.0
matplotlib>=3.5.0
scipy>=1.7.0
```

---

## 🏗️ System Architecture

<pre>
    📊 Dataset                🔧 ETL Pipeline           📝 Preprocessing
   (ir_datasets)      →      (etl.py)          →      (Clean & Transform)
                                                               |
                                                               ↓
                                          🔀 IR Methods Selection
                                        /        |            \
                                       ↓         ↓             ↓
                              📊 VSM           🎯 LSI      🧠 Neural IR
                          (TF-IDF + Cosine)  (SVD + Latent)  (mBERT Embeddings)
                                       \         |             /
                                        \        |            /
                                         ↓       ↓           ↓
                                          📈 Evaluation Framework
                                         (Precision/Recall/F1)
                                                  |
                                                  ↓
                                          📊 Visualization
                                        (PR Curves & Metrics)
</pre>

**Architecture Components:**
- **Data Layer**: IR datasets with queries, documents, and relevance judgments
- **Processing Layer**: ETL pipeline with comprehensive text preprocessing
- **Model Layer**: Three distinct IR approaches (VSM, LSI, Neural)
- **Evaluation Layer**: Comprehensive metrics and visualization framework

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Preprocessing
```bash
# Extract and clean dataset
python src/etl.py \
  --input data/raw/ \
  --output data/processed/
```

### 3. Run IR Methods
```bash
# Vector Space Model
python src/vsm.py --data data/processed/

# Latent Semantic Indexing
python src/lsi.py --data data/processed/

# Neural IR with mBERT
python src/neural_ir.py --data data/processed/
```

### 4. Evaluate & Visualize
```bash
# Generate evaluation metrics and plots
python src/eval.py \
  --predictions output/ \
  --qrels data/processed/qrels.csv
```
### **5. Launch Interactive Demo**
```bash
# Start Streamlit application
streamlit run app_lsi.py
streamlitt run app_vsm.py
```
---

## 🎥 Demo & Screenshots

<p align="center">
  <a href="https://share.streamlit.io/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"/>
  </a>
</p>

## 📊 Performance Comparison

<img src="https://bers31.github.io/bernardo.github.io/Custom_Search_Engine_With_VSM%26LSI/images/Picture2.png" alt="Performance with VSM" width="800">
<img src="https://bers31.github.io/bernardo.github.io/Custom_Search_Engine_With_VSM%26LSI/images/Picture5.png" alt="Performance with LSI" width="800">

<strong><a href="https://bers31.github.io/bernardo.github.io/Custom_Search_Engine_With_VSM%26LSI/">🎬 Live Demo</a></strong> | <strong><a href="https://github.com/bers31/bernardo.github.io/tree/main/Custom_Search_Engine_With_VSM%26LSI">📁 Explore Code</a></strong>

---

## 📁 Project Structure

```
📦 Information-Retrieval-Benchmark/
├── 📊 data/
│   ├── 🗂️ raw/                     # Original ir_datasets files
│   └── ✨ processed/               # Cleaned CSV/Parquet files
├── 📓 notebooks/
│   ├── 📊 TBI_VSM.ipynb            # VSM pipeline & evaluation
│   ├── 🎯 TBI_LSI.ipynb            # LSI pipeline & evaluation  
│   ├── 🧠 Code_Neural_IR_mBERT.ipynb # mBERT embedding & ranking
│   └── 📈 precision_recall.ipynb   # PR-curve & analysis
├── 🔧 src/
│   ├── ⚙️ etl.py                   # Extract & transform pipeline
│   ├── 📊 vsm.py                   # Vector Space Model functions
│   ├── 🎯 lsi.py                   # Latent Semantic Indexing
│   ├── 🧠 neural_ir.py             # mBERT embedding & ranking
│   └── 📈 eval.py                  # Metrics calculation & plotting
├── 📋 requirements.txt
├── 📖 README.md
└── ⚖️ LICENSE
```

---

## 🔬 Methodology Deep Dive

### 🗃️ Dataset Components
- **Queries**: `(query_id, text)` - Search queries with unique identifiers
- **Documents**: `(doc_id, text)` - Document collection corpus
- **Qrels**: `(query_id, doc_id, relevance)` - Relevance judgments for evaluation

### 🔄 ETL Pipeline
1. **Extract**: Load data using `ir_datasets` API
2. **Transform**: 
   - Remove duplicates and handle missing values
   - Case folding and non-alphanumeric character removal
   - Space normalization and optional tokenization
3. **Load**: Export cleaned DataFrames to processed data directory

### 🎯 IR Methods Implementation

<div align="center">

<table>
<tr>
<th>Method</th>
<th>Approach</th>
<th>Key Technology</th>
</tr>
<tr>
<td><strong>VSM</strong></td>
<td>TF-IDF vectorization with cosine similarity</td>
<td><code>sklearn.TfidfVectorizer</code></td>
</tr>
<tr>
<td><strong>LSI</strong></td>
<td>SVD dimensionality reduction on TF-IDF</td>
<td><code>sklearn.TruncatedSVD</code></td>
</tr>
<tr>
<td><strong>Neural IR</strong></td>
<td>mBERT embeddings with similarity search</td>
<td><code>sentence-transformers</code></td>
</tr>
</table>

</div>

---

## 📊 Evaluation Metrics

- **Precision@k**: Relevant documents in top-k results
- **Recall@k**: Coverage of relevant documents in top-k
- **F1-Score**: Harmonic mean of precision and recall
- **Mean Average Precision (mAP)**: Average precision across all queries
- **Precision-Recall Curves**: Visual performance analysis

---

## 🗺️ Project Scope

This project was developed as a **complete, self-contained academic assignment** for the Information Retrieval course at Universitas Diponegoro. The scope below reflects what was fully implemented and delivered.

| Module | Description | Status |
|--------|-------------|--------|
| ⚙️ **ETL Pipeline** | Data extraction via `ir_datasets`, deduplication, case folding, and text normalization | ✅ Done |
| 📊 **VSM** | TF-IDF vectorization with cosine similarity ranking | ✅ Done |
| 🎯 **LSI** | Truncated SVD dimensionality reduction applied on top of TF-IDF | ✅ Done |
| 🧠 **Neural IR (mBERT)** | Multilingual BERT embeddings with similarity-based ranking | ✅ Done |
| 📈 **Evaluation Framework** | Precision@k, Recall@k, F1-Score, mAP, and Precision-Recall curves | ✅ Done |
| 🖥️ **Streamlit Demo** | Interactive search interface for VSM and LSI via `app_vsm.py` and `app_lsi.py` | ✅ Done |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **💾 Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **📤 Push** to the branch (`git push origin feature/AmazingFeature`)
5. **🔄 Open** a Pull Request

### 🐛 Bug Reports & 💡 Feature Requests
Please use <a href="https://github.com/bers31/bernardo.github.io/issues">GitHub Issues</a> with appropriate labels.

### 👥 Contributors
<div align="center">
<a href="https://github.com/bers31/bernardo.github.io/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=bers31/bernardo.github.io" alt="Contributors">
</a>
</div>

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Bernardo - Universitas Diponegoro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📫 Contact & Connect

<p align="center">
<strong>👨‍💻 Bernardo - Computer Science Student</strong><br/>
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

<p align="center">
⭐ <strong>If you found this project helpful, please give it a star!</strong> ⭐
</p>

<p align="center">
<em>Made with ❤️ by <a href="https://github.com/bers31">Bernardo</a> at Universitas Diponegoro</em><br/>
<img src="https://visitor-badge.laobi.icu/badge?page_id=bers31.bernardo.github.io" alt="Visitor Count">
</p>

---
### Full Screenshots
![Screenshot 1](images/Picture1.png)
![Screenshot 2](images/Picture2.png)
![Screenshot 3](images/Picture3.png)
![Screenshot 4](images/Picture4.png)
![Screenshot 5](images/Picture5.png)
![Screenshot 6](images/Picture6.png)

### Conclusion
This project demonstrates the effectiveness of combining VSM and LSI to create a powerful search engine that delivers highly relevant search results. By leveraging Python and Streamlit, the project provides an intuitive and interactive user experience. The use of LSI significantly enhances search accuracy, making this search engine a valuable tool for finding information efficiently.
