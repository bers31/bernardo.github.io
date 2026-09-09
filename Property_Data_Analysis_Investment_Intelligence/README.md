<div class="hero">

<h1>🏘️ Property Data Analysis & Investment Intelligence Platform</h1>

<p>Real-Estate Analytics · Macroeconomic Intelligence · Market Evaluation · Investment Decision Support</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Data%20Visualization-6D28D9?style=flat-square" alt="Data Visualization"/>
  <img src="https://img.shields.io/badge/Statistical%20Analysis-8B5CF6?style=flat-square" alt="Statistical Analysis"/>
  <img src="https://img.shields.io/badge/Dashboard-F59E0B?style=flat-square" alt="Dashboard"/>
  <img src="https://img.shields.io/badge/CSV-217346?style=flat-square&logo=microsoft-excel&logoColor=white" alt="CSV Export"/>
  <img src="https://img.shields.io/badge/Web%20Application-1D4ED8?style=flat-square" alt="Web Application"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="MIT License"/>
</p>

<p>
A property market analytics platform that combines real-estate listing data
with macroeconomic indicators to support structured market evaluation and
investment decision-making.
</p>

</div>

---

## 📖 Project Overview

The **Property Data Analysis & Investment Intelligence Platform** is a data-driven property market analytics system designed to help analysts evaluate real-estate markets from both **micro-level listing characteristics** and **macro-level economic conditions**.

The platform combines:

* Property listing data.
* Market structure indicators.
* Price and size analysis.
* Supply-related signals.
* Macroeconomic indicators.
* Affordability metrics.
* Regional comparisons.
* Area-level benchmarking.
* Interactive data exploration.
* CSV-based downstream analysis.

The goal is not simply to display property listings, but to create a structured analytical workflow that transforms heterogeneous market data into an investment-oriented decision process.

```text id="7m4q2x"
Property Listings
       +
Macroeconomic Indicators
       ↓
Data Structuring
       ↓
Market Analysis
       ↓
Regional Comparison
       ↓
Area-Level Evaluation
       ↓
Price Benchmarking
       ↓
Investment Decision
```

> **Portfolio focus:** This project demonstrates how data analysis can connect operational property data with broader economic indicators to support structured and repeatable investment evaluation.

---

## 🎯 Business Objective

Property investment decisions are rarely determined by a listing's asking price alone.

An attractive property may become less attractive when considered alongside:

* Local affordability.
* Interest rates.
* Population growth.
* Housing supply.
* Regional economic growth.
* Historical price movement.
* Market volatility.

The platform therefore combines multiple analytical dimensions:

```text id="c8p5m2"
Property-Level Data
        +
Area-Level Market Data
        +
Macroeconomic Conditions
        ↓
Structured Investment Analysis
```

This allows an analyst to move from **“Is this property cheap?”** toward the more useful question:

> **“Is this property attractively priced relative to its market, affordability conditions, supply-demand environment, and broader economic context?”**

---

## 🗄️ Data Architecture

The system separates data into two logical structures according to how frequently the information changes.

### ⚡ Operational Data Structure

The operational layer contains frequently changing property-market information.

Typical metrics include:

| Metric                   | Analytical Purpose                                         |
| ------------------------ | ---------------------------------------------------------- |
| **Average price**        | Baseline market-price benchmark                            |
| **Price mode**           | Most common observed market price                          |
| **Land area**            | Property-size comparison                                   |
| **Building area**        | Built-property benchmarking                                |
| **Active listing count** | Proxy for market supply / liquidity                        |
| **Min–max price**        | Entry-level vs. premium market range                       |
| **Property type**        | Distinguish land-oriented vs. built-property opportunities |
| **Price trend**          | Monitor market movement over time                          |
| **Price fluctuation**    | Identify market heterogeneity and volatility               |

### 📊 Analytical Data Structure

The analytical layer contains relatively slower-moving economic indicators used to contextualize property-market conditions.

