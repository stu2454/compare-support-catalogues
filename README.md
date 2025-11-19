# NDIS Support Catalogue Comparison Tool

A digital-first internal tool for the National Disability Insurance Agency (NDIA) Markets Delivery team to convert Support Catalogue Excel files to structured JSON and compare versions with detailed change detection.

## 🎯 Purpose

This tool addresses the limitations of static document-based pricing artefacts by:
- Converting Excel catalogues to machine-readable JSON
- Comparing catalogue versions with field-level change detection
- Providing governance insights (e.g., items requiring review)
- Demonstrating the value of digital-first pricing artefacts

## 🏗️ Architecture

```
streamlit-catalogue-comparison/
├── streamlit_app.py              # Home page with navigation
├── pages/
│   ├── 2_compare_versions.py     # Main workflow (upload → map → compare)
│   └── 3_JSON_Conversion_Explainer.py  # Educational content
├── xlsx_to_json.py               # Conversion engine
├── version_diff.py               # Comparison logic
├── ndis_theme.css                # NDIA purple branding
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container setup
├── docker-compose.yml            # Compose configuration
└── assets/                       # Diagrams for explainer page
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

### Option 2: Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Access at http://localhost:8501
```

## 📋 Features

### 1. Robust Sheet Detection & Mapping
- Lists all sheets in uploaded workbooks with row counts
- User-driven sheet mapping (handles different naming conventions)
- Preview functionality for selected sheets
- Supports catalogues with or without legacy sheets

### 2. Smart Excel → JSON Conversion
- **Column mapping**: Automatically detects column variations
  - "Item Number" vs "Support Item Number" → `item_number`
  - "NSW" vs "New South Wales" → `price_limit_nsw`
- **Data normalization**:
  - Dates → YYYY-MM-DD format
  - "Yes"/"No" → true/false
  - Empty cells → null
  - Prices → float numbers
- **Validation**: Ensures every item has required fields

### 3. Comprehensive Version Comparison
Detects 7 types of changes:

| Change Type | Description |
|-------------|-------------|
| **Added** | Present only in NEW Current |
| **Removed** | Present in OLD Current, absent from NEW (governance risk) |
| **Moved to Legacy** | Present in OLD Current, now in NEW Legacy |
| **Legacy Removed** | Present in OLD Legacy, absent from NEW |
| **Modified** | In both Current with field-level changes |
| **Unchanged** | In both Current with no changes |
| **Anomalies** | Unusual transitions requiring review |

### 4. Field-Level Change Tracking
For modified items, the tool shows:
- Which specific fields changed (support_name, prices, dates, etc.)
- Old value vs new value
- Both table view and JSON format

### 5. Professional UI
- NDIA purple (#6D3078) branding
- Accessible design
- Wide layout for data tables
- Clear tab navigation
- Download buttons for JSON outputs

## 📊 Usage Workflow

1. **Upload Files**
   - Upload OLD and NEW catalogue Excel files

2. **Map Sheets**
   - Use tabs to configure OLD and NEW catalogues separately
   - Select Current sheet (required)
   - Select Legacy sheet (optional)
   - Preview selected sheets

3. **Convert & Compare**
   - Click "Convert to JSON and Run Comparison"
   - View metadata for both catalogues
   - Download JSON files

4. **Analyze Results**
   - Review summary metrics (added, removed, modified, etc.)
   - Expand sections for detailed results
   - Download modified items as JSON for further analysis

## 🔧 Technical Details

### Dependencies
- **Python 3.11**
- **Streamlit**: Web UI framework
- **pandas**: Data manipulation
- **openpyxl**: Excel file handling

### JSON Schema
```json
{
  "metadata": {
    "source_filename": "...",
    "generated_at": "YYYY-MM-DD HH:MM:SS",
    "current": { "sheet": "...", "rows": 0 },
    "legacy": { "sheet": "...", "rows": 0 }
  },
  "current_items": [
    {
      "item_number": "05_123456",
      "support_name": "...",
      "registration_group": "...",
      "category": "...",
      "unit": "...",
      "claim_type": "...",
      "price_limit_nsw": 0.0,
      "price_limit_vic": 0.0,
      "price_limit_qld": 0.0,
      "price_limit_sa": 0.0,
      "price_limit_wa": 0.0,
      "price_limit_tas": 0.0,
      "price_limit_nt": 0.0,
      "price_limit_act": 0.0,
      "effective_from": "YYYY-MM-DD",
      "effective_to": "YYYY-MM-DD",
      "notes": "...",
      "raw_row_index": 0
    }
  ],
  "legacy_items": [...]
}
```

### Comparison Output
```json
{
  "added": [...],
  "removed": [...],
  "moved_to_legacy": [...],
  "legacy_removed": [...],
  "modified": [
    {
      "item_number": "05_123456",
      "old": {...},
      "new": {...},
      "changes": {
        "support_name": {
          "old": "Old description",
          "new": "New description"
        }
      }
    }
  ],
  "unchanged": [...],
  "anomalies": [...]
}
```

## 🎨 NDIA Branding

The tool uses official NDIA colors:
- **Primary purple**: #6D3078
- **Purple light**: #8B4A96
- **Purple dark**: #4F2357
- **Greys**: #F8F9FA, #E9ECEF, #495057, #212529

All styling is defined in `ndis_theme.css`.

## 📈 What This Enables

Once pricing data is in JSON format:

**For Markets Delivery:**
- Version comparison dashboards
- Automated validation of business rules
- Trend analysis and reporting
- Smart search and filtering

**For ICT/Systems:**
- API access to pricing data
- Automated system updates
- Data quality checks

**For Service Providers:**
- Direct API queries for pricing
- Validation of claims against current pricing
- Auto-updates in provider software

**For Analytics:**
- Real-time dashboards
- Market analysis
- Data visualizations

## 🚢 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Docker Deployment
```bash
docker build -t ndis-catalogue-tool .
docker run -p 8501:8501 ndis-catalogue-tool
```

### Render.com / Cloud Deployment
1. Push code to Git repository
2. Connect to Render.com
3. Configure as Docker service
4. Set port to 8501
5. Deploy

## 📝 Future Enhancements

Potential additions for production:
- [ ] Additional filters (e.g., "show only price changes")
- [ ] Export to executive briefing formats
- [ ] Integration with NDIA systems
- [ ] Scheduled automated comparisons
- [ ] Email alerts for anomalies
- [ ] API endpoints for external access
- [ ] Advanced anomaly detection
- [ ] Historical trend analysis

## 🤝 Contributing

This is an internal NDIA tool developed by Markets Delivery. For questions or suggestions, contact the digital transformation team.

## 📄 License

Internal NDIA use only.

---

**NDIS Support Catalogue Comparison Tool** · Markets Delivery · National Disability Insurance Agency
