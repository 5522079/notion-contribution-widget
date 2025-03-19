import os
import csv

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()
user_name = os.getenv('USER_NAME')
url = "https://github.com/users/" + str(user_name) + "/contributions"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
days = soup.find_all("td", {"class": "ContributionCalendar-day"})

contributions = []
for day in days:
    date = day.get("data-date")
    
    tooltip = day.find_next("tool-tip")
    if tooltip:
        tooltip_text = tooltip.text.strip()
        if "No contributions" in tooltip_text:
            cnt = 0
        else:
            cnt = int(tooltip_text.split()[0])
    else:
        cnt = 0
    
    if date:
        contributions.append((date, cnt))

contributions.sort(key=lambda x: x[0])

file_path = './data/contributions.csv'

with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    for date, cnt in contributions:
        writer.writerow([date, cnt])