| Indicator      | Analytical Purpose                                          |
| -------------- | ----------------------------------------------------------- |
| **IHPR**       | Monitor national residential property-price direction       |
| **Inflation**  | Convert nominal price growth into a real-return perspective |
| **UMR**        | Approximate local purchasing-power conditions               |
| **Population** | Estimate future buyer / renter pool                         |
| **BI Rate**    | Contextualize financing and mortgage-cost conditions        |
| **GDP Growth** | Assess broader economic momentum                            |
| **PIR**        | Evaluate housing affordability relative to local income     |

The architecture is therefore:

```text id="m6v3q8"
┌──────────────────────────────┐
│ Operational Market Data      │
│                              │
│ Listings                     │
│ Prices                       │
│ Property Sizes               │
│ Supply                       │
│ Property Types               │
│ Price Trends                 │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Analytical Economic Data     │
│                              │
│ IHPR                         │
│ Inflation                    │
│ UMR                          │
│ Population                   │
│ BI Rate                      │
│ GDP Growth                   │
│ PIR                          │
└──────────────┬───────────────┘
               │
               ▼
        Investment Analysis
```

---

## 📈 Property Market Analysis

The platform analyzes property markets through multiple dimensions rather than relying on a single price metric.

### 💰 Price Analysis

Price analysis includes:

* Average price.
* Median-like market tendency through the mode.
* Minimum and maximum values.
* Price movement over time.
* Area-to-area comparisons.

Using the **price mode** can provide a useful view of the most commonly observed price level while reducing the influence of extreme outliers.

### 📐 Property Size Analysis

Land and building area are analyzed to understand the physical characteristics of properties within a market.

This supports comparisons such as:

```text id="q3m8x5"
Area
 ↓
Typical Land Size
 ↓
Typical Building Size
 ↓
Typical Price
 ↓
Relative Market Position
```

### 🏠 Property Type Analysis

Property type helps distinguish different investment characteristics.

For example:

```text id="v7p2m4"
Vacant Land
   ↓
Capital-Gain-Oriented Thesis

Built Property
   ↓
Potential Rental / Cash-Flow Thesis
```

The platform therefore considers property type as part of investment context rather than treating all listings as equivalent.

---

## 🏙️ Market Supply & Listing Density

The number of active listings provides a useful market-level signal.

Conceptually:

```text id="k8m4q2"
High Listing Density
       ↓
More Available Comparables
       ↓
Potentially More Competitive Market

Low Listing Density
       ↓
Fewer Comparables
       ↓
Potentially Tighter Supply
```

Listing density is not treated as a standalone measure of market liquidity, but as a market-structure signal that can be interpreted together with other indicators.

---

## 📉 Price Range & Market Segmentation

Minimum and maximum prices help reveal the internal structure of an area.

```text id="b5x7m3"
Minimum Price
     ↓
Entry-Level Market

Typical / Modal Price
     ↓
Core Market

Maximum Price
     ↓
Premium / Upgrade Market
```

This provides more context than relying solely on an area-wide average.

---

## 📊 Price Trend & Volatility

### Price Trend

Price trends are used to understand the direction of market movement.

The analysis helps answer:

* Is the market appreciating?
* Is price movement relatively stable?
* Has growth accelerated or weakened?
* How does the area compare with nearby markets?

### Price Fluctuation

Price fluctuation provides a qualitative signal about market heterogeneity.

```text id="p9m6x2"
High Fluctuation
      ↓
More Heterogeneous / Transitional Market
      ↓
Potentially Higher Uncertainty
      +
Potential Upside

Low Fluctuation
      ↓
More Stable Market
      ↓
Potentially Lower Uncertainty
```

Volatility should therefore be interpreted as both a **risk signal and a potential opportunity signal**, depending on the broader market context.

---

## 🌍 Macroeconomic Integration

One of the core strengths of the platform is that property listings are not analyzed in isolation.

### 🏠 IHPR

