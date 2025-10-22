
import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from handle_uploads import handle_code_generation,handle_csv_upload,handle_excel_upload,handle_image_upload,handle_pdf_upload,handle_question,handle_txt_upload
from scrape_website import scrape_website
from handle_text_image import handle_text_and_image
from common import context
from pathlib import Path
# print("context",context)
app = FastAPI()
origins = [
    "http://localhost:5173",  
]
app.add_middleware(
    CORSMiddleware,
    
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


imagedir = "images/"
pdfdir = "pdfs/"
exceldir = "excels/"
txtdir = "texts/"
csvdir = "csv/"


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.post("/process_input/")
async def process_input(
    query: Optional[str] = Form(None), 
    description: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None), 
    url: Optional[str] = Form(None)
):
    print(f"Received request: query={query}, description={description}, file={file}, url={url}")
    if(query!=None and (query.startswith("https") or query.startswith("http"))):
        url=query
        query=None
    
    if query and not file:
        response = handle_question(query)
        return {"data": response["content"]}


    if description and not file:
        response = handle_code_generation(description)
        return {"data": response["content"]}


    if url:
        response = scrape_website(url)
        return {"data": response}


    if query and file:

        file_ext = file.filename.split(".")[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        if file_ext in ["jpg", "jpeg", "png"]:
            file_path = f"{imagedir}{unique_filename}"
        elif file_ext == "pdf":
            file_path = f"{pdfdir}{unique_filename}"
        elif file_ext == "xlsx":
            file_path = f"{exceldir}{unique_filename}"
        elif file_ext == "csv":
            file_path = f"{csvdir}{unique_filename}"
        elif file_ext == "txt":
            file_path = f"{txtdir}{unique_filename}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        contents = await file.read()
        # print("contents",contents)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)
        combined_response = handle_text_and_image(query, file_path)
        file_path = Path(file_path)
        file_path.unlink()
        return {"data": combined_response}


    if file:
        file_ext = file.filename.split(".")[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        if file_ext in ["jpg", "jpeg", "png"]:
            file_path = f"{imagedir}{unique_filename}"
        elif file_ext == "pdf":
            file_path = f"{pdfdir}{unique_filename}"
        elif file_ext in ["xlsx", "xls"]:
            file_path = f"{exceldir}{unique_filename}"
        elif file_ext == "csv":
            file_path = f"{csvdir}{unique_filename}"
        elif file_ext == "txt":
            file_path = f"{txtdir}{unique_filename}"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        contents = await file.read()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)


        if file_ext in ["jpg", "jpeg", "png"]:
            response = handle_image_upload(file_path)
        elif file_ext == "pdf":
            response = handle_pdf_upload(file_path)
        elif file_ext in ["xlsx", "xls"]:
            response = handle_excel_upload(file_path)
        elif file_ext == "csv":
            response = handle_csv_upload(file_path)
        elif file_ext == "txt":
            response = handle_txt_upload(file_path)
        file_path = Path(file_path)
        file_path.unlink()
        return {"data": response["content"]}

    
    return {"data": "No valid input provided"}
