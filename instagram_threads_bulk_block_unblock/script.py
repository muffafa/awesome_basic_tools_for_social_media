# You can also print your user list and block them one by one manually
import pandas

count = 0
excel_data = pandas.read_excel("users.xlsx", sheet_name="List")

for column in excel_data["usernames"].tolist():
    url = "https://www.instagram.com/" + str(excel_data["usernames"][count])
    count = count + 1
    print(url)
