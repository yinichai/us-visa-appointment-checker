import requests
from bs4 import BeautifulSoup
import time
import configparser
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

MONTH = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

config = configparser.ConfigParser()
config.read('config.ini')

schedule_id = config['DEFAULT']['SCHEDULE_ID']
country = config['DEFAULT']['COUNTRY_CODE']
city = config['DEFAULT']['CITY']
session = config['DEFAULT']['SESSION_ID'] 
user_agent = config['DEFAULT']['USER_AGENT'] 


def refresh(country_code, schedule_id, session):
    req = requests.Session()
    headers = {
        "User-Agent": user_agent,
        "Referer": "https://ais.usvisa-info.com/%s/niv/schedule/%s/continue_actions" % (country_code, schedule_id),
        "Cookie": "_yatri_session=" + session

    }
    r = req.get("https://ais.usvisa-info.com/%s/niv/schedule/%s/payment" % (country_code, schedule_id), headers=headers)
    if r.status_code != 200:
        print("Error")
    soup = BeautifulSoup(r.text, "html.parser")
    time_table = soup.find("table", {"class": "for-layout"})
    result = []
    
    if time_table:
        for tr in time_table.find_all("tr"):
            tds = tr.find_all("td")
            if not len(tds) == 2:
                continue
            place = tds[0].text
            date_str = tds[1].text
            s = date_str.split()
            year, month, day = 0, 0, 0
            if len(s) >= 3 and s[0] != "No":
                day_str, month_str, year_str = s[-3], s[-2].replace(",", ""), s[-1]
                year, month, day = int(year_str), MONTH[month_str], int(day_str)
            result.append([place, (year, month, day)])
            if year == 2024 and month == 1 and place in [city]:
                print("\a")
            # add your condition here
            # trigger an alarm when a slot is found
    session = r.cookies["_yatri_session"]
    return result, session



if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        print(now)
        result, session = refresh(country, schedule_id, session)
        print(result)
        time.sleep(120) # sleep 2 min
