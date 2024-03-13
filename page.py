from selenium import webdriver
from selenium.webdriver.common.by import By
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
    
            
def click_product_list(driver):
    product_list = driver.find_element(By.XPATH, "(//div[@class='accordion ui fluid']/div[@class='title'])[2]")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", product_list)
    product_list.click()
    time.sleep(5)



def main():

    driver = webdriver.Firefox()
    driver.maximize_window()

    db = sqlite3.connect('minstroy.db')
    cursor = db.cursor()
    cursor.execute("""SELECT id, url FROM urls WHERE name = 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "АГРОПРОМ"';""")
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

        click_product_list(driver)
main()