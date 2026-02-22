import json
import re
import os
import numpy as np

# ------------------------ 1. Configurable Field Regex -------------------------
FIELD_REGEX = {
    "invoice_number": r"(CN-\d+)",
    "date": r"(\d{2}/\d{2}/\d{4})",
    "Total_Items": r"([-+]?\d+\.\d{2})",
    "Freight": r"([-+]?\d+\.\d{2})",
    "Final_Amount": r"([-+]?\d+\.\d{2})",
    "GST": r"(\d+\.\d{2})\s*%",
    # Add more if needed...
}
# ------------------------------------------------------------------------------

class SelfLearningValidator:
    def __init__(self, doc, pil_images, vendor_name, pdf_path, field_map_path="FieldLearningMap.json"):
        self.doc = doc
        self.images = pil_images
        self.vendor = vendor_name
        self.pdf_path = pdf_path
        self.field_map_path = field_map_path
        self.field_map = self._load_field_map()

    def _load_field_map(self):
        if os.path.exists(self.field_map_path):
            return json.load(open(self.field_map_path))
        return {}

    def _extract_text_by_coords(self, image, coords, model):
        x, y, w, h = coords["x"], coords["y"], coords["width"], coords["height"]
        cropped = image.crop((x, y, x + w, y + h))
        cropped_array = np.array(cropped.convert("RGB"))
        cropped_doc = model([cropped_array])
        lines = cropped_doc.pages[0].export()['blocks'][0]['lines']
        return " ".join(word["value"] for line in lines for word in line["words"])

    def validate_and_extract(self, required_fields, model):
        if not self.vendor or self.vendor not in self.field_map:
            print(f"❌ No template data found for vendor: {self.vendor}")
            return required_fields

        updated = False
        for field, value in required_fields.items():
            if value is not None or field == "vendor_name":
                continue  # already filled or not applicable

            print(f"\n🔍 Trying to auto-extract missing field: {field}")
            found = False

            for template_id, fields in self.field_map[self.vendor].items():
                coords = fields.get(field)
                if not coords:
                    continue

                try:
                    image = self.images[0]  # Assuming 1st page
                    ocr_text = self._extract_text_by_coords(image, coords, model)
                    pattern = FIELD_REGEX.get(field)
                    if pattern:
                        match = re.search(pattern, ocr_text)
                        if match:
                            val = match.group(1)
                            if field in ["invoice_number", "date"]:
                                required_fields[field] = val
                            else:
                                required_fields[field] = abs(float(val))
                            print(f"✅ Extracted {field} using template {template_id}: {required_fields[field]}")
                            found = True
                            updated = True
                            break
                except Exception as e:
                    print(f"⚠️ Error using template {template_id}: {e}")
                    continue

            if not found:
                print(f"⚠️ Manual validation required for: {field}")
                os.system("start cmd /k uvicorn Manual_Validation.main:app --reload")
                break  # let user manually label, re-run this afterward

        return required_fields
