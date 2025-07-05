from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import gspread
import time
from datetime import datetime

# Google Sheet से कनेक्ट (पब्लिक शीट का इस्तेमाल करो)
gc = gspread.service_account(filename='credentials.json')  # नोट: बिना API के भी चलेगा
sheet = gc.open("YouTube_Videos").sheet1

# YouTube अपलोड फंक्शन
def upload_video(video_path, title, description):
    options = Options()
    options.add_argument("--headless")  # बिना GUI के चलेगा
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/upload")
    time.sleep(30)  # मैन्युअल लॉगिन का टाइम
    driver.find_element("xpath", '//input[@type="file"]').send_keys(video_path)
    time.sleep(5)
    driver.find_element("name", "title").send_keys(title)
    driver.find_element("id", "description").send_keys(description)
    driver.find_element("id", "done-button").click()
    driver.quit()

# मेन लूप
records = sheet.get_all_records()
now = datetime.now().strftime("%d %b %I%p")  # e.g., "11 Jul 10AM"

for i, row in enumerate(records, start=2):
    if row["Status"] == "Pending" and row["Upload Time"] == now:
        upload_video(row["Video File"], row["Title"], row["Description"])
        sheet.update_cell(i, 4, "Uploaded")
