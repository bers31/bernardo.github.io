<div align="center">
  <h1>📊 Data Analysis Dashboard</h1>
  <p><em>Transform Excel Analytics into Interactive Intelligence</em></p>

  <p>
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
    <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
    <img src="https://img.shields.io/badge/version-1.0.0-orange" alt="Version">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white" alt="Pandas">
    <img src="https://img.shields.io/badge/Excel-217346?logo=microsoft-excel&logoColor=white" alt="Excel">
  </p>
</div>

---

## 📖 About This Project

This project consolidates multiple Excel workbook analyses into a **unified, structured data analysis pipeline** with role-based data segmentation. Born from the need to transform static Excel reports into clean, reproducible insights, this project serves as a comprehensive solution for data cleaning, exploratory analysis, and business intelligence visualization — all built on top of Microsoft Excel as the primary data source and delivery format.

**Why This Matters:** Raw Excel data is rarely analysis-ready. This project establishes a disciplined ETL workflow that extracts data from Excel workbooks, cleans and transforms it using Python, and delivers actionable insights through well-structured visualizations and summary reports — bridging the gap between spreadsheet data and meaningful decision support.

---

## ✨ Key Features

- 📥 **Excel-Driven Data Ingestion** — Reads directly from `.xlsx` workbooks using `openpyxl` and `pandas`
- 🧹 **Automated ETL Pipeline** — Handles missing values, type normalization, deduplication, and column standardization
- 📊 **Multi-Dataset Integration** — Unified analysis across Sales, Customer Segmentation, and Accident Report datasets
- 🎯 **Role-Based Data Views** — Separate analysis outputs tailored for Admin, Student, Lecturer, Department Head, and Dean perspectives
- 📈 **Rich Visualizations** — Charts, heatmaps, and summary dashboards generated with Matplotlib and Seaborn
- 📋 **Export-Ready Outputs** — Cleaned datasets and visual reports exported back to Excel or PDF for stakeholder distribution

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Primary Data Format** | Microsoft Excel (`.xlsx`) |
| **Language** | Python 3.8+ |
| **Data Processing** | Pandas, NumPy, openpyxl |
| **Visualization** | Matplotlib, Seaborn |
| **Development Environment** | Jupyter Notebook |
| **Export** | openpyxl (Excel), Matplotlib (PDF/PNG) |

---

## 🚀 Quick Start Guide

### Prerequisites
```bash
Python >= 3.8
pip package manager
Microsoft Excel (for viewing source files and outputs)
```

### Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io/Data_Analysis_Excel

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter Notebook
jupyter notebook
```

### Core Dependencies

```txt
pandas>=1.3.0
numpy>=1.21.0
openpyxl>=3.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
jupyter>=1.0.0
```

### Running the Analysis

Open the notebooks in the following sequence:

```bash
# Step 1 – Data cleaning and ETL
jupyter notebook notebooks/01_etl_cleaning.ipynb

# Step 2 – Exploratory data analysis per dataset
jupyter notebook notebooks/02_sales_analysis.ipynb
jupyter notebook notebooks/03_customer_segmentation.ipynb
jupyter notebook notebooks/04_accident_report.ipynb

# Step 3 – Role-based summary reports
jupyter notebook notebooks/05_role_based_views.ipynb
```

---

## 🎥 Demo & Screenshots

**[👁 View Demo →](https://bers31.github.io/bernardo.github.io/Data_Analysis_Excel/)**

<div align="center">
  <img src="https://bers31.github.io/bernardo.github.io/Data_Analysis_Excel/images/Picture7.png"
       alt="Dashboard Preview"
       style="max-width: 100%; height: auto; border-radius: 8px;" />
</div>

---

## 🗃️ Data Sources

| Dataset | Records | Key Metrics | Analysis Focus |
|---------|---------|-------------|----------------|
| **Sales Data** | 112,036 rows | Revenue, Profit, Quantity | Time-series trends, regional performance |
| **Customer Segmentation** | 1,026 rows | Demographics, Purchase behaviour | Buyer personas, conversion analysis |
| **Accident Reports** | Variable | Location, Severity, Time | Safety analytics, trend identification |

All datasets originate from `.xlsx` source files and are processed entirely within the Python/Pandas pipeline before results are written back to structured Excel output files.

---

## 📁 Project Structure

```
Data_Analysis_Excel/
│
├── 📂 data/
│   ├── raw/                    # Original Excel workbooks (.xlsx)
│   └── processed/              # Cleaned and transformed datasets
│
├── 📂 notebooks/
│   ├── 01_etl_cleaning.ipynb
│   ├── 02_sales_analysis.ipynb
│   ├── 03_customer_segmentation.ipynb
│   ├── 04_accident_report.ipynb
│   └── 05_role_based_views.ipynb
│
├── 📂 outputs/
│   ├── figures/                # Exported charts and visualizations
│   └── reports/                # Summary Excel and PDF outputs
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🗺️ Project Scope

This project was developed as a **complete, self-contained academic assignment** for the Data Warehouse and Business Intelligence course at Universitas Diponegoro. The scope below reflects what was fully implemented and delivered.

| Module | Description | Status |
|--------|-------------|--------|
| 🗄️ **ETL Pipeline** | Excel ingestion, missing value handling, type normalization, and deduplication using Pandas and openpyxl | ✅ Done |
| 📊 **Sales Analysis** | Revenue, profit, and quantity trend analysis with regional and time-series breakdowns | ✅ Done |
| 👥 **Customer Segmentation** | Demographic and purchase behaviour analysis for buyer persona insights | ✅ Done |
| 🚨 **Accident Report Analysis** | Location, severity, and temporal trend analysis for safety insights | ✅ Done |
| 🎯 **Role-Based Views** | Separate summary outputs tailored for Admin, Student, Lecturer, Department Head, and Dean | ✅ Done |
| 📋 **Export & Reporting** | Cleaned datasets and visual reports exported to Excel and PDF | ✅ Done |
| 📈 **Visualization Suite** | Charts, heatmaps, and distribution plots generated with Matplotlib and Seaborn | ✅ Done |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

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

---

### Full Screenshots
![Screenshot 1](images/Picture7.png)
![Screenshot 2](images/Picture8.png)
![Screenshot 3](images/Picture9.png)
![Screenshot 4](images/Picture10.png)

---

## 📫 Contact & Connect

<p align="center">
<strong>👨‍💻 Bernardo Nandaniar Sunia — Computer Science Graduate</strong><br/>
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