The **Residential Property Price Index (IHPR)** provides a national benchmark for broader residential property-price direction.

### 📈 Inflation

Inflation is used to distinguish nominal price appreciation from real purchasing-power-adjusted growth.

For example:

```text id="m7q4x2"
Nominal Property Growth
          -
       Inflation
          ↓
       Real Gain
```

### 💵 UMR

Regional minimum wage is used as a rough proxy for local purchasing power.

It contributes to affordability-oriented analysis, particularly through the Price-to-Income Ratio.

### 👥 Population

Population growth provides a signal for the potential future pool of buyers or renters.

```text id="w5m8p3"
Population Growth
       ↓
Potential Demand Growth
       ↓
Compare with Housing Supply
       ↓
Supply-Demand Signal
```

### 🏦 BI Rate

The Bank Indonesia policy rate provides financing context because interest-rate changes can affect mortgage costs and investor financing decisions.

### 📊 GDP Growth

Regional or national economic growth provides a broader indicator of economic momentum that can be compared against property-price trends.

---

## 💵 Price-to-Income Ratio (PIR)

The **Price-to-Income Ratio (PIR)** is used as an affordability indicator.

Conceptually:

```text id="x4m9q2"
Property Price
──────────────
Local Income
      ↓
     PIR
```

A high and rapidly rising PIR may indicate increasing affordability pressure.

However, PIR should not be interpreted mechanically.

```text id="j7p3m8"
High PIR
  +
Rapid Increase
  ↓
Potential Overpricing Signal

High PIR
  +
Stable
  +
Affluent / High-Demand Market
  ↓
Not Automatically a Bubble
```

This distinction is important because affordability metrics need to be interpreted within local economic and demand conditions.

---

## 🔍 Cross-Indicator Analysis

Single metrics rarely provide enough information to support an investment conclusion.

The platform therefore combines indicators to derive additional market signals.

### 👥 Population Growth × Housing Supply

```text id="a5m8q3"
Fast Population Growth
          +
Limited Housing Supply
          ↓
Demand > Supply
          ↓
Potential Upward Price Pressure
```

This signal helps identify areas where demographic growth may be outpacing available housing.

### 🏦 BI Rate × Property Type

Financing conditions can interact differently with property types.

```text id="p6x3m9"
Rising Interest Rate
        ↓
Higher Financing Cost
        ↓
Compare Investment Thesis

Built / Rentable Property
        ↓
Potential Rental Cash Flow

Vacant Land
        ↓
More Reliance on Future Appreciation
```

The framework therefore considers property type together with financing conditions.

### 📈 GDP / GRDP × Property Price Trend

A region with relatively strong economic growth but comparatively slower property-price growth may warrant further investigation.

```text id="q9m4x5"
Economic Growth
      ↑
Property Prices
      ↓ / Flat
      ↓
Potential "Not Yet Priced In" Signal
```

This is a screening signal, not a guarantee of future appreciation.

---

## 🧭 Investment Analysis Workflow

The platform provides a structured decision workflow.

```text id="k3w8m5"
1. Macro Screening
   │
   ├── IHPR
   ├── BI Rate
   ├── Inflation
   ├── GDP Growth
   ├── Population
   ├── UMR
   └── PIR
        ↓
2. Province / City Comparison
        ↓
3. Area-Level Drill-Down
        ↓
4. Affordability & Price Benchmarking
        ↓
5. Listing Evaluation
        ↓
6. Compare Against Area Average / Typical Price
        ↓
7. Examine Price Trend & Volatility
        ↓
8. Investment Decision
```

The final decision framework can be expressed as:

```text id="v8m2q7"
BUY
NEGOTIATE
WAIT
PASS / AVOID
```

The platform does not automate investment decisions. Instead, it creates a repeatable analytical framework that helps an analyst make them with better information.

---

## 🏷️ Listing Evaluation

At the individual-property level, a listing can be evaluated against its surrounding market.

Key comparison dimensions include:

