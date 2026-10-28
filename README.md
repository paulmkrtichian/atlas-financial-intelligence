# ATLAS AI
### AI-Powered Financial Research & Intelligence Platform

Atlas AI is a Python-based financial intelligence platform designed to combine artificial intelligence, financial statement analysis, and quantitative modeling into a unified research environment.

The project explores how AI can assist financial analysts by interpreting financial questions, selecting analytical tools, identifying meaningful financial trends, and generating research insights supported by numerical calculations.

Unlike a traditional AI chatbot, Atlas integrates language models with Python-based financial analysis tools to improve the reliability and transparency of its outputs.

**Status:** Active Development — Version 3

---

## Overview

Financial analysis frequently involves collecting information from multiple sources, standardizing financial statements, calculating performance metrics, and interpreting results.

Atlas AI aims to streamline this workflow through a combination of:

- AI-assisted financial research
- Automated financial calculations
- Financial statement standardization
- Historical performance analysis
- Scenario modeling
- Interactive financial dashboards

The long-term objective is to develop an AI-powered financial research environment capable of supporting increasingly complex analytical workflows.

---

## Key Features

### 1. AI Financial Analyst

Atlas allows users to ask financial questions in natural language.

The AI identifies an appropriate analytical tool, executes a Python-based calculation, and generates an explanation of the result.

**Example questions:**

- How much did revenue grow?
- What was the company's operating margin?
- How profitable was the company after expenses?
- Summarize the company's financial performance.

**Workflow:**

`User Question → AI Tool Selection → Python Calculation → AI Interpretation`

Currently supported tools include:

| Financial Tool | Function |
|---|---|
| Revenue Growth | Calculates year-over-year revenue growth |
| Operating Margin | Measures operating profitability |
| Net Margin | Measures net profitability |
| Financial Summary | Retrieves key income statement figures |

This approach separates financial calculations from language-model interpretation.

### 2. Research Intelligence

Atlas generates AI-assisted financial research reports using standardized company data.

The research workflow is designed to:

- Identify significant financial developments
- Examine historical financial performance
- Highlight potential strengths and weaknesses
- Distinguish observed financial results from hypotheses
- Support conclusions with available financial evidence

Atlas also incorporates validation mechanisms intended to reduce unsupported financial claims.

### 3. Financial Statement Analysis

Atlas supports importing and analyzing company financial data.

Capabilities include:

- CSV-based financial data imports
- Financial column mapping and standardization
- Revenue and profitability analysis
- Historical financial comparisons
- Financial ratio calculations
- Interactive financial visualizations

The platform also includes public-company financial data functionality.

### 4. Scenario Intelligence

Atlas provides a scenario modeling environment that allows users to examine alternative financial outcomes.

Users can construct:

**Downside Scenario:** More conservative assumptions.

**Base Scenario:** A central set of modeling assumptions.

**Upside Scenario:** More optimistic assumptions.

The current scenario engine projects revenue and operating income using adjustable growth and operating-margin assumptions.

Outputs include:

- Projected revenue
- Projected operating income
- Scenario comparison charts
- Final-year financial comparisons
- Downloadable scenario data

Scenario outputs are illustrative and should not be interpreted as investment forecasts.

### 5. Research-to-Scenario Integration

Atlas connects its Research Intelligence and Scenario Intelligence modules.

Users can investigate a financial finding, select a modeling question, and transfer relevant historical financial information into the scenario modeling environment.

This creates a workflow connecting AI-assisted research with quantitative financial analysis.

### 6. Hybrid AI Architecture

Atlas supports a modular AI architecture designed for both local and cloud-based language models.

**Current implementation:**

- Local language-model inference through Ollama
- Qwen-based financial question interpretation
- Python-based financial calculations
- A provider-routing module for future cloud integration

Cloud AI integration is planned as an optional capability.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Pandas | Financial data processing |
| Plotly | Financial data visualization |
| Ollama | Local language-model inference |
| Qwen | Natural-language financial analysis |
| SQLite | Local data storage |
| Pytest | Automated testing |

---

## System Architecture

```text
                     ATLAS AI
                        |
                Streamlit Interface
                        |
          +-------------+-------------+
          |             |             |
     Financial      Research      Scenario
      Analysis      Intelligence   Intelligence
          |             |             |
          |        AI Model Router     |
          |             |             |
          |       Local AI / Cloud AI |
          |             |             |
          +-------------+-------------+
                        |
              Python Financial Tools
                        |
              Calculated Results
                        |
               AI Interpretation
                        |
                User Review
```

Atlas is designed around a separation between language-model reasoning and deterministic financial calculations.

---

## Getting Started

### Prerequisites

- Python
- Git
- Ollama
- A compatible local language model

### Installation

Clone the repository:

```bash
git clone https://github.com/paulmkrtichian/atlas-financial-intelligence.git
```

Navigate into the project:

```bash
cd atlas-financial-intelligence
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project dependencies using the repository's dependency file, once configured.

### Configure Ollama

Install Ollama and download the local model:

```bash
ollama pull qwen3:4b
```

Ensure Ollama is running before using local AI features.

### Launch Atlas

```bash
python -m streamlit run app.py
```

### Run Tests

```bash
python -m pytest -v
```

---

## Development Roadmap

### Current Development

- [x] Interactive Streamlit dashboard
- [x] Financial statement analysis
- [x] Financial column standardization
- [x] Historical financial analysis
- [x] Scenario modeling
- [x] AI-generated financial research
- [x] Research-to-scenario integration
- [x] Local language-model integration
- [x] AI financial tool selection
- [x] Automated financial calculation tests

### Planned Enhancements

- [ ] Multi-tool AI reasoning
- [ ] Cloud AI provider integration
- [ ] Multi-document financial intelligence
- [ ] Advanced retrieval-augmented generation
- [ ] Research memory and source tracking
- [ ] Discounted cash flow valuation
- [ ] Valuation sensitivity analysis
- [ ] Excel financial model exports
- [ ] Expanded financial research automation

---

## Project Motivation

Atlas AI was developed to explore the intersection of artificial intelligence, financial analysis, and software engineering.

As AI becomes increasingly integrated into financial workflows, the ability to combine language models with reliable analytical tools presents opportunities to improve research efficiency and accessibility.

Atlas is an ongoing effort to understand these technologies through practical development rather than relying exclusively on existing AI applications.

---

## Disclaimer

Atlas AI is an experimental research and educational project.

Its analyses, projections, and AI-generated interpretations may contain errors and should be independently verified.

The platform does not provide personalized investment advice.

---

**Built with Python, Streamlit, and AI.**