# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

cascades_url = "https://www.equityapartments.com/seattle/south-lake-union/cascade-apartments##bedroom-type-section-1"

page = requests.get(cascades_url)

soup = BeautifulSoup(page.content, 'html.parser')

rows = soup.find_all("li", class_="list-group-item row unit")

for row in rows:
    pricing = row.find("span", class_="pricing").text
    time_period = row.find("span", class_="time-period").text
    row_text = row.text
    avail_idx_start = row_text.find("Available") + len("Available") + 1
    avail_len = row_text[avail_idx_start:].find("2020") + len("2020")
    availability = row_text[avail_idx_start:avail_idx_start+avail_len]
    sq_ft_start = row_text.find("sq.ft.") - len("XXXX ")
    sq_ft = row_text[sq_ft_start:sq_ft_start + len("XXXX")].strip()
    floor_start = row_text.find("Floor") + len("Floor") + 1
    floor = row_text[floor_start:floor_start+1]
    # print("row_text = " + str(row_text))
    print("pricing = " + str(pricing))
    print("time period = " + str(time_period))
    print("availability = " + str(availability))
    print("sq ft = " + sq_ft)
    print("floor = " + floor)
    # print(row)
    print("------------------------------------------------------------------------------------")

