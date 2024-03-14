from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import sqlite3


driver = webdriver.Firefox()
driver.maximize_window()

db = sqlite3.connect('minstroy.db')
cursor = db.cursor()

def click_show_more_info():
    more_info = driver.find_element(By.XPATH, "//a[@class='entity-card__info-more']")
    more_info.click()
    time.sleep(1.5)
            
def click_open_list(num):
    the_list = driver.find_element(By.XPATH, f"(//div[@class='accordion ui fluid']/div[@class='title'])[{num}]") # 2 - product, 3 - resourse
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(5)
    
def click_pagination():
    active = driver.find_element(By.XPATH, "//div[@class='content active']")
    try:
        element = active.find_element(By.XPATH, ".//div[@class='ui mini pagination menu']/a[4]")
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
        element.click()
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
    except NoSuchElementException:
        pass
    time.sleep(5)

def click_close_list():
    the_list = driver.find_element(By.XPATH, "//div[@class='accordion ui fluid']/div[@class='active title']")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(1.5)

def get_suppliers_info(id):
    table = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[2]")
    data = (id, ) + tuple([x.text for x in table])
    return data

def get_products():
    active = driver.find_element(By.XPATH, "//div[@class='content active']")
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    data = []
    for elem in elements:
        okpd2 = elem.find_element(By.XPATH, "(./td[1])/div").text
        name = elem.find_element(By.XPATH, "(./td[2])/div").text
        data.append((okpd2, name))
    return data

def get_resources():
    active = driver.find_element(By.XPATH, "//div[@class='content active']")
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    data = []
    for elem in elements:
        ksr = elem.find_element(By.XPATH, "(./td[1])/div").text
        name = elem.find_element(By.XPATH, "(./td[2])/div").text
        unit = elem.find_element(By.XPATH, "(./td[3])/div").text
        capacity = elem.find_element(By.XPATH, "./td[4]").text
        data.append((ksr, name, unit, capacity))
    return data


def main():
    cursor.execute("""SELECT id, url FROM urls WHERE id > 26""")
    urls = cursor.fetchall()

    for id, url in urls:
        driver.get(url)

        time.sleep(5)

        click_show_more_info()
        info = get_suppliers_info(id)
        cursor.execute("""INSERT INTO suppliers
                   (id, full_name, legal_address, inn, ogrn, actual_address,
                   opf_legal, kpp, okved2, tnved, transport, contact, network)
                   VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?)""", info)
        db.commit()
        print(info)
        print("----------------------------------------------")

        click_open_list(2)
        click_pagination()
        products = get_products()
        for product in products:
            data = (id, ) + product
            cursor.execute("""INSERT INTO products
                            (supplier_id, okpd2, name)
                            VALUES (? , ? , ?)""", data)
            db.commit()
            print(data)
            print("----------------------------------------------")
        click_close_list()

        click_open_list(3)
        click_pagination()
        resources = get_resources()
        for resource in resources:
            data = (id, ) + resource
            cursor.execute("""INSERT INTO construction_resources
                           (supplier_id, ksr, name, unit, capacity)
                           VALUES (? , ? , ? , ? , ?)""", data)
            db.commit()
            print(data)
            print("----------------------------------------------")
        click_close_list()


main()