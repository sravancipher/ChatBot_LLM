import google.generativeai as genai
genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")
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
