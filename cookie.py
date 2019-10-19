from selenium import webdriver
import os
import pickle
import httplib2

base_path = os.getcwd()


def geting_cookie():
    pkl_file = 'cookies.pkl'
    chroptions = webdriver.ChromeOptions()
    chroptions.add_argument(argument='headless')
    driver = webdriver.Chrome(base_path + '/chromedriver', options=chroptions)

    driver.get('https://www.google.com/flights?hl=en')
    pickle.dump(driver.get_cookies(), open(pkl_file, 'wb'))
    current_url = driver.current_url
    print('before')
    print(driver.get_cookies())
    return current_url, pkl_file


def load_cookie(url, pkl_file):
    opt2 = webdriver.ChromeOptions()
    opt2.add_argument('disable-infobars')
    driver2 = webdriver.Chrome(base_path + '/chromedriver', options=opt2)
    driver2.get(url)
    cookies = pickle.load(open(pkl_file, 'rb'))
    for cookie in cookies:
        driver2.add_cookie(cookie)
    driver2.implicitly_wait(3)
    cookies = driver2.get_cookies()
    print("after load cookies")
    print(driver2.get_cookies())
    driver2.quit()
    return cookies


url, pkl = geting_cookie()  # tuple unpacking
cookies_list = load_cookie(url, pkl)
http = httplib2.Http()
# get cookie_value here
for c in cookies_list:
    headers = {'expiry': str(c.get('expiry'))}
    response, content = http.request("https://www.google.com/flights?hl=en", 'GET', headers=headers)
    print(response, content)