| Dimension                | Question                                                      |
| ------------------------ | ------------------------------------------------------------- |
| 💰 **Price**             | Is the asking price above or below the area's typical level?  |
| 📐 **Land Area**         | How large is the property relative to the local market?       |
| 🏠 **Building Area**     | Does the built area match the area's typical profile?         |
| 🏷️ **Property Type**    | Is the investment thesis land-oriented or cash-flow-oriented? |
| 📈 **Price Trend**       | Is the local market appreciating, stable, or weakening?       |
| 📊 **Price Fluctuation** | How heterogeneous or volatile is the market?                  |
| 💵 **Affordability**     | How does the price compare with local income indicators?      |
| 🌍 **Macro Context**     | Does the broader economic environment support the thesis?     |

---

## 🖥️ Frontend & Access Control

A role-based web frontend provides different levels of access.

### 👨‍💼 Admin Role

Administrators have access to:

* Full CRUD operations.
* Data management.
* Market-data maintenance.
* Analytical-data management.

### 👤 User Role

Users receive analysis-oriented access:

* Read-only data exploration.
* Category filtering.
* Market analysis.
* Full-table CSV export.

The access model can be represented as:

```text id="m2q7x4"
                 Login
                   ↓
            Role Identification
              /       \
             /         \
        Admin           User
          ↓               ↓
     Full CRUD        Read / Filter
          ↓               ↓
     Data Management   CSV Export
```

---

## 📤 CSV Export

The platform supports **CSV export** so analysts can continue working with the data outside the application.

Typical downstream workflows include:

```text id="p5x8m3"
Dashboard
    ↓
Filter / Select Data
    ↓
CSV Export
    ↓
Python / Excel / Statistical Analysis
```

This makes the platform useful not only as a dashboard, but also as a data-access layer for further analysis.

---

## 📊 Analytical Dashboard

The dashboard is designed to provide:

* Market-level summaries.
* Category filtering.
* Property comparison.
* Macroeconomic context.
* Listing exploration.
* Data export.

The interaction model is:

```text id="c8m4q7"
User
 ↓
Select Region / Category
 ↓
Apply Filters
 ↓
Inspect Market Indicators
 ↓
Compare Listings
 ↓
Export Data
```

This supports both high-level market screening and detailed property exploration.

---

## 🏗️ System Architecture

The project can be viewed through five logical layers.

### 📥 Data Layer

Contains property listings and macroeconomic indicators.

### 🗄️ Data Modeling Layer

Separates frequently updated operational information from relatively stable analytical indicators.

### 🔄 Processing Layer

Transforms raw records into comparable market metrics and derived indicators.

### 📊 Analytics Layer

Combines:

```text id="x6q3m9"
Property Metrics
      +
Market Statistics
      +
Macroeconomic Indicators
      +
Affordability Metrics
      ↓
Investment Signals
```

### 🖥️ Presentation Layer

Provides role-based dashboard access, filtering, and CSV export.

---

## 🔄 End-to-End Data Flow

```text id="n7m3x8"
Property Listings
       ↓
Operational Data Structure
       │
       ├──────────────┐
       │              │
       ↓              ↓
Market Metrics    Listing Evaluation
       │              │
       └──────┬───────┘
              ↓
     Analytical Data
              +
     Macroeconomic Data
              ↓
      Cross-Indicator Analysis
              ↓
       Investment Signals
              ↓
        Web Dashboard
              ↓
        User Decision
```

---

## 🔬 Technical Highlights

### Dual Data Structures

Separating operational and analytical information according to update frequency simplifies data-refresh logic and creates a clearer conceptual data architecture.

### Market Benchmarking

Property listings are interpreted against area-level market statistics instead of being evaluated in isolation.

### Macroeconomic Context

IHPR, inflation, UMR, population, BI Rate, GDP growth, and PIR provide external context for local property-market analysis.

### Derived Investment Signals

The platform relates multiple indicators to surface signals that would not be visible from a single dataset.

