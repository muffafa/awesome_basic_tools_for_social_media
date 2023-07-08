import time
import pandas

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

count = 0
excel_data = pandas.read_excel("users.xlsx", sheet_name="List")

# Open Chrome and maximize window
driver = webdriver.Chrome()
driver.maximize_window()

# Login to Instagram
driver.get("https://www.instagram.com")
input("Press ENTER after login into Instagram")

for column in excel_data["usernames"].tolist():
    user = str(excel_data["usernames"][count])
    url = "https://www.instagram.com/" + user
    driver.get(url)
    count = count + 1
    print("Trying to unblock user: " + user)
    time.sleep(2)

    # Click unblock button and unblock user
    try:
        click_btn = WebDriverWait(driver, 35).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text() = 'Unblock']"))
        )
    except Exception as e:
        print("Sorry could not find the unblock")
    else:
        time.sleep(2)
        click_btn.click()
        try:
            click_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[@class='xjbqb8w xaqea5y x1b1mbwd xav7gou xtuw4uo x1ypdohk xvs91rp x1evy7pa xdj266r x11i5rnm xat24cr x1mh8g0r x1wxaq2x x1iorvi4 x1sxyh0 xjkvuk6 xurb0ha x2b8uid x87ps6o xxymvpz xh8yej3 x52vrxo x4gyw5p xkmlbd1 x1xlr1w8']",
                    )
                )
            )
        except Exception as e:
            print("Sorry could not find the Unblock button")
        else:
            time.sleep(2)
            click_btn.click()
            time.sleep(1)
            print("Unblocked user: " + user)

driver.quit()
print("The script executed successfully.")
