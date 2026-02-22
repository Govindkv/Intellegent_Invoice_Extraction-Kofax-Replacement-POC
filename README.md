# Intellegent_Invoice_Extraction-Kofax-Replacement-POC
An advanced invoicing automation solution that combines **deep learning-based OCR (DocTR)** with rule-based field extraction to intelligently extract, validate, and learn field locations from invoices. Features a web-based UI for manual validation and template coordinate mapping.

This Intelligent Invoice Extraction pipeline built as a Proof of Concept to replace Kofax in my organization. Designed a scalable local OCR-based processing system to extract structured invoice data, reduce licensing costs, and improve automation efficiency. This repo demonstrates the real-time production effort and business impact.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This system automates invoice processing by:
1. **Converting PDFs to images** for processing
2. **Extracting text** using DocTR (deep learning OCR)
3. **Parsing invoice fields** via regex patterns
4. **Validating extracted data** against business rules
5. **Learning field coordinates** from vendors for future extractions
6. **Providing manual validation UI** for missing or suspicious fields

### Use Cases
- Automated invoice data entry
- Compliance and audit trail generation
- Multi-vendor invoice processing
- Vendor template learning and optimization

---

## ✨ Features

| Feature | Description | Technology |
|---------|-------------|-----------|
| 🤖 **OCR Processing** | DocTR deep learning model for text detection + bounding boxes | Neural Network (PyTorch) |
| 📍 **Coordinate Mapping** | Stores learned field positions per vendor template | JSON-based repository |
| ✅ **Smart Validation** | Rule-based detection of missing fields, duplicates, type mismatches | Deterministic algorithms |
| 🎨 **Interactive UI** | Canvas-based field annotation and coordinate capture | FastAPI + JavaScript |
| 📊 **JSON Export** | Structured output for downstream processing | JSON serialization |
| 🔄 **Template Learning** | Improves speed with saved vendor templates (not model retraining) | Static template storage |
| 🌐 **REST API** | FastAPI endpoints for integration | REST framework |

---

## 🏗️ Architecture

```
┌─────────────────┐
│   PDF Input     │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────┐
│ PDF to Image Conversion      │
│ (pdf2image + Poppler)        │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ 🤖 MACHINE LEARNING LAYER (DocTR)   │
│ ─────────────────────────────────── │
│ • Pre-trained Neural Network        │
│ • Deep Learning: ResNet50 + PyTorch │
│ • Text Detection & Localization     │
│ • Bounding Box Generation           │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ RULE-BASED EXTRACTION LAYER         │
│ ─────────────────────────────────── │
│ • Regex Pattern Matching            │
│ • Coordinate-Based Lookup           │
│ • Template Query (FieldLearningMap) │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ VALIDATION & BUSINESS LOGIC         │
│ ─────────────────────────────────── │
│ • Deterministic Rule Checking       │
│ • Duplicate Detection               │
│ • Type Validation                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Manual Validation UI (if needed)    │
│ (FastAPI + Interactive Canvas)      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ JSON Output & Template Storage      │
│ (Saves coordinates for future use)  │
└──────────────────────────────────────┘
```

### Technology Stack by Layer

| Layer | Technology | Type |
|-------|-----------|------|
| **OCR** | DocTR with PyTorch backend | 🤖 Deep Learning |
| **Extraction** | Python regex + JSON lookups | 🔧 Rule-Based |
| **Validation** | Business logic rules | ⚙️ Deterministic |
| **UI** | FastAPI + HTML/Canvas | 🌐 Web Framework |

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** (Tested on 3.10)
- **Poppler** (for PDF processing)
- **Git** (optional)

### Step 1: Clone Repository
```bash
cd C:\Users\Govind\Downloads\Data_Scientist
git clone <https://github.com/Govindkv/Intellegent_Invoice_Extraction-Kofax-Replacement-POC.git>
cd Intellegent_Invoice_Extraction
```

### Step 2: Install Poppler (Windows)

**Option A: Using Conda** (Recommended)
```bash
conda install -c conda-forge poppler
```