### Role-Based Data Access

Administrative CRUD and user-oriented read/filter/export access provide a practical separation between data maintenance and analytical consumption.

### Decision-Oriented Analytics

The analytical pipeline ends with a structured investment decision workflow rather than stopping at descriptive statistics.

---

## 💡 Investment Decision Framework

The platform supports four broad outcomes:

| Decision            | General Interpretation                                                          |
| ------------------- | ------------------------------------------------------------------------------- |
| 🟢 **Buy**          | Property and market indicators support the investment thesis                    |
| 🟡 **Negotiate**    | Fundamentals may be attractive, but price appears above the preferred benchmark |
| 🔵 **Wait**         | Market conditions or uncertainty suggest delaying the decision                  |
| 🔴 **Pass / Avoid** | Pricing, affordability, volatility, or macro conditions weaken the thesis       |

These categories are analytical outputs intended to structure human judgment, not automated financial advice.

---

## 📊 Portfolio-Level Analytical Questions

The platform enables questions such as:

* Which areas have the strongest pricing momentum?
* Where is housing supply relatively constrained?
* Which regions show stronger affordability pressure?
* Where is population growing faster than housing availability?
* Which property types are better aligned with the prevailing financing environment?
* Which listings appear expensive relative to their local market?
* Which areas may be growing economically without equivalent property-price repricing?
* Which markets appear stable versus transitional?

---

## 💼 Business Value

The platform transforms fragmented property and economic data into a repeatable analytical workflow.

```text id="r4m8q2"
Raw Property Data
      +
Macroeconomic Data
      ↓
Structured Market Intelligence
      ↓
Comparable Benchmarks
      ↓
Cross-Indicator Signals
      ↓
Investment Screening
      ↓
Better-Informed Decisions
```

This creates value at multiple levels:

### 🔎 Market Screening

Identify regions and cities worth deeper investigation.

### 🏙️ Area Comparison

Compare local markets using both property and macroeconomic indicators.

### 🏠 Listing Evaluation

Assess individual properties against area-level benchmarks.

### 📈 Opportunity Detection

Identify potential supply-demand imbalances and markets that may not yet be fully repriced.

---

## 🗺️ Project Scope

| Module                             | Description                                                        | Status        |
| ---------------------------------- | ------------------------------------------------------------------ | ------------- |
| 🏘️ **Property Market Analysis**   | Analyze price, size, listing density, type, trend, and fluctuation | ✅ Implemented |
| 🗄️ **Operational Data Structure** | Frequently updated property-market data                            | ✅ Implemented |
| 📊 **Analytical Data Structure**   | Relatively stable macroeconomic indicators                         | ✅ Implemented |
| 🏦 **Macroeconomic Integration**   | IHPR, inflation, UMR, population, BI Rate, GDP growth, PIR         | ✅ Implemented |
| 💰 **Affordability Analysis**      | Price-to-Income Ratio and price-to-UMR comparison                  | ✅ Implemented |
| 📈 **Market Benchmarking**         | Compare listings with area-level market conditions                 | ✅ Implemented |
| 🔍 **Cross-Indicator Analysis**    | Combine demographic, supply, economic, and pricing signals         | ✅ Implemented |
| 👨‍💼 **Admin CRUD**               | Administrative data management                                     | ✅ Implemented |
| 👤 **User Access**                 | Read-only filtering and analytical exploration                     | ✅ Implemented |
| 📤 **CSV Export**                  | Export data for further analysis                                   | ✅ Implemented |
| 🖥️ **Web Dashboard**              | Interactive property and market-data frontend                      | ✅ Implemented |
| 🧭 **Investment Workflow**         | Buy / negotiate / wait / pass decision framework                   | ✅ Implemented |

---

## 💼 Portfolio Alignment

The project directly reflects the capabilities described in the professional project entry:

