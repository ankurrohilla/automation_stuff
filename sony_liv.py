from selenium import webdriver
import os
import time

base_path = os.getcwd()
driver = webdriver.Chrome(base_path + '/chromedriver')
driver.get(url='https://www.sonyliv.com/')
driver.implicitly_wait(5)
driver.fullscreen_window()

# close the pop-up notification
driver.find_element_by_id('wzrk-cancel').click()

# scroll down for finding shows
lenOfPage = driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

match = False
while (match == False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

# find element by by name Shows
driver.find_element_by_link_text('Shows')

driver.implicitly_wait(5)

# click the show element by xpath
p = driver.find_element_by_xpath(
    '//*[@id="movie_24"]/ul/data-owl-carousel/div/div/div[1]/li/div/custom-rails-landscape/div/a/div/img')
p.click()
driver.implicitly_wait(10)

driver.save_screenshot('test.png')
driver.quit()
