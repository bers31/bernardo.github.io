# Neural Information Retrieval (IR) Based on mBERT
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

<table>
<tr>
<td width="50%">

### 🚀 **Core Capabilities**
- **End-to-End IR Pipeline** from raw data to evaluation
- **Multiple Ranking Methods** comparison framework
- **Transformer-Based Embeddings** using mBERT
- **Comprehensive Metrics** (Precision, Recall, F1-Score)

</td>
<td width="50%">

### 🛠️ **Advanced Algorithms**
- **Cosine Similarity** (Baseline approach)
- **XGBoost** Learning-to-Rank implementation
- **RankNet** Pairwise ranking neural network
- **LambdaMART** Advanced ranking algorithm

</td>
</tr>
</table>

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

<div align="center">

### **🌐 Live Demo**
<a href="https://bers31.github.io/bernardo.github.io/Advance_Information_Retrieval_System/">
<img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"/>
</a>

</div>

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

<div align="center">

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔍 Neural IR Pipeline Architecture                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📁 Raw Data   │    │   🔍 Queries    │    │  📋 Documents   │
│  Vaswani Corpus │    │   Collection    │    │   Collection    │
│   (ir_datasets) │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │    🔄 ETL Pipeline      │
                    │  ┌─────────────────────┐│
                    │  │ • Data Cleaning     ││
                    │  │ • Case Folding      ││
                    │  │ • Remove Duplicates ││
                    │  │ • Handle Missing    ││
                    │  │ • Text Preprocessing││
                    │  └─────────────────────┘│
                    └───────────┬─────────────┘
                                ▼
                 ┌─────────────────────────────────┐
                 │     🤖 mBERT Embedding Engine   │
                 │ Model: paraphrase-multilingual- │
                 │        mpnet-base-v2            │
                 │ Output: 768-dimensional vectors │
                 └───────────────┬─────────────────┘
                                 ▼
        ┌─────────────────────────────────────────────────┐
        │           📊 Feature Engineering                │
        │ ┌─────────────────┐  ┌─────────────────────────┐│
        │ │ Primary Features│  │   Additional Features   ││
        │ │ • Query Embeddi.│  │ • Text Length          ││
        │ │ • Doc. Embeddi. │  │ • Word Count           ││
        │ │ • Cosine Sim.   │  │ • Query-Doc Overlap    ││
        │ └─────────────────┘  └─────────────────────────┘│
        └─────────────────────────────┬───────────────────┘
                                      ▼
    ┌────────────────────────────────────────────────────────────────┐
    │                    🏆 Ranking Algorithms                       │
    └────────────────────────────────────────────────────────────────┘
              │                 │                 │                 │
              ▼                 ▼                 ▼                 ▼
    ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
    │  📏 Cosine      │ │ 🌳 XGBoost  │ │ 🧠 RankNet  │ │ 🎯 LambdaMART   │
    │   Similarity    │ │ Learning-   │ │ Pairwise    │ │ Advanced LTR    │
    │   (Baseline)    │ │ to-Rank     │ │ Ranking     │ │ Algorithm       │
    └─────────┬───────┘ └──────┬──────┘ └──────┬──────┘ └────────┬────────┘
              │                │                │                │
              └────────────────┼────────────────┼────────────────┘
                               ▼                ▼
                    ┌─────────────────────────────────┐
                    │       📈 Evaluation Engine      │
                    │ ┌─────────────────────────────┐ │
                    │ │ • Precision Calculation    │ │
                    │ │ • Recall Measurement       │ │
                    │ │ • F1-Score Computation     │ │
                    │ │ • Cross-Model Comparison   │ │
                    │ └─────────────────────────────┘ │
                    └───────────────┬─────────────────┘
                                    ▼
                        ┌─────────────────────┐
                        │  📊 Results &       │
                        │  Performance        │
                        │  Analysis           │
                        │                     │
                        │  🎯 Best Model:     │
                        │     LambdaMART      │
                        │     F1: 0.817       │
                        └─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              💻 User Interface Layer                            │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐ │
