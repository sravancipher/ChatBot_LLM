import google.generativeai as genai
import json
genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
# from gemini_flash import GeminiModel, FineTuner, DatasetLoader

# model_name = "gemini-flash-1.5"
# model = GeminiModel.from_pretrained(model_name)
# dataset = DatasetLoader.load_from_file("formatted_data.json")

# # Step 3: Initialize Fine-Tuner
# fine_tuner = FineTuner(
#     model=model,
#     dataset=dataset,
#     output_dir="./fine_tuned_gemini",
#     learning_rate=2e-5,
#     epochs=3,
#     batch_size=16
# )

# # Step 4: Train the Model
# fine_tuner.train()

# # Step 5: Save the Fine-Tuned Model
# model.save_pretrained("./fine_tuned_gemini")

# # Step 2: Load and Tokenize Dataset
# dataset = DatasetLoader.load_from_file("custom_data.json")
@app.post("/readque/")
def read_que(request: QueryRequest):
    # print(query)
    que=request.query
    # model = GeminiModel.from_pretrained("./fine_tuned_gemini")
    # response = model.generate(que)
    response = model.generate_content(que)
    return json.loads(json.dumps(response.text, default=str))

from fastapi import File, UploadFile
import uuid
import os
imagedir="images/"
@app.post("/upload")
async def create_upload_file(file: UploadFile=  File(...)):
    file.filename=f"{uuid.uuid4()}.jpg"
    contents=await file.read()
    with open(f"{imagedir}{file.filename}","wb") as f:
        f.write(contents)
    img=os.listdir(imagedir)
    path=f"{imagedir}{file.filename}"
    print("path:",path)
    response = model.generate_content(
    [
        "Write a short, engaging blog post based on this picture. It should include a description of the picture",
        "images/"+file.filename,
    ]
    
)
    # print("filename",file.filename)
    return json.loads(json.dumps(response.text, default=str))
# imagedir="images/"
# import easyocr
# reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
# result = reader.readtext('images/test.jpg',detail=0)

# print(result)
import easyocr
@app.post("/imgextract")
async def create_upload_file(file: UploadFile=  File(...)):
    file.filename=f"{uuid.uuid4()}.jpg"
    contents=await file.read()
    with open(f"{imagedir}{file.filename}","wb") as f:
        f.write(contents)
    img=os.listdir(imagedir)
    path=f"{imagedir}{file.filename}"
    print("path:",path)
    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    result = reader.readtext("images/"+file.filename,detail=0)
    return result
    # response = model.generate_content("images/"+file.filename,)
    # print("filename",file.filename)
    
from pdfminer.high_level import extract_text
import spacy
nlp = spacy.load("en_core_web_sm")
# text = extract_text("GENAI.pdf")
# print(text)
pdfdir="pdfs/"
@app.post("/pdfxtract")
async def create_upload_file(file: UploadFile=  File(...)):
    file.filename=f"{uuid.uuid4()}.pdf"
    contents=await file.read()
    with open(f"{pdfdir}{file.filename}","wb") as f:
        f.write(contents)
    
    path=f"{pdfdir}{file.filename}"
    print("path:",path)
    text = extract_text("pdfs/"+file.filename)
    #print(text)
    return text
    
    # about_doc = nlp(text)
    # sentences = list(about_doc.sents)
    # print(len(sentences))
    # finaltext=[]
    # for sentence in sentences:
    #     finaltext.append(sentence[:5])
    
    # print(finaltext)
    # return finaltext
    # response = model.generate_content("images/"+file.filename,)
    # print("filename",file.filename)