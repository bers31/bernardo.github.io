# 🤖 Neural Information Retrieval (IR) Based on mBERT
### 🔍 *Multilingual document retrieval powered by transformer embeddings and advanced ranking algorithms*

---

<div align="center">

<img src="https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge" alt="Build Status"/>
<img src="https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python" alt="Python Version"/>
<img src="https://img.shields.io/badge/license-MIT-orange.svg?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/badge/model-mBERT-red.svg?style=for-the-badge&logo=tensorflow" alt="mBERT"/>
<img src="https://img.shields.io/badge/demo-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit" alt="Streamlit"/>

</div>

---

## 📖 Project Overview

<div align="center">
<img src="https://img.shields.io/badge/Status-Active%20Development-success?style=flat-square" alt="Status"/>
<img src="https://img.shields.io/badge/Type-Research%20Project-informational?style=flat-square" alt="Type"/>
<img src="https://img.shields.io/badge/Domain-Information%20Retrieval-purple?style=flat-square" alt="Domain"/>
</div>

### 🎯 **Background & Motivation**

Traditional Information Retrieval (IR) systems rely heavily on statistical methods like **BM25** and **TF-IDF**. While effective, these approaches often struggle with semantic understanding and multilingual contexts. 

This project leverages the power of **mBERT (Multilingual BERT)** to generate rich, contextual embeddings that significantly enhance search quality across multiple languages. By combining state-of-the-art transformer models with advanced ranking algorithms, we create a robust end-to-end IR pipeline.

### 🌟 **Key Benefits**

- **🌍 Multilingual Support**: Search across languages without retraining
- **🧠 Semantic Understanding**: Context-aware document matching
- **📊 Comprehensive Evaluation**: Multiple ranking algorithms comparison  
- **🔬 Research-Ready**: Modular framework for IR experimentation

---

## ✨ Key Features

| 🚀 **Core Capabilities** | 🛠️ **Advanced Algorithms** |
|---------------------------|----------------------------|
| **End-to-End IR Pipeline** from raw data to evaluation | **Cosine Similarity** (Baseline approach) |
| **Multiple Ranking Methods** comparison framework | **XGBoost** Learning-to-Rank implementation |
| **Transformer-Based Embeddings** using mBERT | **RankNet** Pairwise ranking neural network |
| **Comprehensive Metrics** (Precision, Recall, F1-Score) | **LambdaMART** Advanced ranking algorithm |

---

## 🛠️ Technology Stack

<div align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"/>
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
</div>

### **Core Technologies**

<table>
<thead>
<tr>
<th>Category</th>
<th>Tools & Libraries</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>🐍 Core Language</strong></td>
<td><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/></td>
<td>Main development language</td>
</tr>
<tr>
<td><strong>📊 Data Processing</strong></td>
<td><code>pandas</code> <code>numpy</code></td>
<td>Data manipulation and analysis</td>
</tr>
<tr>
<td><strong>🔍 IR Framework</strong></td>
<td><code>ir_datasets</code></td>
<td>Dataset loading and management</td>
</tr>
<tr>
<td><strong>🤖 ML & Embeddings</strong></td>
<td><code>sentence-transformers</code> <code>scikit-learn</code></td>
<td>Embedding generation and similarity</td>
</tr>
<tr>
<td><strong>🏆 Ranking Models</strong></td>
<td><code>xgboost</code> <code>lightgbm</code></td>
<td>Advanced ranking algorithms</td>
</tr>
<tr>
<td><strong>📈 Visualization</strong></td>
<td><code>streamlit</code> <code>matplotlib</code></td>
<td>Interactive demos and plots</td>
</tr>
<tr>
<td><strong>⚡ Performance</strong></td>
<td><code>numpy</code> vectorization</td>
<td>Optimized computations</td>
</tr>
</tbody>
</table>

---

## 🚀 Installation & Quick Start

### **Prerequisites**
- Python 3.8 or higher
- 8GB+ RAM recommended for embedding generation
- CUDA-capable GPU (optional, for faster processing)

