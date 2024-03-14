from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import visibility_of
import time
import json
import sqlite3


def click_show_more_info(driver):
    more_info = driver.find_element(By.XPATH, "//a[@class='entity-card__info-more']")
    more_info.click()
    time.sleep(5)

def get_suppliers_info(driver, id):
    table = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[2]")
    data = (id, ) + tuple([x.text for x in table])
    return data
    
            
def open_list(driver, num):
    the_list = driver.find_element(By.XPATH, f"(//div[@class='accordion ui fluid']/div[@class='title'])[{num}]") # 2 - product, 3 - resourse
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(5)

    
def click_pagination(driver):
    active = driver.find_element(By.XPATH, "//")
    element = active.find_element(By.XPATH, "//div[@class='ui mini pagination menu']/a[4]")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
    element.click()
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
    time.sleep(5)


def close_list(driver):
    the_list = driver.find_element(By.XPATH, "//div[@class='accordion ui fluid']/div[@class='active title']")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(5)


def get_data(driver):
    pass

def main():

    driver = webdriver.Firefox()
    driver.maximize_window()

    db = sqlite3.connect('minstroy.db')
    cursor = db.cursor()
    cursor.execute("""SELECT id, url FROM urls WHERE id < 3""")
    urls = cursor.fetchall()

    for id, url in urls:
        driver.get(url)

        time.sleep(5)

        click_show_more_info(driver)
        data = get_suppliers_info(driver, id)
        # cursor.execute("""INSERT INTO suppliers
        #            (id, full_name, legal_address, inn, ogrn, actual_address,
        #            opf_legal, kpp, okved2, tnved, transport, contact, network)
        #            VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?)""", data)
        # db.commit()
        print(data)

        open_list(driver, 2)
        click_pagination(driver)
        close_list(driver)

        open_list(driver, 3)
        click_pagination(driver)
        close_list(driver)


main()