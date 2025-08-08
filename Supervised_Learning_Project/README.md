# Customer Segmentation — Supervised Multi-Class Classification
### *Intelligent customer profiling through advanced machine learning techniques*

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)

</div>

---

## 📖 **Project Description**

This project implements a **supervised learning** approach for **customer segmentation** using multi-class classification techniques. Built as an academic project at Universitas Diponegoro, it leverages the Kaggle dataset `abisheksudarshan/customer-segmentation` to predict customer segments based on demographic and behavioral features.

The solution addresses the critical business challenge of understanding customer behavior patterns, enabling companies to:
- **Optimize marketing strategies** through targeted campaigns
- **Improve customer retention** with personalized experiences  
- **Enhance resource allocation** based on segment characteristics
- **Drive revenue growth** through data-driven decision making

---

## ✨ **Key Features**

<table>
<tr>
<td width="50%">

### 🎯 **Machine Learning Models**
- K-Nearest Neighbors (KNN)
- Random Forest Classifier
- Support Vector Machine (SVM)
- XGBoost Classifier
- Logistic Regression

</td>
<td width="50%">

### 🔧 **Advanced Processing**
- Comprehensive ETL pipeline
- Feature engineering & scaling
- Hyperparameter optimization
- Cross-validation techniques
- PCA dimensionality reduction

</td>
</tr>
</table>

- **📊 Balanced Dataset Handling**: Stratified sampling with 500 samples per class
- **🎨 Rich Visualizations**: Interactive EDA with confusion matrices and feature importance plots
- **⚡ Pipeline Architecture**: Automated preprocessing with scikit-learn pipelines
- **🔍 Model Interpretability**: Feature importance analysis for business insights
- **📈 Comprehensive Evaluation**: Multi-metric assessment (Accuracy, Precision, Recall, F1-score)

---

## 🛠️ **Technologies & Tools**

<div align="center">

| **Category** | **Technologies** |
|:---:|:---:|
| **Programming** | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> |
| **Machine Learning** | <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn"> <img src="https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white" alt="XGBoost"> |
| **Data Analysis** | <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"> <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"> |
| **Visualization** | <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge" alt="Matplotlib"> <img src="https://img.shields.io/badge/seaborn-9cf?style=for-the-badge" alt="Seaborn"> |
| **Development** | <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter"> <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" alt="Kaggle"> |

</div>

---

## 🚀 **Installation & Quick Start**

### **Prerequisites**
```bash
Python >= 3.8
pip or conda package manager
```

### **Setup Instructions**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bers31/bernardo.github.io.git
   cd bernardo.github.io
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Dataset**
   ```bash
   # The dataset will be automatically downloaded via kagglehub in the notebook
   # Or manually place CSV files in data/raw/ directory
   ```

5. **Run the Analysis**
   ```bash
   # Start Jupyter Notebook
   jupyter notebook
   
   # Run notebooks in sequence:
   # 1. KNN, Random_Forest, SVM.ipynb
   # 2. XGBoost, Logistic_Regression.ipynb
   ```

### **Dependencies (requirements.txt)**
```txt
python>=3.8
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
matplotlib>=3.5.0
seaborn>=0.11.0
kagglehub>=0.1.0
joblib>=1.1.0
nbformat>=5.4.0
```

---

## 🎥 **Demo & Screenshots**

<div align="center">

### **Project Architecture**
```
┌─────────────────────────────────────────────────────────┐
│                    DATA PIPELINE                        │
├─────────────────────────────────────────────────────────┤
│  📥 Data Loading    │  🧹 Data Cleaning  │  🔧 Feature   │
│  (Kaggle API)       │  (ETL Process)      │  Engineering  │
└─────────────────────┴─────────────────────┴─────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 MACHINE LEARNING MODELS                 │
├─────────────────────────────────────────────────────────┤
│  🎯 KNN         │  🌲 Random Forest  │  ⚡ XGBoost     │
│  🔍 SVM         │  📈 Logistic Reg   │  🎛️ Tuning     │
└─────────────────┴────────────────────┴─────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                    EVALUATION                           │
├─────────────────────────────────────────────────────────┤
│  📊 Metrics     │  🎨 Visualizations │  📋 Reports     │
│  📈 Validation  │  🔍 Interpretability│  💾 Artifacts  │
└─────────────────┴────────────────────┴─────────────────┘
```

### **Sample Visualization**
*Confusion Matrix and Feature Importance plots are generated automatically*

![Demo Placeholder](https://via.placeholder.com/800x400/2E3440/81A1C1?text=Customer+Segmentation+Results)

**🔗 [View Live Demo](https://bers31.github.io/bernardo.github.io/)**

</div>

---

## 📊 **Project Roadmap**

<div align="center">

| **Milestone** | **Target Date** | **Status** | **Description** |
|:---:|:---:|:---:|:---|
| 🔍 **Data Exploration** | Week 1 | ✅ Complete | Initial EDA and data understanding |
| 🧹 **Data Preprocessing** | Week 2 | ✅ Complete | ETL pipeline and feature engineering |
| 🤖 **Model Development** | Week 3 | ✅ Complete | Implementation of 5 ML algorithms |
| ⚙️ **Hyperparameter Tuning** | Week 4 | ✅ Complete | Grid search optimization |
| 📈 **Model Evaluation** | Week 5 | ✅ Complete | Comprehensive performance analysis |
| 📝 **Documentation** | Week 6 | ✅ Complete | README and code documentation |

</div>

---

## 🤝 **Contributing**

We welcome contributions from the community! Here's how you can help:

### **Ways to Contribute**
- 🐛 **Bug Reports**: Found an issue? Create a detailed bug report
- ✨ **Feature Requests**: Suggest new features or improvements  
- 📖 **Documentation**: Help improve our documentation
- 🧪 **Testing**: Add test cases or improve existing ones
- 🎨 **Visualizations**: Enhance charts and plots

### **Contribution Guidelines**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Development Setup**
```bash
# Clone your fork
git clone https://github.com/your-username/bernardo.github.io.git

# Add upstream remote
git remote add upstream https://github.com/bers31/bernardo.github.io.git

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

---

## 📄 **License**

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Bernardo
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

</div>

---

## 📫 **Contact & Connect**

<div align="center">

### **Get in Touch**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@example.com)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/bers31)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://bers31.github.io/bernardo.github.io/)

---

### **About the Developer**
🎓 **Computer Science Student** at Universitas Diponegoro  
🔬 **Specializing in**: Machine Learning, Data Science, and Web Development  
🌟 **Passionate about**: Creating innovative solutions through technology

---

<img src="https://komarev.com/ghpvc/?username=bers31&color=brightgreen&style=flat-square" alt="Profile Views">

**⭐ If you found this project helpful, please give it a star!**

</div>

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/bers31">Bernardo</a> • Universitas Diponegoro • 2025</sub>
</div>

### Screenshots
![Screenshot 1](images/image.png)
![Screenshot 2](images/image1.png)
![Screenshot 3](images/image2.png)
![Screenshot 4](images/image3.png)
![Screenshot 5](images/image4.png)
![Screenshot 6](images/image5.png)

### Conclusion
This project highlights the application of advanced supervised learning techniques for effective customer segmentation. By leveraging algorithms such as k-NN, Random Forest, SVM, XGBoost, and Logistic Regression, we have successfully demonstrated how machine learning can provide actionable insights into customer behavior. The results from this project can help businesses design more targeted marketing strategies, enhance customer engagement, and optimize resource allocation. Furthermore, the outlined future work presents opportunities for improving the system with cutting-edge technologies and real-time capabilities, ensuring scalability and adaptability in dynamic business environments.