| LinkedIn Capability                   | Project Evidence                                                |
| ------------------------------------- | --------------------------------------------------------------- |
| Property market analytics             | Property listing and market-level analysis                      |
| Python / Pandas                       | Analytical data processing                                      |
| Data visualization                    | Dashboard-oriented market presentation                          |
| Statistical analysis                  | Market metrics, trends, ratios, and comparative analysis        |
| Macroeconomic integration             | IHPR, inflation, UMR, population, BI Rate, GDP growth           |
| Price-to-Income Ratio                 | Affordability analysis                                          |
| Operational vs. analytical structures | Update-frequency-based data architecture                        |
| Role-based frontend                   | Admin and user access model                                     |
| CRUD                                  | Administrative data management                                  |
| Filtering                             | User-oriented market exploration                                |
| CSV export                            | Downstream data analysis                                        |
| Investment workflow                   | Macro screening → area analysis → listing evaluation → decision |
| Cross-indicator insights              | Population × supply, rates × property type, GDP × price trends  |

> **Portfolio positioning:** This project demonstrates the ability to combine operational real-estate data with macroeconomic intelligence and turn the resulting analysis into a structured investment evaluation workflow.

---

## 📈 From Data to Investment Intelligence

The core value chain can be summarized as:

```text id="m8x4q6"
Property Data
      +
Economic Data
      ↓
Data Architecture
      ↓
Market Metrics
      ↓
Affordability Analysis
      ↓
Cross-Indicator Relationships
      ↓
Market Signals
      ↓
Listing Benchmark
      ↓
Investment Decision
```

This positioning emphasizes the project as an **investment intelligence platform**, not merely a property listing dashboard.

---

## 🔭 Future Development

Potential future extensions include:

* Automated macroeconomic data refresh.
* Historical market-index time series.
* Automated valuation models.
* Property price anomaly detection.
* Spatial / geospatial analysis.
* Rental-yield estimation.
* Mortgage affordability simulation.
* Time-series property-price forecasting.
* Investment scoring models.
* Scenario analysis for interest-rate and inflation changes.
* Alerting for newly identified underpriced areas.
* Portfolio-level property comparison.

These are future directions and are not presented as current functionality.

---

## 🚀 Deployment

The application is structured as a web-based analytical platform.

The operational workflow is:

```text id="q7m2x5"
Data Sources
     ↓
Data Processing
     ↓
Analytical Models / Indicators
     ↓
Web Application
     ↓
Dashboard
     ↓
Filtering / Export
```

Production access and sensitive investment data should remain protected when the platform is deployed in a live environment.

---

## 📸 Project Screenshots

![Screenshot 1](images/Picture1.png)

![Screenshot 2](images/Picture2.png)

![Screenshot 3](images/Picture3.png)

![Screenshot 4](images/Picture4.png)

![Screenshot 5](images/Picture5.png)

![Screenshot 6](images/Picture6.png)

![Screenshot 7](images/Picture7.png)

![Screenshot 8](images/Picture8.png)

![Screenshot 9](images/Picture9.png)

![Screenshot 10](images/Picture10.png)

![Screenshot 11](images/Picture11.png)

![Screenshot 12](images/Picture12.png)

![Screenshot 13](images/Picture13.png)

![Screenshot 14](images/Picture14.png)

![Screenshot 15](images/Picture15.png)

![Screenshot 16](images/Picture16.png)

![Screenshot 17](images/Picture17.png)

![Screenshot 18](images/Picture18.png)

![Screenshot 19](images/Picture19.png)

![Screenshot 20](images/Picture20.png)

![Screenshot 21](images/Picture21.png)

![Screenshot 22](images/Picture22.png)

![Screenshot 23](images/Picture23.png)

![Screenshot 24](images/Picture24.png)

![Screenshot 25](images/Picture25.png)

![Screenshot 26](images/Picture26.png)

![Screenshot 27](images/Picture27.png)

![Screenshot 28](images/Picture28.png)

![Screenshot 29](images/Picture29.png)

