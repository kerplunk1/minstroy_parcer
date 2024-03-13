from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import sqlite3


def click_filter(driver):

    driver.execute_script("window.scrollTo({top: 700, behavior: 'smooth'});")
    time.sleep(5)

    price_posted_check_box = driver.find_element(By.XPATH, "//input[@class='hidden'][@value='PricePosted']/parent::div/parent::div")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", price_posted_check_box)
    price_posted_check_box.click()
    time.sleep(5)


def get_suppliers(driver):

    navigation = driver.find_element(By.XPATH, "//a[@class='item'][@type='lastItem']")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", navigation)
    
    total_pages = int(navigation.get_attribute("value"))
    current_page = 0

    all_suppliers = []

    while current_page != total_pages:
        supliers = driver.find_elements(By.XPATH, "//a[@class='text-blue1 text-xl']/parent::div")

        for elem in supliers:
            name = elem.find_element(By.XPATH, "./a[@class='text-blue1 text-xl']").text
            address = elem.find_element(By.XPATH, "./div[@class='text-gray6 mb-2.5']").text
            tags = [x.text for x in elem.find_elements(By.XPATH, "./div[@class='flex']/div[@class='mr-3 pl-4 pr-4 p-1 text-xs bg-gray13']")]
            url = elem.find_element(By.XPATH, "./a[@class='text-blue1 text-xl']").get_attribute("href")
            obj = {
                "name": name,
                "address": address,
                "tags": json.dumps(tags, ensure_ascii=False),
                "url": url
            }
            all_suppliers.append(obj)

            print(name, address, tags, url, sep='\n')
            print("-----------------------------------")

        current_page += 1
        next_page = driver.find_element(By.XPATH, "//a[@class='item'][@type='nextItem']")
        time.sleep(5)
        next_page.click()
    
    return all_suppliers

def insert_to_db(table, data):
    pass


def main():

    url = "https://fgiscs.minstroyrf.ru/monitoring"

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)

    time.sleep(5)

    click_filter(driver)
    urls = get_suppliers(driver)


main()