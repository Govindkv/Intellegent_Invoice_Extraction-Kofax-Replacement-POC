import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import json, re, os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
poppler_path = r"C:\Users\Govind\miniconda3\Library\bin"
#pil_images = convert_from_path(pdf_path, poppler_path=poppler_path)
# Step 1: Convert PDF to PIL images
pdf_path = r"C:\Users\Govind\Downloads\Data_Scientist\Intellegent_Invoice_Extraction\Invoices\CN-006991.pdf"
pil_images = convert_from_path(pdf_path, poppler_path = poppler_path)
output_dir = os.path.join(os.path.dirname(pdf_path), "OCRed")

# Create OCRed folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Step 2: Convert PIL images to RGB NumPy arrays
image_arrays = [np.array(img.convert("RGB")) for img in pil_images]

# Step 3: Load the OCR model
model = ocr_predictor(pretrained=True)

# Step 4: Run OCR on the image arrays
doc = model(image_arrays)

# Step 5: Visualize + Save OCRed image
for i, (page, pil_img) in enumerate(zip(doc.pages, pil_images)):
    draw = ImageDraw.Draw(pil_img)
    
    for block in page.blocks:
        for line in block.lines:
            # Draw bounding box
            points = (np.array(line.geometry) * [pil_img.width, pil_img.height]).flatten()
            draw.rectangle([points[0], points[1], points[2], points[3]], outline="green", width=2)
            # Optional: draw text near box
            text = " ".join([word.value for word in line.words])
            draw.text((points[0], points[1]-10), text, fill="red")
    
    filename = pdf_path.split(sep="\\")[-1].rstrip(".pdf")
    output_path = os.path.join(output_dir, f"{filename}_page_{i+1}_ocred.png")
    pil_img.save(output_path)
    ## print(f"Saved OCRed image: {output_path}")

# <==========================Required_Fields==============================>
full_text = ""
for page in doc.pages:
    for block in page.blocks:
        for line in block.lines:
            full_text += " ".join([word.value for word in line.words]) + "\n"

def extract_invoice_fields(text: str):
    data = {
        "vendor_name": None,
        "store_name": None,
        "store_id": None,
        "bill_to_store_name": None,
        "bill_to_store_id": None,
        "invoice_number": None,
        "date": None,
        "Total_Items": None,
        "Freight": None,
        "Final_Amount": None,
        "GST": None,
        "type": None
    }

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text_clean = " ".join(lines)

    # Vendor
    for line in lines:
        if not data["vendor_name"] and "PTY" in line.upper():
            data["vendor_name"] = line

    # Type
    if "Credit adjustment note" in full_text_clean:
        data["type"] = "Credit adjustment note"

    # Invoice number
    inv_match = re.search(r"(CN-\d+)", full_text_clean)
    if inv_match:
        data["invoice_number"] = inv_match.group(1)

    # Date
    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", full_text_clean)
    if date_match:
        data["date"] = date_match.group(1)

    # Ship To
    ship_match = re.search(r"Ship To:\s*([^\n]+)", text)
    if ship_match:
        ship_line = ship_match.group(1).strip()
        parts = ship_line.split()
        if len(parts) >= 2:
            data["store_id"] = parts[-1]
            data["store_name"] = " ".join(parts[:-1])

    # Payer
    payer_match = re.search(r"Payer:\s*([^\n]+)", text)
    if payer_match:
        payer_line = payer_match.group(1).strip()
        parts = payer_line.split()
        if len(parts) >= 2:
            data["bill_to_store_id"] = parts[-1]
            data["bill_to_store_name"] = " ".join(parts[:-1])

    # Sub total
    sub_match = re.search(r"TOTAL ITEMS.*?AUD\s*([-+]?\d+\.\d{2})", full_text_clean)
    if sub_match:
        data["Total_Items"] = abs(float(sub_match.group(1)))

    # GST
    gst_match = re.search(r"GST.*?(\d+\.\d{2})\s*%", full_text_clean, re.DOTALL)
    if gst_match:
        data["GST"] = abs(float(gst_match.group(1)))

    # Freight
    freight_match = re.search(r"Freight.*?AUD\s*([-+]?\d+\.\d{2})", full_text_clean)
    if freight_match:
        data["Freight"] = abs(float(freight_match.group(1)))

    # Final total
    final_match = re.search(r"Final Amount.*?AUD\s*([-+]?\d+\.\d{2})", full_text_clean)
    if final_match:
        data["Final_Amount"] = abs(float(final_match.group(1)))

    return data