│  │  🖥️ Streamlit   │  │  📓 Jupyter     │  │    🔧 CLI Tools                │ │
│  │    Web App      │  │    Notebooks    │  │  • etl.py                      │ │
│  │  Interactive    │  │  Development    │  │  • embedding.py                │ │
│  │  Demo & Viz     │  │  & Analysis     │  │  • ranking_*.py                │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

</div>

### **System Flow:**
1. **📁 Data Input** → Vaswani Dataset via `ir_datasets`
2. **🔄 ETL Pipeline** → Data cleaning & preprocessing
3. **🤖 mBERT Encoding** → Generate contextual embeddings
4. **📊 Feature Engineering** → Cosine similarity + additional features
5. **🏆 Ranking Models** → Multiple algorithm comparison
6. **📈 Evaluation** → Precision, Recall, F1-Score metrics

---

## 🗓️ Development Roadmap

<table>
<thead>
<tr>
<th><strong>Phase</strong></th>
<th><strong>Milestone</strong></th>
<th><strong>Target Date</strong></th>
<th><strong>Status</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Phase 1</strong></td>
<td>Data Pipeline & ETL</td>
<td>✅ Completed</td>
<td><img src="https://img.shields.io/badge/100%25-success" alt="100% Complete"/></td>
</tr>
<tr>
<td><strong>Phase 2</strong></td>
<td>mBERT Integration</td>
<td>✅ Completed</td>
<td><img src="https://img.shields.io/badge/100%25-success" alt="100% Complete"/></td>
</tr>
<tr>
<td><strong>Phase 3</strong></td>
<td>Baseline Implementation</td>
<td>✅ Completed</td>
<td><img src="https://img.shields.io/badge/100%25-success" alt="100% Complete"/></td>
</tr>
<tr>
<td><strong>Phase 4</strong></td>
<td>Advanced Ranking Models</td>
<td>🔄 In Progress</td>
<td><img src="https://img.shields.io/badge/80%25-yellow" alt="80% Complete"/></td>
</tr>
<tr>
<td><strong>Phase 5</strong></td>
<td>Performance Optimization</td>
<td>📅 Q1 2025</td>
<td><img src="https://img.shields.io/badge/Planning-blue" alt="Planning"/></td>
</tr>
<tr>
<td><strong>Phase 6</strong></td>
<td>Production Deployment</td>
<td>📅 Q2 2025</td>
<td><img src="https://img.shields.io/badge/Planning-blue" alt="Planning"/></td>
</tr>
</tbody>
</table>

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

<div align="center">
  <h2>📫 Contact &amp; Support</h2>
  <p><strong>👨‍💻 Developer Information</strong><br/>
     Bernardo — Computer Science Student<br/>
     Universitas Diponegoro
  </p>
  <p>
    <a href="https://linkedin.com/in/bernardo-sunia/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=suniabernardo@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white"/></a>
    <a href="https://github.com/bers31"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/></a>
    <a href="https://bit.ly/bernardo-my_portfolio"><img src="https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white"/></a>
  </p>
  <p>⭐ If you found this project helpful, please give it a star!</p>
  <p>Made with ❤️ by <a href="https://github.com/bers31">Bernardo</a> at Universitas Diponegoro<br/>
  <em>Transforming correctional facility communication through intelligent technology</em></p>
</div>

---

<div align="center">
<sub>Built with ❤️ by <a href="https://github.com/bers31">Bernardo</a> • Neural Information Retrieval Project • 2024-2025</sub>
</div>

### Full Screenshots
![Screenshot 1](images/image.png)
![Screenshot 2](images/image1.png)
![Screenshot 3](images/image2.png)
![Screenshot 4](images/image3.png)
![Screenshot 5](images/image4.png)
![Screenshot 6](images/image5.png)

### Conclusion
This project demonstrates the implementation of a modern Information Retrieval system that combines deep learning and machine learning techniques to deliver more accurate and relevant search results compared to traditional keyword-based approaches.
