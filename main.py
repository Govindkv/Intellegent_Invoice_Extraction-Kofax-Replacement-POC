from fastapi import FastAPI, UploadFile, Request 
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pdf2image import convert_from_path
import json, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

image_folder = "Invoices"
map_file = "FieldLearningMap.json"

filename = "CN-006991.pdf"
os.makedirs(image_folder, exist_ok=True)

class FieldData(BaseModel):
    vendor_name: str
    template_id: str
    field_name: str
    coords: dict

# Helper to load/save mappings
def load_mappings():
    if os.path.exists(map_file):
        return json.load(open(map_file))
    return {}

def save_mappings(mappings):
    with open(map_file, "w") as f:
        json.dump(mappings, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, filename: str = filename):
    return templates.TemplateResponse("index.html", {"request": request, "filename": filename})

@app.get("/image/{filename}")
def get_image(filename: str):
    file_path = os.path.join(image_folder, filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        img_path = file_path.replace(".pdf", ".png")
        if not os.path.exists(img_path):
            image_pages = convert_from_path(file_path, dpi=300, poppler_path=r"C:\Program Files\poppler-24.08.0\Library\bin")
            
            file_name = filename.rstrip(".pdf")
            Output_Images_Path = r"C:\Users\Govind\Downloads\Work_And\Self_Learning\Invoice_Extraction_demo\Invoices"
            output_path = os.path.join(Output_Images_Path, f"{file_name}.png")
            image_pages[0].save(output_path, 'PNG')
        return FileResponse(img_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return FileResponse(file_path)

    else:
        return JSONResponse({"error": "Unsupported file type"}, status_code=400)

@app.post("/learn/", response_class=JSONResponse)
async def learn(data: FieldData):
    mappings = load_mappings()

    vendor = data.vendor_name.strip()
    template = data.template_id.strip()
    field = data.field_name.strip()

    if vendor not in mappings:
        mappings[vendor] = {}
    if template not in mappings[vendor]:
        mappings[vendor][template] = {}

    mappings[vendor][template][field] = data.coords
    save_mappings(mappings)

    return {
        "status": "ok",
        "vendor_name": vendor,
        "template_id": template,
        "field_name": field,
        "coords": data.coords
    }