### **1. Clone the Repository**
```bash
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io
```

### **2. Install Dependencies**
```bash
# Create virtual environment (recommended)
python -m venv neural_ir_env
source neural_ir_env/bin/activate  # On Windows: neural_ir_env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### **3. Data Preprocessing & ETL**
```bash
# Run ETL pipeline
python src/etl.py --input raw/ --output processed/
```

### **4. Generate Embeddings**
```bash
# Generate mBERT embeddings for queries and documents
python src/embedding.py
```

### **5. Train & Evaluate Ranking Models**
```bash
# Run all ranking algorithms
python src/ranking_cosine.py
python src/ranking_xgboost.py  
python src/ranking_ranknet.py
python src/ranking_lambdamart.py
```

### **6. Launch Interactive Demo**
```bash
# Start Streamlit application
streamlit run app.py
```

---

## 🎥 Demo & Screenshots


### 🌐 Live Demo
[**► Launch Application**](https://bers31.github.io/bernardo.github.io/Advance_Information_Retrieval_System/)

![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

<details>
<summary><b>📸 Click to view screenshots</b></summary>

<div align="center">

<p><strong>Main Dashboard</strong></p>
<img src="https://bers31.github.io/bernardo.github.io/Advance_Information_Retrieval_System/images/image5.png" alt="Main Dashboard" width="80%"/>

<p><strong>Search Results Comparison</strong></p>
<img src="https://bers31.github.io/bernardo.github.io/Advance_Information_Retrieval_System/images/image1.png" alt="Search Results" width="80%"/>

<p><strong>Performance Metrics Visualization</strong></p>
<img src="https://bers31.github.io/bernardo.github.io/Advance_Information_Retrieval_System/images/image.png" alt="Performance Metrics" width="80%"/>

</div>

</details>

---

## 📊 Project Architecture

The system is organized into five sequential layers, each with a distinct responsibility in the IR pipeline.

**Layer 1 — Data Input**

| Source | Description |
|--------|-------------|
| 📁 Queries Collection | Raw search queries from the Vaswani test collection |
| 📋 Documents Collection | Corpus of documents to be retrieved and ranked |
| 📊 Relevance Judgments (Qrels) | Ground-truth relevance labels for evaluation |

**Layer 2 — ETL Pipeline**

| Step | Operation |
|------|-----------|
| Case Folding | Normalize text to lowercase |
| Deduplication | Remove duplicate entries across corpus |
| Missing Data Handling | Filter and impute incomplete records |
| Text Normalization | Standardize punctuation, whitespace, and encoding |

**Layer 3 — Embedding & Feature Engineering**

| Component | Detail |
|-----------|--------|
| 🤖 mBERT Encoder | `paraphrase-multilingual-mpnet-base-v2` |
| Output Dimensionality | 768-d contextual vectors per query and document |
| Primary Features | Query embeddings, document embeddings, cosine similarity scores |
| Additional Features | Text length ratios, word count statistics, query-document overlap |

**Layer 4 — Ranking Algorithms**

| Algorithm | Type | Description |
|-----------|------|-------------|
| 📏 Cosine Similarity | Baseline | Direct similarity scoring between embeddings |
| 🌳 XGBoost | Learning-to-Rank | Gradient boosted tree ranker |
| 🧠 RankNet | Pairwise Neural | Neural network trained on pairwise preferences |
| 🎯 LambdaMART | Listwise LTR | Advanced gradient boosting with NDCG optimization — **Best: F1 0.817** |

**Layer 5 — Evaluation & Interface**

| Component | Description |
|-----------|-------------|
| 📈 Per-Query Metrics | Precision@K, Recall@K, F1-Score@K |
| 📈 Aggregate Metrics | Mean Average Precision (MAP), Normalized DCG (NDCG) |
| 🖥️ Streamlit Dashboard | Interactive web UI for live search and result visualization |
| 📓 Jupyter Notebooks | Research exploration and development environment |
| 🔧 CLI Tools | `etl.py`, `embedding.py`, `ranking_*.py`, `evaluate.py` |

### System Flow

1. **📁 Data Input** → Vaswani Dataset loaded via `ir_datasets`
2. **🔄 ETL Pipeline** → Data cleaning and preprocessing
3. **🤖 mBERT Encoding** → Generate contextual 768-d embeddings
4. **📊 Feature Engineering** → Cosine similarity scores and auxiliary features
5. **🏆 Ranking Models** → Four algorithms trained and compared
6. **📈 Evaluation** → Precision, Recall, F1-Score, MAP, and NDCG computed

---

## 🗺️ Project Scope

This project was developed as a **complete, self-contained academic assignment** for the Advanced Information Retrieval course at Universitas Diponegoro. The scope below reflects what was fully implemented and delivered.

| Module | Description | Status |
|--------|-------------|--------|
| 🔄 **ETL Pipeline** | Data loading, cleaning, deduplication, and text normalization | ✅ Done |
| 🤖 **mBERT Embedding** | Contextual 768-d vector generation for queries and documents | ✅ Done |
| 📊 **Feature Engineering** | Cosine similarity scores, text length ratios, query-document overlap | ✅ Done |
| 📏 **Cosine Similarity** | Baseline ranking via embedding similarity | ✅ Done |
| 🌳 **XGBoost LTR** | Learning-to-Rank with gradient boosted trees | ✅ Done |
| 🧠 **RankNet** | Pairwise neural ranking model | ✅ Done |
| 🎯 **LambdaMART** | Advanced listwise ranking algorithm (best performer: F1 0.817) | ✅ Done |
| 📈 **Evaluation Engine** | Precision, Recall, F1-Score, MAP, and NDCG metrics | ✅ Done |
| 🖥️ **Streamlit Demo** | Interactive web dashboard for live search and result visualization | ✅ Done |

---

## 📈 Performance Metrics

<div align="center">

<table>
<thead>
<tr>
<th><strong>Algorithm</strong></th>
<th><strong>Avg Precision</strong></th>
<th><strong>Avg Recall</strong></th>
<th><strong>Avg F1-Score</strong></th>
<th><strong>Training Time</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Cosine Similarity</strong></td>
<td>0.742</td>
<td>0.681</td>
<td>0.710</td>
<td>~2 min</td>
</tr>
<tr>
<td><strong>XGBoost</strong></td>
<td>0.798</td>
<td>0.756</td>
<td>0.776</td>
<td>~15 min</td>
</tr>
<tr>
<td><strong>RankNet</strong></td>
<td>0.812</td>
<td>0.773</td>
<td>0.792</td>
<td>~25 min</td>
</tr>
<tr>
<td><strong>LambdaMART</strong></td>
<td><strong>0.834</strong></td>
<td><strong>0.801</strong></td>
<td><strong>0.817</strong></td>
<td>~20 min</td>
</tr>
</tbody>
</table>

</div>

<blockquote>
<p><strong>Note</strong>: Results based on Vaswani test collection. Performance may vary with different datasets.</p>
</blockquote>

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

<details>
<summary><b>🛠️ Development Guidelines</b></summary>

### **Getting Started**
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add some amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Code Standards**
- Follow **PEP 8** Python style guidelines
- Add **docstrings** to all functions and classes
- Include **unit tests** for new features
- Update **documentation** as needed

### **Areas for Contribution**
- 🐛 **Bug fixes** and performance improvements
- 📊 **New ranking algorithms** implementation
- 🌍 **Additional language support**
- 📚 **Documentation** enhancements
- 🧪 **Test coverage** expansion

</details>

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
![Screenshot 1](images/image.png)
![Screenshot 2](images/image1.png)
![Screenshot 3](images/image2.png)
![Screenshot 4](images/image3.png)
![Screenshot 5](images/image4.png)
![Screenshot 6](images/image5.png)

### Conclusion
This project demonstrates the implementation of a modern Information Retrieval system that combines deep learning and machine learning techniques to deliver more accurate and relevant search results compared to traditional keyword-based approaches.
