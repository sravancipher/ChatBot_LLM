import easyocr
import spacy
import pandas as pd
from pdfminer.high_level import extract_text
from common import context
import google.generativeai as genai
genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")
nlp = spacy.load("en_core_web_sm")

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
    # print("type of text returned by image_upload",type(extract_text))
    context.append(extracted_text)
    # print("after type change",extract_text)
    return {"type": "image_text", "content": extracted_text}
def handle_pdf_upload(file_path):
    text = extract_text(file_path)
    response = model.generate_content("summarize this text in 5 to 10 lines words:"+text)
    context.append(text)
    print("pdf text",type(text), text)
    return {"type": "query_response", "content":response.text,"summarized":text}

    return {"type": "pdf_text", "content": text}


def handle_excel_upload(file_path):
    df = pd.read_excel(file_path)
    text = df.to_string(index=False)
    context.append(text)
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
    cont=""
    if context:
        cont=context[-1]
    print("cont",cont)
    if(find_relevant_context(query, cont)):
        response=model.generate_content("this is the question:"+query+"answer the question using this context:"+cont)
        print("response1",response.text)
        return {"type": "query_response", "content": response.text}
    response = model.generate_content(query)
    print("response2",response.text)
    return {"type": "query_response", "content": response.text}

def find_relevant_context(query, cont):
    wh_words = {"who", "what", "where", "when", "why", "which", "how"}
    doc = nlp(query.lower())
    filtered_keywords = [
        token.text for token in doc if not token.is_stop and token.text not in wh_words
    ]
    for word in filtered_keywords:
        if word.lower() in cont.lower():  
            return cont
    return False

def handle_code_generation(description):
    response = model.generate_content(description)
    return {"type": "code_response", "content": response.text}

