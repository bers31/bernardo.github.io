<div align="center">
  <h1>🏘️ Property Data Analysis & Investment Intelligence Platform</h1>
  <h3>Operational & Analytical Data Schemas · Macroeconomic Indicator Integration · Investment Decision Workflow</h3>

  <br/>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/Deployment-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
  <img src="https://img.shields.io/badge/Export-CSV-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" alt="CSV Export">
  <img src="https://img.shields.io/badge/Status-Production-22C55E?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Project-Client%20%2F%20Confidential-1D4ED8?style=for-the-badge" alt="Client Project">

  <br/><br/>

  <sub>Part of my <a href="https://bers31.github.io/bernardo.github.io/">Data Analyst portfolio</a></sub>
</div>

---

## 📖 Project Overview

The data backbone for property investment analysis: a structured database and role-based frontend that lets an analyst move from national macroeconomic indicators all the way down to individual listing evaluation. The database is deliberately split into two schemas by update frequency, keeping fast-changing market data separate from slow-moving economic indicators.

---

## 🗄️ Data Architecture

### Operational Schema *(frequently updated)*

| Metric | Purpose |
|--------|---------|
| Average price, land area, building area | Baseline "fair price" benchmark for a given area |
| Active listing count | Proxy for market liquidity: more listings, easier to find comparables and sell |
| Land/building area mode | Most common property profile in the market |
| Min–max price range | Reveals entry-level vs. upgrade segmentation, and flags mispriced listings |
| Property type (vacant land vs. built) | Signals capital-gain-only positioning vs. rentable cash-flow positioning |
| Price trend (by price mode, not mean) | Reflects the area's actual "busy point" for price negotiation, unskewed by outliers |
| Price fluctuation | High = heterogeneous/transitional area (higher risk, higher upside); Low = mature, stable market (lower risk, lower upside) |

### Analytical Schema *(infrequently updated)*

| Indicator | Purpose |
|-----------|---------|
| **IHPR** (Residential Property Price Index) | Bank Indonesia's quarterly national house price index, overall trend direction |
| **Inflation** | Used to compute *real* return (e.g. 5% nominal price growth − 4% inflation = 1% real gain) |
| **UMR** (Regional Minimum Wage) | Rough proxy for local purchasing power, feeds into PIR |
| **Population census** | Estimates the future pool of buyers/renters |
| **BI Rate** | Bank Indonesia's benchmark rate, drives mortgage cost |
| **GDP growth** | Broad economic health indicator correlated with housing demand |
| **PIR** (Price-to-Income Ratio) | A high and fast-rising PIR can signal overpricing relative to local income, though a high but *stable* PIR in an affluent, high-demand area doesn't necessarily mean a bubble |

---

## 🖥️ Frontend & Access Control

A role-separated frontend supports:

- **Admin role**: full CRUD access to the underlying database
- **User role**: read-only access with category filters and full-table **.csv** export

---

## 🧭 Investment Analysis Workflow

The end-to-end flow this platform is designed to support:

`Macro check (IHPR, BI Rate, inflation, GDP, census, UMR, PIR)` → `Province/city comparison` → `Area drill-down` → `PIR / price-to-UMR check` → `Listing evaluation vs. area average & trend` → `Decision: buy, negotiate, wait, or pass`

---

## 💡 Cross-Indicator Insights

| Insight | Signal |
|---------|--------|
| **Population growth × housing supply** | Fast in-migration paired with relatively low local housing supply signals demand outpacing supply, a likely driver of future price increases |
| **BI Rate × property type** | In a rising-rate environment, rentable built property is relatively safer than vacant land, since rental cash flow helps offset mortgage interest cost |
| **GDP/GRDP × city-level price trend** | A city growing faster than the national average, whose property prices haven't risen proportionally, is a strong candidate for an area **"not yet priced in"** by the market |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Database Design** | Dual-schema (operational + analytical) relational structure |
| **Backend** | Role-based CRUD API |
| **Frontend** | Web-based dashboard with filtering & CSV export |
| **External Data Integration** | Bank Indonesia (IHPR, BI Rate), national census/regional UMR data |
| **Deployment** | Railway |

---

## 🚀 Deployment & Access

The platform is deployed and used in production to support investment analysis workflows. Live dashboard access is kept private, as it reflects proprietary investment methodology and business data.

---

## 🔬 Outcomes

- Designed a schema split that keeps fast-moving market data and slow-moving macro indicators cleanly separated, simplifying refresh logic and query performance.
- Operationalized abstract macroeconomic indicators (IHPR, PIR, BI Rate) into a concrete, repeatable **investment decision workflow**.
- Surfaced cross-indicator insights, such as population growth versus housing supply, that aren't visible from any single metric in isolation.

---

## 📄 Project Ownership

This project was developed during my tenure as **Data Analyst at PT Wiraky Nusa Telekomunikasi**. It is documented here as a professional portfolio case study; the underlying database and production platform remain the property of PT Wiraky Nusa Telekomunikasi.

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