![Screenshot 30](images/Picture30.png)

![Screenshot 31](images/Picture31.png)

![Screenshot 32](images/Picture32.png)

![Screenshot 33](images/Picture33.png)

![Screenshot 34](images/Picture34.png)

![Screenshot 35](images/Picture35.png)

![Screenshot 36](images/Picture36.png)

![Screenshot 37](images/Picture37.png)

![Screenshot 38](images/Picture38.png)

![Screenshot 39](images/Picture39.png)

![Screenshot 40](images/Picture40.png)

![Screenshot 41](images/Picture41.png)

![Screenshot 42](images/Picture42.png)

![Screenshot 43](images/Picture43.png)

![Screenshot 44](images/Picture44.png)

![Screenshot 45](images/Picture45.png)

![Screenshot 46](images/Picture46.png)

![Screenshot 47](images/Picture47.png)

![Screenshot 48](images/Picture48.png)

![Screenshot 49](images/Picture49.png)

![Screenshot 50](images/Picture50.png)

![Screenshot 51](images/Picture51.png)

![Screenshot 52](images/Picture52.png)

![Screenshot 53](images/Picture53.png)

![Screenshot 54](images/Picture54.png)

![Screenshot 55](images/Picture55.png)

![Screenshot 56](images/Picture56.png)

![Screenshot 57](images/Picture57.png)

![Screenshot 58](images/Picture58.png)

![Screenshot 59](images/Picture59.png)

![Screenshot 60](images/Picture60.png)

![Screenshot 61](images/Picture61.png)

![Screenshot 62](images/Picture62.png)

![Screenshot 63](images/Picture63.png)

![Screenshot 64](images/Picture64.png)

![Screenshot 65](images/Picture65.png)

![Screenshot 66](images/Picture66.png)

![Screenshot 67](images/Picture67.png)

![Screenshot 68](images/Picture68.png)

![Screenshot 69](images/Picture69.png)

![Screenshot 70](images/Picture70.png)

![Screenshot 71](images/Picture71.png)

![Screenshot 72](images/Picture72.png)

![Screenshot 73](images/Picture73.png)

![Screenshot 74](images/Picture74.png)

![Screenshot 75](images/Picture75.png)

![Screenshot 76](images/Picture76.png)

![Screenshot 77](images/Picture77.png)

![Screenshot 78](images/Picture78.png)

![Screenshot 79](images/Picture79.png)

![Screenshot 80](images/Picture80.png)

![Screenshot 81](images/Picture81.png)

![Screenshot 82](images/Picture82.png)

---

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for the complete license text.

Third-party datasets, economic data sources, libraries, APIs, and external services remain subject to their respective licenses and terms.

---

<div class="contact-hero">

<p><strong>Interested in the project?</strong></p>

<p>
👨‍💻 <strong>Bernardo Nandaniar Sunia</strong><br/>
Bachelor of Computer Science — Diponegoro University<br/>
Property Analytics · Data Analysis · Investment Intelligence
</p>

<p>
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

<p>
<em>Property analytics · Macroeconomic analysis · Data visualization · Investment decision support</em>
</p>

</div>

---

## 📌 Conclusion

The **Property Data Analysis & Investment Intelligence Platform** demonstrates how structured property-market data can be combined with macroeconomic indicators to create a repeatable analytical framework for investment evaluation.

By separating **frequently updated operational property data** from **relatively stable analytical indicators**, the platform establishes a clearer foundation for market analysis. Price, property size, listing density, property type, price trends, and market fluctuation can then be interpreted alongside **IHPR, inflation, UMR, population, BI Rate, GDP growth, and PIR**.

The resulting workflow moves from **macroeconomic screening and regional comparison to area-level analysis, listing benchmarking, and investment decisions such as buy, negotiate, wait, or pass**.

The project's strongest contribution is therefore not a single metric or dashboard, but the integration of multiple signals into a structured decision process that turns property data into **investment intelligence**.
