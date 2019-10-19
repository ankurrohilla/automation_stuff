from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import pandas as pd
import time
import os

base_path = os.getcwd()

t1 = time.perf_counter()
chroptions = webdriver.ChromeOptions()
chroptions.add_argument(argument='headless')
driver = webdriver.Chrome(base_path + '/chromedriver',
                          options=chroptions)
df = pd.read_csv('city_codes.csv')


def get_one_way_flight(from_, to_, date):
    one_way_url = f'https://www.google.com/flights?hl=en#flt={from_}.{to_}.{date};c:INR;e:1;sd:1;t:f;tt:o'
    return one_way_url


def get_two_way_flight(from_, to_, date, return_date):
    two_way_url = f'https://www.google.com/flights?hl=en#flt={from_}.{to_}.{date}*{to_}.{from_}.{return_date};c:INR;e:1;sd:1;t:f'
    return two_way_url


def google_flight(url):
    driver.get(url)
    driver.implicitly_wait(5)
    timings = driver.find_elements_by_class_name('gws-flights-results__times-row')
    if not timings:
        return None
    else:
        durations = driver.find_elements_by_class_name('gws-flights-results__duration')
        prices = driver.find_elements_by_class_name('gws-flights-results__itinerary-price')
        results = []
        for i in range(len(timings)):
            duration = durations[i].text
            price = prices[i].text
            results.append({'dur': duration, 'pr': price})
        return results


# s = requests.get('https://www.ccra.com/airport-codes/').content
# soup = BeautifulSoup(s, 'html.parser')
# data = []
# table = soup.find('table', attrs={'id': 'tablepress-40'})
# table_body = table.find('tbody')
#
# rows = table_body.find_all('tr')
# for row in rows:
#     cols = row.find_all('td')
#     cols = [ele.text.strip() for ele in cols]
#     data.append([ele for ele in cols if ele])
#
# df = pd.DataFrame(data)
# df.columns = ['city', 'country', 'code']
# df.to_csv('city_codes.csv', index=False)

date = '2020-02-09'  # date format should be yyyy-mm-dd
len_df = len(df)
for _ in range(12):
    rndm = random.randint(0, len_df - 1)
    i = random.randint(0, len_df - 1)
    frm = df['code'][i]
    to = df['code'][rndm]
    url = get_one_way_flight(from_=frm, to_=to, date=date)
    # url = get_two_way_flight(from_=frm, to_=to, date=date)

    data_list = google_flight(url)
    print(f'Flights for date - {date}')
    if data_list is None:
        print(f'Flight from "{df["city"][i]}" to "{df["city"][rndm]}" is not available')
    else:
        for item in data_list:
            print(
                f'Flight from "{df["city"][i]}" to "{df["city"][rndm]}" take {item.get("dur")}'
                f' and {item.get("pr")} cost.')

t2 = time.perf_counter()
driver.quit()

print(f'Finished in {t2-t1} seconds')

# ~~~~~~~~~~~~~~~~~~~~~output~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flights for date - 2020-02-09
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 11 h 14 m and ₹ 22,777 cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 15 h 30 m and  cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 12 h 30 m and ₹ 25,592 cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 12 h 8 m and  cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 13 h 25 m and ₹ 26,331 cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 12 h 8 m and  cost.
# Flight from "Orange County, CA" to "Bar Harbor, ME" take 16 h 20 m and ₹ 33,582 cost.