**Option B: Download Executable**
- Download from: https://github.com/oschwartz10612/poppler-windows/releases
- Extract to: `C:\Program Files\poppler-24.08.0`

### Step 3: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation
```bash
python -c "from doctr.models import ocr_predictor; print('✅ All dependencies installed!')"
```

---

## 🎬 Quick Start

### Run Basic Extraction
```bash
# Single invoice processing
python app.py
```

### Launch Web Interface
```bash
# Start the FastAPI server
python main.py

# Open browser: http://localhost:8000
```

### Process Multiple Invoices
```python
from src.Invoice_Extraction import extract_invoice_fields, Extract_using_coordinates

pdf_path = r"C:\path\to\invoice.pdf"
fields = extract_invoice_fields(pdf_text)
validated_fields = Extract_using_coordinates(fields, pdf_path)
print(validated_fields)
```

---

## 📁 Project Structure

```
Intellegent_Invoice_Extraction/
├── 📄 app.py                          # Main entry point
├── 📄 main.py                         # FastAPI web server
├── 📋 requirements.txt                # Python dependencies
├── 📋 FieldLearningMap.json          # Vendor template coordinates
│
├── 📁 src/
│   ├── Invoice_Extraction.py         # Core OCR & extraction logic
│   ├── SelfLearninValidation.py      # Self-learning validator
│   └── __pycache__/
│
├── 📁 templates/
│   └── index.html                    # Web UI template
│
├── 📁 static/
│   └── app.js                        # Frontend JavaScript
│
├── 📁 Invoices/                      # Input PDFs
│   ├── CN-006991.pdf
│   └── OCRed/                        # OCR output images
│
├── 📁 Output/                        # Extracted JSON results
│   └── extracted_fields.json
│
└── 📁 iiextraction/                  # Conda environment (optional)
```

---

## 📖 Usage Guide

### 1️⃣ Basic Invoice Processing

**Configuration** (in `src/Invoice_Extraction.py`):
```python
# Set your PDF path
pdf_path = r"C:\path\to\invoice.pdf"

# Set Poppler path (if not in system PATH)
poppler_path = r"C:\Users\Govind\miniconda3\Library\bin"
```

**Run Extraction**:
```bash
python app.py
```

**Output** (saved to `Output/extracted_fields.json`):
```json
{
  "vendor_name": "INTEGRIA HEALTHCARE (AUSTRALIA) PTY LIMITED",
  "invoice_number": "CN-006991",
  "date": "15/09/2024",
  "Total_Items": 1234.50,
  "Freight": 45.00,
  "Final_Amount": 1834.50,
  "GST": 10.00
}
```

### 2️⃣ Manual Field Mapping (Web UI)

**Launch the web interface**:
```bash
python main.py
```

**Steps**:
1. Navigate to `http://localhost:8000` in your browser
2. Invoice image appears on canvas
3. Draw boxes around fields (drag mouse to create rectangles)
4. Enter the field name (e.g., "invoice_number")
5. Click "Save" to store coordinates
6. Coordinates are saved in `FieldLearningMap.json`

### 3️⃣ Validation Workflow

The system performs **automatic validation** checking:
Template Learning System

**How the System "Learns"** (Note: This is **template storage**, not model training):
1. User manually maps fields once per vendor/template via web UI
2. Coordinates are **stored** (not learned by ML model) in `FieldLearningMap.json`
3. Future invoices **reuse** saved coordinates for faster extraction
4. New vendors trigger manual mapping workflow
5. ⚠️ **Important**: The DocTR OCR model itself is pre-trained and doesn't retrain on your datatracted text | Trigger manual UI |

**Example**:
```
⚠️ Post-extraction validation detected issues:
 - Total_Items matches Freight, suspicious
 - GST is missing (None)
Fields reset to None where applicable. Re-validation required.
```

### 4️⃣ Learning from Vendors

**How the System Learns**:
1. User manually maps fields once per vendor/template
2. Coordinates stored in `FieldLearningMap.json`
3. Future invoices use saved coordinates (faster extraction)
4. New vendors trigger manual mapping workflow

