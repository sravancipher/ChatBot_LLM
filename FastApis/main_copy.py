import google.generativeai as genai
import json
import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import spacy
import pandas as pd
from pdfminer.high_level import extract_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


from typing import Optional

genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")


nlp = spacy.load("en_core_web_sm")


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
textfromeach = []

def scrape_website(url):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service("E:/GenAi/FastApis/chromedriver.exe"), options=chrome_options)

    try:
        driver.get(url)
        try:
            close_popup = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
            close_popup.click()
        except:
            pass


        static_content = []
        static_elements = driver.find_elements(By.XPATH, "//div | //span | //a | //h1 | //h2 | //h3 | //p")
        for element in static_elements:
            try:
                text = element.text.strip()
                if text:
                    static_content.append(text)
            except Exception:
                continue  


        dynamic_content = set()
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                elements = driver.find_elements(By.XPATH, "//div | //span | //a | //h1 | //h2 | //h3 | //p")
                for element in elements:
                    try:
                        text = element.text.strip()
                        if text:
                            dynamic_content.add(text)
                    except Exception:
                        continue  

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            except Exception:
                break 

        driver.quit()
        print("-------------------------------------")
        print("static_content",type(static_content))
        print("-------------------------------------")
        return {
            "text": url,
            "content": ' '.join(static_content),
            
        }

    except Exception as e:
        driver.quit()
        return {"error": str(e)}


def handle_image_upload(file_path):
    reader = easyocr.Reader(['ch_sim', 'en'])
    result = reader.readtext(file_path, detail=0)
    extracted_text = ' '.join([item for item in result])
    doc = nlp(extracted_text)
    print("Named Entities, Phrases, and Concepts:")
    for ent in doc.ents:
        print(ent.text, ent.label_)

    print("\nPart-of-Speech tagging:")
    for token in doc:
        print(token.text, token.pos_)

    print("\nLemmas:")
    for token in doc:
        print(token.text, token.lemma_)

    print("\nSentences:")
    for sent in doc.sents:
        print(sent.text)
    return {"type": "image_text", "content": sent.text}

def handle_pdf_upload(file_path):
    text = extract_text(file_path)
    return {"type": "pdf_text", "content": text}

def handle_excel_upload(file_path):
    df = pd.read_excel(file_path)
    text = df.to_string(index=False)
    return {"type": "excel_text", "content": text}

def handle_csv_upload(file_path):
    df = pd.read_csv(file_path)
    text = df.to_string(index=False)
    return {"type": "csv_text", "content": text}

def handle_txt_upload(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return {"type": "txt_text", "content": text}


def handle_question(query):
    response = model.generate_content(query)
    return {"type": "query_response", "content": response.text}


def handle_code_generation(description):
    response = model.generate_content(description)
    return {"type": "code_response", "content": response.text}


def handle_text_and_image(text: str, file_path: str):
    # Extract text from the image using OCR
    # reader = easyocr.Reader(['ch_sim', 'en'])
    # image_text = reader.readtext(file_path, detail=0)
    print("file_path",file_path)
    # Generate output based on the combined text
    response = model.generate_content(["Write a short, engaging blog post based on this picture.",file_path])
    print(response.text)
    return {
        "type": "text_and_image_response",
        # "input_text": text,
        # "extracted_image_text": image_text,
        "content": response.text,
    }


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
    if(query.startswith("https") or query.startswith("http")):
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
        print("contents",contents)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)

        # Handle combined text and file input
        # if file_ext in ["jpg", "jpeg", "png"]:
        #     response = handle_image_upload(file_path)
        # elif file_ext == "pdf":
        #     response = handle_pdf_upload(file_path)
        # elif file_ext == "xlsx":
        #     response = handle_excel_upload(file_path)
        # elif file_ext == "csv":
        #     response = handle_csv_upload(file_path)
        # elif file_ext == "txt":
        #     response = handle_txt_upload(file_path)


        combined_response = handle_text_and_image(query, file_path)
        return {"data": combined_response}


    if file:
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
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)


        if file_ext in ["jpg", "jpeg", "png"]:
            response = handle_image_upload(file_path)
        elif file_ext == "pdf":
            response = handle_pdf_upload(file_path)
        elif file_ext == "xlsx":
            response = handle_excel_upload(file_path)
        elif file_ext == "csv":
            response = handle_csv_upload(file_path)
        elif file_ext == "txt":
            response = handle_txt_upload(file_path)

        return {"data": response["content"]}


    return {"data": "No valid input provided"}
