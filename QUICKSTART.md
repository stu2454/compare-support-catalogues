# Quick Start Guide

## 🚀 Get Running in 3 Steps

### Step 1: Navigate to directory
```bash
cd streamlit-catalogue-comparison
```

### Step 2: Choose your method

**Option A: Docker (Recommended)**
```bash
docker-compose up --build
```

**Option B: Python**
```bash
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Step 3: Open browser
```
http://localhost:8501
```

---

## ✅ Verify Everything Works

Run the test suite:
```bash
python test_tool.py
```

Expected output:
```
✅ Sheet detection: PASSED
✅ Column mapping: PASSED  
✅ Data normalization: PASSED
✅ JSON conversion: PASSED
✅ Version comparison: PASSED
✅ Change detection: PASSED
```

---

## 📊 Using the Tool

1. **Home page:** Read overview and navigate
2. **Compare Versions page:**
   - Upload OLD and NEW Excel files
   - Use tabs to map sheets
   - Click "Convert to JSON and Run Comparison"
   - Explore results in expanders
   - Download JSON files
3. **JSON Explainer page:** Understand the "why"

---

## 📦 Deploying to Production

### To Render.com (or similar):

1. Push code to Git repository
2. Create new Web Service on Render
3. Connect your repository
4. Configure:
   - **Environment:** Docker
   - **Port:** 8501
   - **Build command:** (automatic from Dockerfile)
   - **Start command:** (automatic from Dockerfile)
5. Deploy!

---

## 🔧 Common Issues

**Port already in use?**
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

**Module not found?**
```bash
# Ensure you're in venv and installed dependencies
pip install -r requirements.txt
```

**CSS not loading?**
```bash
# Check ndis_theme.css exists in same directory as streamlit_app.py
ls ndis_theme.css
```

---

## 📝 Files Overview

| File | Purpose | Lines |
|------|---------|-------|
| `streamlit_app.py` | Home page | ~100 |
| `pages/2_compare_versions.py` | Main workflow | ~400 |
| `pages/3_JSON_Conversion_Explainer.py` | Explainer | ~300 |
| `xlsx_to_json.py` | Conversion engine | ~350 |
| `version_diff.py` | Comparison logic | ~200 |
| `ndis_theme.css` | NDIA styling | ~200 |
| `test_tool.py` | Test suite | ~350 |

**Total:** ~1,900 lines of production code

---

## 🎯 Key Commands

```bash
# Run tests
python test_tool.py

# Run app (development)
streamlit run streamlit_app.py

# Run app (Docker)
docker-compose up --build

# Stop Docker
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build --force-recreate
```

---

## 📚 Documentation

- **PROJECT_SUMMARY.md** - Complete project overview
- **README.md** - Technical documentation
- **assets/README.md** - Diagram requirements
- Code comments throughout

---

**Status:** ✅ Ready to run!  
**First step:** `python test_tool.py`
