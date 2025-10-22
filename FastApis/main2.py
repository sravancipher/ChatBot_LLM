import google.generativeai as genai
import json
import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pdfminer.high_level import extract_text
import easyocr
import spacy
import pandas as pd
import json
import os
# Configure Google Generative AI
genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")

# Load Spacy model for text processing
nlp = spacy.load("en_core_web_sm")

# Initialize FastAPI app
app = FastAPI()
origins = [
    "http://localhost:5173",  # React frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories for storing files
imagedir = "images/"
pdfdir = "pdfs/"
exceldir = "excels/"
txtdir = "texts/"
csvdir = "csv/"
textfromeach=[]
def handle_image_upload(file_path):
    # Image text extraction
    reader = easyocr.Reader(['ch_sim', 'en'])
    result = reader.readtext(file_path, detail=0)
    # textfromeach.append(result)
    return {"type": "image_text", "content": result}

def handle_pdf_upload(file_path):
    # PDF text extraction
    text = extract_text(file_path)
    # textfromeach.append(text)
    return {"type": "pdf_text", "content": text}

def handle_excel_upload(file_path):
    # Excel text extraction
    df = pd.read_excel(file_path)
    text = df.to_string(index=False)
    # textfromeach.append(text)
    return {"type": "excel_text", "content": text}

def handle_csv_upload(file_path):
    # Excel text extraction
    df = pd.read_csv(file_path)
    text = df.to_string(index=False)
    # textfromeach.append(text)
    return {"type": "csv_text", "content": text}

def handle_txt_upload(file_path):
    # TXT file text extraction
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # textfromeach.append(text)
    return {"type": "txt_text", "content": text}

def handle_question(query):
    # Generate response for text query
    response = model.generate_content(query)
    # textfromeach.append(response.text)
    return {"type": "query_response", "content": response.text}

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

class QueryRequest(BaseModel):
    query: str

@app.post("/process_input/")
async def process_input(query: str = None, file: UploadFile = None):
    if query:
        # Handle text query
        return handle_question(query)

    elif file:
        # Save the uploaded file
        file_ext = file.filename.split(".")[-1].lower()
        print("file ext",file_ext)
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        if file_ext in ["jpg", "jpeg", "png"]:
            file_path = f"{imagedir}{unique_filename}"
        elif file_ext == "pdf":
            file_path = f"{pdfdir}{unique_filename}"
        elif file_ext in ["xls", "xlsx"]:
            file_path = f"{exceldir}{unique_filename}"
        elif file_ext in ["csv"]:
            file_path = f"{csvdir}{unique_filename}"
        elif file_ext == "txt":
            file_path = f"{txtdir}{unique_filename}"
        else:
            return {"error": "Unsupported file type"}

        contents = await file.read()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)

        # Process the file based on its type
        if file_ext in ["jpg", "jpeg", "png"]:
            return handle_image_upload(file_path)
        elif file_ext == "pdf":
            return handle_pdf_upload(file_path)
        elif file_ext=="xlsx":
            return handle_excel_upload(file_path)
        elif file_ext =="csv":
            return handle_csv_upload(file_path)
        elif file_ext == "txt":
            return handle_txt_upload(file_path)

    return {"error": "No valid input provided"}




# output_file = "formatted_data.json"
# if os.path.exists(output_file):
#         # Load existing data
#         with open(output_file, "r", encoding="utf-8") as f:
#             data = json.load(f)
# else:
#     # Initialize empty list if file does not exist
#     data = []

#     # Create new input-output pairs
# for i in range(0, len(textfromeach) - 1, 2):  # Pair consecutive lines
#     entry = {
#             "input": textfromeach[i],
#             "output": textfromeach[i + 1]
#         }
#     data.append(entry)

#     # Save updated data back to the file
# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=4)

# print(f"Data saved incrementally to {output_file}")

