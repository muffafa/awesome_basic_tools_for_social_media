# Program to send bulk messages through WhatsApp web from a text file
# Author @muffafa

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Read phone numbers from data.txt
with open("data.txt", "r", encoding="utf-8") as f:
    numbers = [line.strip() for line in f if line.strip()]

# Read message from text.txt
with open("text.txt", "r", encoding="utf-8") as f:
    message = f.read().strip()

count = 0

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://web.whatsapp.com")
input(
    "Press ENTER after logging into WhatsApp Web and ensuring your chats are visible."
)

for number in numbers:
    try:
        url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        driver.get(url)
        try:
            click_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button',
                    )
                )
            )
        except Exception:
            print("Sorry, message could not be sent to", number)
        else:
            sleep(2)
            click_btn.click()
            sleep(5)
            print("Message sent to:", number)
        count += 1
    except Exception as e:
        print("Failed to send message to", number, str(e))

driver.quit()
print("The script executed successfully.")
