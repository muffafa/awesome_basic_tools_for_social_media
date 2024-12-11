# Program to send bulk messages through WhatsApp web from a text file
# Author @muffafa

import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct file paths
data_file = os.path.join(current_dir, "data.txt")
text_file = os.path.join(current_dir, "text.txt")

#If there is an image
image_path = "/Users/muffafa/Desktop/Muhammed-Mustafa-Savar.jpg"  # Update as needed

# Read phone numbers
with open(data_file, "r", encoding="utf-8") as f:
    numbers = [line.strip() for line in f if line.strip()]

# Read message
with open(text_file, "r", encoding="utf-8") as f:
    message = f.read().strip()

message = message.replace("\n", "%0A")

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
            # # Send text message
            # send_text_btn = WebDriverWait(driver, 35).until(
            #     EC.element_to_be_clickable(
            #         (By.XPATH, "/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button/span")
            #     )
            # )
            # sleep(2)
            # send_text_btn.click()
            # sleep(5)
            # print("Message sent to:", number)

            # Attach image (directly to the file input)
            attach_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[1]/div/button/span",
                    )
                )
            )
            attach_btn.click()
            sleep(2)

            # Directly find the input under "Fotoğraflar ve Videolar"
            photos_videos_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//span[contains(text(),'Fotoğraflar ve Videolar')]/following::input[@type='file'][1]",
                    )
                )
            )
            photos_videos_input.send_keys(image_path)
            sleep(2)

            # After the image preview is displayed, click send
            send_img_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div[3]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span",
                    )
                )
            )
            sleep(2)
            send_img_btn.click()
            sleep(5)
            print("Message sent to:", number)

        except Exception:
            print("Could not send to:", number)
    except Exception as e:
        print("Failed for:", number, str(e))

driver.quit()
print("The script executed successfully.")