def validate_numeric_fields(data):
    issues = []

    if data is None:
        # By default, assume all numeric-looking fields must be present
        data = []

    # Detect missing required numeric fields
    for field in data:
        if data.get(field) is None:
            issues.append(f"{field} is missing (None)")

    # Gather extracted numeric fields (ignore None)
    numeric_fields = {k: v for k, v in data.items() if isinstance(v, (int, float)) and v is not None}

    # Compare for suspicious equality
    keys = list(numeric_fields.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            k1, k2 = keys[i], keys[j]
            if numeric_fields[k1] == numeric_fields[k2]:
                issues.append(f"{k1} matches {k2}, suspicious")
                data[k1] = None
                data[k2] = None

    if issues:
        print("⚠️ Post-extraction validation detected issues:")
        for issue in issues:
            print(f" - {issue}")
        print("Fields reset to None where applicable. Re-validation required.")
        return True
    else:
        print("✅ Post-extraction validation passed.")
        return False

def extract_line_Items():
    return None

## <===================================Manual Validation====================================>

def load_field_map(json_path="FieldLearningMap.json"):
    if os.path.exists(json_path):
        return json.load(open(json_path))
    return {}

def extract_text_by_coords(image, coords):
    x, y, w, h = coords["x"], coords["y"], coords["width"], coords["height"]
    cropped = image.crop((x, y, x + w, y + h))
    return model([np.array(cropped.convert("RGB"))]).pages[0].export()['blocks'][0]['lines']


def Extract_using_coordinates(required_fields, pdf_path):
    vendor = required_fields.get("vendor_name")
    if not vendor:
        print("❌ Vendor name missing. Cannot proceed.")
        return required_fields

    field_map = load_field_map()

    # 🚨 Handle empty or missing vendor early
    if not field_map or vendor not in field_map:
        print(f"❌ No template or FieldLearningMap found for vendor: {vendor}")
        fields_to_validate = [k for k, v in required_fields.items() if v is None and k != "vendor_name"]
        print("🧾 The following fields need manual validation:", ", ".join(fields_to_validate))
        print("⚠️ Launching Manual Validation App...")
        os.system("start cmd /k uvicorn main:app --reload")
        return required_fields

    # Convert PDF to image (first page only)
    images = pil_images #convert_from_path(pdf_path, poppler_path=poppler_path)
    image = images[0]

    # Centralized regexes
    field_regex = {
        "invoice_number": r"(CN-\d+)",
        "date": r"(\d{2}/\d{2}/\d{4})",
        "Total_Items": r"TOTAL\s*ITEMS(?:\s|\n|\r)+(?:[A-Z]+\s*)*([-+]?\d+\.\d{2})",
        "Freight": r"Freight(?:\s|\n|\r)+(?:[A-Z]+\s*)*([-+]?\d+\.\d{2})",
        "Final_Amount": r"Final\s*Amount(?:\s|\n|\r)+(?:[A-Z]+\s*)*([-+]?\d+\.\d{2})",
        "GST": r"GST\s*(\d+\.\d{2})\s*%\s*[\d\s.]*AUD\s*([-+]?\d+\.\d{2})"
    }

    for field, value in required_fields.items():
        if value is not None or field == "vendor_name":
            continue  # Already extracted

        print(f"🔍 Trying to auto-extract missing field: {field}")
        found = False

        for template_id, fields in field_map.get(vendor, {}).items():
            coords = fields.get(field)
            if not coords:
                continue

            try:
                ocr_lines = extract_text_by_coords(image, coords)
                combined_text = " ".join(word['value'] for line in ocr_lines for word in line['words'])

                pattern = field_regex.get(field)
                if pattern:
                    match = re.search(pattern, combined_text)
                    if match:
                        val = match.group(1)
                        required_fields[field] = val if field in ["invoice_number", "date"] else abs(float(val))
                        print(f"✅ Extracted {field}: {required_fields[field]} using template: {template_id}")
                        found = True
                        break
            except Exception as e:
                print(f"⚠️ Failed with template {template_id} for field {field}: {e}")

        if not found:
            # print(f"⚠️ Manual validation required for: {field}")
            # print("⚠️ Launching Manual Validation App...")
            # os.system("start cmd /k uvicorn main:app --reload")
            break  # pause here for user action

    return required_fields


required_fields = extract_invoice_fields(full_text)
needs_validation = validate_numeric_fields(required_fields)
required_fields_post_validation = Extract_using_coordinates(required_fields, pdf_path)
validation_status = validate_numeric_fields(required_fields)
print(required_fields)
print(needs_validation)
print(required_fields_post_validation)