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
    print("Trying to block user: " + user)
    time.sleep(2)

    # Click options button and block user
    try:
        click_btn = WebDriverWait(driver, 35).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha']//div[@class='x6s0dn4 x78zum5 xdt5ytf xl56j7k']//*[name()='svg']",
                )
            )
        )
    except Exception as e:
        print("Sorry could not find the options button")
    else:
        time.sleep(2)
        click_btn.click()
        try:
            click_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[text() = 'Block']",
                    )
                )
            )
        except Exception as e:
            print("Sorry could not find the block button")
        else:
            time.sleep(2)
            click_btn.click()
            try:
                click_btn = WebDriverWait(driver, 35).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[text() = 'Block']",
                        )
                    )
                )
            except Exception as e:
                print(
                    "Sorry could not find the block button after clicking the block button"
                )
            else:
                time.sleep(2)
                click_btn.click()
                time.sleep(1)
                print("Blocked user: " + user)

driver.quit()
print("The script executed successfully.")
