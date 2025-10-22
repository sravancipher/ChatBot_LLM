## 📌 ParaBot — AI Powered File Understanding & Query Assistant

ParaBot is an AI-driven web application built using **FastAPI (Backend)** and **TypeScript + React (Frontend)** that allows users to upload different types of files (PDF, Excel, Image, TXT, CSV) and extract insights, summaries, context-aware answers, or perform OCR-based text recognition. It can also scrape web pages, generate code from descriptions, and handle text + image inputs simultaneously.

---

## 🚀 Features

✅ Ask natural language questions
✅ Upload PDF and get smart AI summary
✅ OCR extraction from Images (EasyOCR)
✅ Read & process Excel (`.xlsx`) and CSV files
✅ TXT parsing and response
✅ Web scraping and summarization (Selenium)
✅ Code generation from plain text description
✅ Combined Image + Text understanding
✅ Context-aware responses using previous extracted text
✅ React + TypeScript frontend UI
✅ FastAPI Backend integrated with Gemini 1.5 Flash model

---

## 🏗️ Tech Stack

| Layer            | Technology                      |
| ---------------- | ------------------------------- |
| Frontend         | React + TypeScript              |
| Backend          | FastAPI (Python)                |
| AI Model         | Gemini 1.5 Flash (Google GenAI) |
| OCR              | EasyOCR                         |
| NLP              | spaCy                           |
| Scraping         | Selenium (ChromeDriver)         |
| Document Parsing | PDFMiner, pandas, openpyxl      |

---

## 📁 Supported Inputs

| Input Type   | Handled By                 | Result                        |
| ------------ | -------------------------- | ----------------------------- |
| Text         | `handle_question()`        | AI generated answer           |
| PDF          | `handle_pdf_upload()`      | Summarization + store context |
| Image        | `handle_image_upload()`    | OCR + entity extraction       |
| Excel        | `handle_excel_upload()`    | Row→Text + store context      |
| CSV          | `handle_csv_upload()`      | Row→Text                      |
| TXT          | `handle_txt_upload()`      | Raw text extraction           |
| URL          | `scrape_website()`         | Scrape + summarize            |
| Text + Image | `handle_text_and_image()`  | Combined understanding        |
| Description  | `handle_code_generation()` | Code generation               |

---

## 🔄 API Workflow

```
POST /process_input/

Request Body (form-data):
- query?: string  (text input)
- description?: string  (for code generation)
- file?: UploadFile     (pdf/image/excel/txt/csv)
- url?: string          (website scraping)

Backend selects proper route based on combination.
```

---

## 📦 Installation (Backend)

```bash
git clone <repo-url>
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🌐 Frontend Setup (TypeScript + React)

```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 Context Memory

After each file upload, extracted text is stored in `context[]`.
Future questions are answered using context awareness.

Example:

> Upload PDF → ask question → ParaBot answers referring to uploaded PDF.

---

## 🧑‍💻 Developer Notes

* File is deleted after processing
* Context persists only in runtime
* Supports cross-origin only from `http://localhost:5173`
* ChromeDriver path must be correctly set
* Gemini 1.5 Flash is used for summarization and generation

---

## 🛣️ Roadmap (Future Enhancements)

* User-based persistent context storage (DB)
* Authentication + user session history
* Multi-file context aggregation
* Downloadable summaries
* Chat-style UI improvement