**Example `FieldLearningMap.json`**:
```json
{
  "INTEGRIA HEALTHCARE (AUSTRALIA) PTY LIMITED": {
    "template_001": {
      "invoice_number": {"x": 100, "y": 200, "width": 150, "height": 30},
      "date": {"x": 100, "y": 250, "width": 150, "height": 30},
      "Final_Amount": {"x": 500, "y": 1485, "width": 200, "height": 40}
    }
  }
}
```

---

## 🔌 API Endpoints

### GET `/`
Serve the main web interface
```bash
curl http://localhost:8000/
```

### POST `/upload`
Upload and process an invoice (if implemented)
```bash
curl -X POST -F "file=@invoice.pdf" http://localhost:8000/upload
```

### GET `/image/{filename}`
Retrieve converted PDF as PNG
```bash
curl http://localhost:8000/image/CN-006991.pdf
```

### POST `/field_data`
Submit manually drawn field coordinates
```bash
curl -X POST http://localhost:8000/field_data \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_name": "VENDOR_NAME",
    "template_id": "001",
    "field_name": "invoice_number",
    "coords": {"x": 100, "y": 200, "width": 150, "height": 30}
  }'
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file (optional):
```bash
PDF_POPPLER_PATH=C:\Program Files\poppler-24.08.0\Library\bin
OCR_MODEL=doctr_db_resnet50  # or your preferred model
OUTPUT_DIR=./Output
```

### Model Configuration
In `src/Invoice_Extraction.py`:
```python
# Load OCR model (first run downloads ~500MB)
model = ocr_predictor(pretrained=True)

# Use GPU (if available)
# model = ocr_predictor(pretrained=True, device='cuda')
```

### Field Regex Patterns
Customize in `src/SelfLearninValidation.py`:
```python
FIELD_REGEX = {
    "invoice_number": r"(CN-\d+)",           # Match CN-XXXXXX
    "date": r"(\d{2}/\d{2}/\d{4})",         # Match DD/MM/YYYY
    "Total_Items": r"([-+]?\d+\.\d{2})",    # Match currency amounts
    "Final_Amount": r"([-+]?\d+\.\d{2})",
    "GST": r"(\d+\.\d{2})\s*%"              # Match percentage
}
```

---

## 🐛 Troubleshooting

### Issue: "Poppler not found"
**Solution**:
```bash
# Option 1: Add to system PATH
# OR modify in code:
poppler_path = r"C:\actual\path\to\poppler\bin"

# Option 2: Install via conda
conda install -c conda-forge poppler
```

### Issue: "OCR Model Download Fails"
**Solution**:
```bash
# Manual model download
python -c "from doctr.models import ocr_predictor; ocr_predictor(pretrained=True)"

# Check internet connection and disk space (~2GB)
```

### Issue: "PDF has no text"
**Possible Causes**:
- PDF is image-based (scanned document)
- PDF is encrypted
- **Solution**: OCR will still work! DocTR extracts from images

### Issue: "Coordinates produce wrong text"
**Solution**:
1. Check image orientation (landscape vs portrait)
2. Verify coordinates in pixels (use browser DevTools)
3. Re-map field in web UI for accuracy
4. Check if PDF has multiple pages (system uses page 1 only)

### Issue: "JSON save fails"
**Solution**:
```bash
# Check output directory exists
mkdir Output

# Check write permissions
ls -la Output/
```

---

## 📊 Supported Invoice Fields

| Field | Format | Example | Required |
|-------|--------|---------|----------|
| `vendor_name` | String | INTEGRIA HEALTHCARE PTY | ✅ Yes |
| `invoice_number` | String (CN-XXXXX) | CN-006991 | ✅ Yes |
| `date` | DD/MM/YYYY | 15/09/2024 | ✅ Yes |
| `store_name` | String | SYDNEY STORE | ✅ Yes |
| `store_id` | String/Number | S001 | ✅ Yes |
| `Total_Items` | Float | 1234.56 | ❌ No |
| `Freight` | Float | 45.00 | ❌ No |
| `Final_Amount` | Float | 1834.50 | ✅ Yes |
| `GST` | Float | 10.00 | ❌ No |
| `type` | String | Credit adjustment note | ❌ No |

---

## 🔄 Workflow Example

```python
# 1. Extract text from invoice
extracted = extract_invoice_fields(full_text)
# Output: {vendor_name: "...", invoice_number: "CN-006991", ...}

