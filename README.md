# NDIS Digital-First Pricing Artefact Tools  
*A modern, structured approach to analysing changes in the NDIS Support Catalogue*

---

## 📘 Overview

The **Digital-First Pricing Artefact Tools** project provides a clean, modern, NDIA-themed web interface for working with NDIS Support Catalogue data in a structured, machine-readable way.

The platform includes:

- A converter that transforms the **official Support Catalogue XLSX** into **validated, structured JSON**.
- A comparison tool that analyses **version-to-version changes**, identifying:
  - Added items  
  - Removed items  
  - Price limit changes by state  
  - Claim type flag changes  
  - Category shifts  
- Export functionality for briefing packs:
  - **Markdown report**  
  - **JSON diff**  
  - **PDF output**

This tool is part of a broader strategic push toward **Digital-First Pricing Artefacts**, improving accuracy, discoverability and maintainability over traditional static PDFs.

---

## 🚀 Features

### 🔄 XLSX → JSON Conversion
- Converts the official **Support Catalogue** Excel file into structured JSON.
- Normalises:
  - booleans (Yes/No → true/false)  
  - price fields  
  - date fields  
- Ensures consistent schema across releases.
- Designed for ingestion into dashboards, RAG/LMM systems, and validation pipelines.

### 🆚 Version Comparison
Upload two catalogue JSON files and instantly see:

- **Items added**
- **Items removed**
- **Modified items**, including:
  - Per-state price changes
  - Claim type changes  
- Summary metrics (added/removed/modified/unchanged counts)

### 📊 Data Presentation
- Paginated tables
- Expandable sections for clarity
- Sorted and labelled data for easy interpretation
- Clean NDIA-aligned visual design

### 📤 Export Capabilities
- **Markdown report** for briefings  
- **JSON representation** of all changes  
- **PDF snapshot** for archival or external reference  

---

## 🏛 Technical Architecture

This project is built using:

| Layer | Technology |
|------|------------|
| Frontend | Streamlit multipage app |
| Styling | Custom NDIA theme (Inter font, NDIA Purple #6D3078 & Teal #009CA6) |
| Processing | Python (pandas, openpyxl) |
| PDF Generation | ReportLab (pure Python, Streamlit-Cloud-friendly) |
| Deployment | Streamlit Cloud |

No Docker is required for Streamlit Cloud deployment.

---

## 📂 Repository Structure

```
digital-first-catalogue-tools/
│
├── streamlit_app.py                # Landing page
├── ndis_theme.css                  # NDIA visual theme (safe version)
├── requirements.txt                # Python dependencies
│
├── version_diff.py                 # Core diff logic
├── xlsx_to_json.py                 # XLSX → JSON converter
│
├── pages/
│   ├── 1_convert_xlsx.py           # Conversion UI
│   └── 2_compare_versions.py       # Diff UI
│
└── README.md
```

---

## ⚙️ Installation (Local Development)

### 1. Clone the repository

```
git clone https://github.com/<your-account>/<your-repo>.git
cd <your-repo>
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the app

```
streamlit run streamlit_app.py
```

The app will launch at:

```
http://localhost:8501
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push this repository to GitHub  
2. Visit: https://streamlit.io/cloud  
3. Select **“New app”**  
4. Choose:
   - Repo: *your repo*
   - Main file: `streamlit_app.py`
5. Click **Deploy**

Streamlit Cloud will automatically:

- install packages from `requirements.txt`
- detect multipage structure
- serve `ndis_theme.css`
- build your environment

---

## 📸 Screenshots (optional)

(Add screenshots here once deployed.)

```
![Home Page](docs/homepage.png)
![Comparison Tool](docs/comparison.png)
```

---

## 🧪 Testing & Validation

This app has been validated for:

- Streamlit Cloud compatibility  
- Modern browsers (Chrome, Edge, Safari)  
- Large file uploads (up to Streamlit’s 200MB limit)  
- JSON accuracy across version changes  
- PDF generation consistency  

---

## 🛠 Extensibility

Future enhancements may include:

- **Visual change charts**
- **Schema validation tooling**
- **API endpoints for automated ingest**
- **NDIA internal authentication layers**
- **Integration with RAG or LLM-based assistants**

If you'd like, I can generate a roadmap or development plan.

---

## 👥 Contributors

This tool is part of the NDIA’s forward-looking work on modernising the delivery of pricing artefacts and improving the discoverability and usability of structured pricing information.

---

## 📄 Licence

Choose an appropriate licence depending on your context:

- **Internal NDIA:** *Proprietary – NDIA internal use only*  
- **Public open-source:** MIT or Apache 2.0  

You may add:

```
© National Disability Insurance Agency
```

---
