from src.Invoice_Extraction import extract_invoice_fields, validate_numeric_fields, validate_numeric_fields, load_field_map, extract_text_by_coords, Extract_using_coordinates
from src.Invoice_Extraction import full_text, pdf_path
import json, os

if __name__ == "__main__":

    required_fields = extract_invoice_fields(full_text)
    needs_validation = validate_numeric_fields(required_fields)
    required_fields_post_validation = Extract_using_coordinates(required_fields, pdf_path)
    validation_status = validate_numeric_fields(required_fields)
    print(required_fields)
    print(needs_validation)
    print(required_fields_post_validation)
    
    os.makedirs("Output", exist_ok=True)
    with open("Output/extracted_fields.json", "w") as f: json.dump(required_fields_post_validation, f, indent=2)