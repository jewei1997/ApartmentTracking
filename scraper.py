# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import os.path
from os import path
from datetime import date

cascades_url = "https://www.equityapartments.com/seattle/south-lake-union/cascade-apartments##bedroom-type-section-1"
mark8th_url = "https://www.equityapartments.com/seattle/south-lake-union/mark-on-8th-apartments##bedroom-type-section-1"

buildings = {
    "Cascades": cascades_url,
    "MarkOn8th": mark8th_url
}

# Export to csv setup
today = date.today()
formated_date = today.strftime("%m/%d")
header = ("Building", "Floor", "Sqft",
          "Availability", "Price " + formated_date)
data = []
option = "write_new"
filename = "aptPrices.csv"


def parseHTML(buidling_name, building_url):
    # parse HTML setup
    page = requests.get(building_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all("li", class_="list-group-item row unit")

    # get available unit info
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
        bed_start = row_text.find("Bed") - len("X ")
        beds = row_text[bed_start:bed_start+1]
        bath_start = row_text.find("Bath") - len("X ")
        baths = row_text[bath_start:bath_start+1]
        if beds != '1' or baths != '1':
            continue
        # printUnits(pricing, time_period, availability, sq_ft, floor, beds, baths)
        data.append((buidling_name, floor, sq_ft, availability, pricing))


def printUnits(pricing, time_period, availability, sq_ft, floor, beds, baths):
    # print("row_text = " + str(row_text))
    print("pricing = " + str(pricing))
    print("time period = " + str(time_period))
    print("availability = " + str(availability))
    print("sq ft = " + sq_ft)
    print("floor = " + floor)
    print("beds = " + beds)
    print("baths = " + baths)
    # print(row)
    print("------------------------------------------------------------------------------------")


def writer(header, data, filename, option):
    with open(filename, "w", newline="") as csvfile:
        if option == "write":
            apt_prices = csv.writer(csvfile)
            apt_prices.writerow(header)
            for unit in data:
                apt_prices.writerow(unit)
        elif option == "update":
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
        else:
            print("csv option not found")


def updater(filename):
    with open(filename, newline="") as file:
        readData = [row for row in csv.DictReader(file)]
        readData[0]["Price " + formated_date] = ""
        for unit in data:
            if alreadyAdded(unit, readData):
                continue
            else:
                readData.append(unit)
    readHeader = readData[0].keys()
    writer(readHeader, readData, filename, "update")


# if the unit already exists in the csv file, add the newest price to the
# existing row and return true, otherwise return false
def alreadyAdded(unit, readData):
    for row in readData:
        if (row.get("Building") == unit[0] and
            row.get("Floor") == unit[1] and
            row.get("Sqft") == unit[2] and
                row.get("Availability") == unit[3]):
            row['Price ' + formated_date] = unit[4]
            # print("already added!")
            return True
    return False


def main():
    for building in buildings:
        parseHTML(building, buildings[building])
    writer(header, data, filename, "write")
    updater(filename)


if __name__ == "__main__":
    main()
