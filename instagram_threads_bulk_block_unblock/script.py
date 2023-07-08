# You can also print your user list and block them one by one manually
import pandas
import os

count = 0

absolute_path = os.path.dirname(__file__)
relative_path = "list/users.xlsx"
full_path = os.path.join(absolute_path, relative_path)
excel_data = pandas.read_excel(full_path, sheet_name="List")

for column in excel_data["usernames"].tolist():
    url = "https://www.instagram.com/" + str(excel_data["usernames"][count])
    count = count + 1
    print(url)
