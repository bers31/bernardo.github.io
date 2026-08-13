<div align="center">
  <h1>📋 Maribaya Visitor Review System: First-Party Feedback Collection & Anomaly Detection</h1>
  <h3>Token-Secured Forms · Multi-Signal Anomaly Scoring · Real-Time Visualization Dashboards</h3>

  <br/>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Security-Token%20Based-DC2626?style=for-the-badge" alt="Token Security">
  <img src="https://img.shields.io/badge/Deployment-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
  <img src="https://img.shields.io/badge/Export-CSV-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" alt="CSV Export">
  <img src="https://img.shields.io/badge/Status-Production-22C55E?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Project-Client%20%2F%20Confidential-1D4ED8?style=for-the-badge" alt="Client Project">

  <br/><br/>

  <sub>Part of my <a href="https://bers31.github.io/bernardo.github.io/">Data Analyst portfolio</a></sub>
</div>

---

## 📖 Project Overview

A **first-party visitor review system** built to collect guest feedback separately for Maribaya Resort and Maribaya Glamping. The form is kept short enough that visitors actually complete it, while still capturing the fields needed for downstream analysis. It's paired with a rule-based **anomaly detection engine** that flags suspicious or spam-like review patterns before they distort the business's rating data.

> **Core problem it solves:** open review links are easy to spam or fabricate. Rather than relying on manual moderation alone, every incoming review is scored against multiple behavioral signals and classified into a confidence tier, so the team can focus moderation effort where it actually matters.

---

## 🔐 Form Access & Validation

| Mechanism | Detail |
|-----------|--------|
| **Token-based access** | Every review link is generated with a unique, system-issued token, so the form cannot be reached without it |
| **15-minute token expiry** | Matched to the typical time a visitor needs to complete the review, limiting the window for link reuse or sharing |
| **Optional fields** | Food & beverage rating, email, and written review are optional, to accommodate visitors who didn't purchase food, or who prefer not to share contact details or write a comment |

---

## 🚨 Anomaly Detection Engine

Four behavioral signals are combined to flag potentially anomalous or spam reviews:

| Signal | Description | Strength |
|--------|--------------|----------|
| **Repeated identity** | Same name, age, and city submitted again within a 15-minute window, which suggests cached browser data reused for spam | Strong when combined with another signal |
| **Review text similarity** | Generic phrases (e.g. *"bagus"*, *"recommended banget"*) repeating across submissions | Weak alone; only checkable when the review field is filled in |
| **Rating pattern similarity** | Similar rating combinations across different submissions | Weak alone; plausible even among genuine reviewers |
| **Off-hours submission** *(Maribaya only)* | Review submitted outside operating hours (08:00–17:00) | Strong on its own, treated as an absolute signal |

**Anomaly Tiers**

| Tier | Trigger Condition |
|------|--------------------|
| 🔴 **Strong** | Off-hours submission (absolute), or repeated identity combined with text or rating similarity on the same review pair |
| 🟠 **Medium** | Repeated identity alone, or combined rating + text similarity across different identities *(still under discussion whether this belongs here or in Low)* |
| 🟡 **Low** | Rating similarity alone, or text similarity alone |

---

## 📊 Visualization Dashboards

Two role-separated dashboards let the team filter and visualize collected reviews, view aggregate statistics, and export the full dataset to **.csv**:

- Maribaya Resort review dashboard
- Maribaya Glamping Tent review dashboard

---

## 💡 Strategic Recommendation: Collection Method

Beyond the system itself, I evaluated collection methods against a simple QR code link, which is free but carries higher spam risk if the link circulates outside intended channels, and compared paid on-site device options:

| Device Option | Cost | Trade-off | Verdict |
|----------------|------|-----------|---------|
| Tablet + Kiosk Mode | Low | Simple, easy to configure, less durable for 24/7 use | Cheapest, easiest maintenance |
| Android POS Terminal | Medium | Better display, durable for 24/7 use, moderate maintenance | **Recommended**, best stability-to-cost balance |
| Industrial Touchscreen Kiosk | High | Professional look, durable, harder maintenance | Rugged, long-lasting |
| Floor-Standing Kiosk | High | Most eye-catching, durable, harder maintenance | Strongest branding, best for high-traffic spots |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend Logic** | Python, token generation & expiry handling |
| **Anomaly Scoring** | Rule-based multi-signal classifier |
| **Dashboard & Visualization** | Web-based filterable dashboard with CSV export |
| **Deployment** | Railway |

---

## 🚀 Deployment & Access

Both dashboards are deployed and actively used to monitor incoming reviews in production. Live dashboard access is kept private to protect visitor data and Maribaya's operational review data.

---

## 🔬 Outcomes

- Replaced an open, unsecured feedback link with a **token-gated, time-limited** submission flow.
- Reduced reliance on manual review moderation through a **tiered, multi-signal anomaly scoring system**.
- Delivered actionable device-investment guidance, balancing cost against durability and spam-resistance for on-site data collection.

---

## 📄 Project Ownership

This project was developed during my tenure as **Data Analyst at PT Wiraky Nusa Telekomunikasi** for the Maribaya property. It is documented here as a professional portfolio case study; the source code and production environment remain the property of PT Wiraky Nusa Telekomunikasi / Maribaya.

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
