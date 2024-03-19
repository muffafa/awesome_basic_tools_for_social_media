import random
import time
import pandas

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
    print("Trying to message user: " + user)
    time.sleep(2)

    # Click message button and message user
    try:
        click_btn = WebDriverWait(driver, 35).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div",
                )
            )
        )
    except Exception as e:
        print("Sorry could not find message button")
    else:
        time.sleep(2)
        click_btn.click()
        time.sleep(15)
        try:
            active_element = driver.switch_to.active_element
            actions = ActionChains(driver)
            mes_text = f"""Sizi, Türkiye genelindeki teknoloji ve inovasyon alanlarında faaliyet gösteren toplulukları bir araya getirdiğimiz, birleştirici ve iş birlikçi ağımız “Harekete Geç” programımıza davet ediyoruz 🥳 Programlarımız tamamen ücretsizdir ve Temmuz ayına kadar devam edecekler 🚀 Siz de topluluğunuzla birlikte bu dinamik ağın bir parçası olmak ve dijital medya sponsorluğu, topluluklara özel buluşmalar ve etkinlikler, eğitmen ve konuşmacı desteği gibi birçok avantajdan faydalanmak istiyorsanız; programın detaylarını, sunacağımız fırsatları ve sizin için hazırladığımız faydaları keşfetmek üzere bu mesaja "Harekete Geç" yazarak dönüş yapın."""
            actions.send_keys(mes_text).perform()
            actions.send_keys(Keys.RETURN).perform()
        except Exception as e:
            print(
                "Sorry could not find the block button after clicking the block button"
            )
        else:
            time.sleep(random.randrange(10, 20))
            print("Messaged user: " + user)

driver.quit()
print("The script executed successfully.")
