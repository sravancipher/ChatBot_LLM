import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai
genai.configure(api_key='AIzaSyCyAEXsYuiHHTebbHoaZOVZuOtZc8Zd100')
model = genai.GenerativeModel("gemini-1.5-flash")
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
        static_text=' '.join(static_content)
        response=model.generate_content("From this content summarize with key points if there any important links show them also:"+static_text)
        return {
            "text": url,
            "content": response.text,
            
        }

    except Exception as e:
        driver.quit()
        return {"error": str(e)}