# 2. Validate data quality
needs_validation = validate_numeric_fields(extracted)
# Output: True (if issues found), False (if all OK)

# 3. Use learned coordinates to re-extract missing fields
improved = Extract_using_coordinates(extracted, pdf_path)
# Output: {vendor_name: "...", invoice_number: "CN-006991", Final_Amount: 1834.50}

# 4. Final validation pass
final_status = validate_numeric_fields(improved)
# Output: False (all fields valid!) or True (still issues)

# 5. Save results
with open("Output/extracted_fields.json", "w") as f:
    json.dump(improved, f, indent=2)
```

---

## 📈 Performance Notes

| Operation | Time | Memory |
|-----------|------|--------|
| PDF → Image | 1-3 sec | ~200MB |
| OCR (first run) | 10-30 sec | ~2GB |
| OCR (subsequent) | 5-10 sec | ~1GB |
| Field extraction | <1 sec | ~50MB |
| Validation | <1 sec | ~10MB |
| **Total per invoice** | **10-45 sec** | **~2GB** |

**Optimization Tips**:
- Use GPU for OCR: `model = ocr_predictor(pretrained=True, device='cuda')`
- Pre-process images to grayscale
- Batch process multiple invoices
- Cache coordinates in `FieldLearningMap.json`

---

## 🤝 Contributing

To extend this project:

1. **Add new field types**:
   ```python
   # In src/Invoice_Extraction.py
   data["my_field"] = None
   my_match = re.search(r"MY_PATTERN", full_text_clean)
   ```

2. **Improve extraction**:
   ```python
   # Add more specific regex patterns
   # or use named entity recognition (NER)
   ```

3. **Add new validators**:
   ```python
   def validate_custom_field(data):
       # Your validation logic
       pass
   ```

4. **Support more vendors**:
   - Create new templates in `FieldLearningMap.json`
   - Test with sample invoices
   - Document coordinate positions

---

## 📞 Support & Contact

For issues or questions:
1. Check **Troubleshooting** section above
2. Review error messages in console output
3. Check Python/library versions match requirements
4. Review `Output/extracted_fields.json` for partial results

---

## 📜 License

This project uses:
- **DocTR**: Apache 2.0
- **FastAPI**: MIT
- **Pillow**: HPND

See individual libraries for license details.

---
� Machine Learning Details

### Current ML Usage
- **DocTR**: Pre-trained OCR model (ResNet50 backbone)
- **PyTorch/TensorFlow**: Backend for OCR inference
- **scikit-learn**: Available but currently unused (can be used for field clustering)

### Why Not Full Model Retraining?
1. **Speed**: Pre-trained models are faster than retraining
2. **Data**: Would need 100s of labeled invoices to improve upon pre-trained model
3. **Complexity**: Retraining adds maintenance overhead
4. **Trade-off**: Current approach balances accuracy vs. implementation simplicity

### Potential ML Enhancements
- Fine-tune DocTR on your specific invoice format
- Use Named Entity Recognition (NER) for intelligent field detection
- Build classifier to detect invoice type/vendor automatically
- Train clustering model to group similar fields

---

## 🚀 Future Enhancements

- [ ] Fine-tune DocTR model on custom invoice dataset
- [ ] Add Named Entity Recognition (NER) for automatic field identification
- [ ] Support for multi-page invoices
- [ ] Batch processing with progress tracking
- [ ] Database storage for historical data
- [ ] ML-based vendor auto-detection (classifier)
- [ ] Confidence scores for extracted fields
- [ ] Invoice comparison/reconciliation
- [ ] Mobile app for field validation
- [ ] Export to CSV/Excel formats
- [ ] Active learning: auto-flag uncertain extractionacted fields
- [ ] Export to CSV/Excel formats

---

**Last Updated**: February 2026  
**Version**: 1.0  
**Status**: ✅ Stable
