from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sqlite3


driver = webdriver.Firefox()
driver.maximize_window()

db = sqlite3.connect('minstroy.db')
cursor = db.cursor()

naming = {
        "Полное наименование": "full_name",
        "Юридический адрес": "legal_address",
        "ИНН": "inn",
        "ОГРН": "ogrn",
        "Фактический адрес": "actual_address",
        "ОПФ юридического лица": "opf_legal",
        "КПП": "kpp",
        "ОКВЭД2": "okved2",
        "ТНВЭД": "tnved",
        "Вид транспорта": "transport",
        "Контактная информация": "contact",
        'Адрес сайта в информационно-телекоммуникационной сети "Интернет': "network"
    }

def click_show_more_info():
    more_info = driver.find_element(By.XPATH, "//a[@class='entity-card__info-more']")
    more_info.click()
    time.sleep(1.5)
            
def click_open_list(num):
    the_list = driver.find_element(By.XPATH, f"(//div[@class='accordion ui fluid']/div[@class='title'])[{num}]") # 2 - product, 3 - resourse
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(5)
    
def click_pagination_100():
    active = driver.find_element(By.XPATH, "//div[@class='content active']")
    try:
        element = active.find_element(By.XPATH, ".//div[@class='ui mini pagination menu']/a[4]")
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
        element.click()
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", element)
    except NoSuchElementException:
        pass
    time.sleep(5)

def click_pagination_next():
    active = driver.find_element(By.XPATH, "//div[@class='content active']")
    try:
        element = active.find_element(By.XPATH, ".//i[@class='chevron right icon']/parent::a")
        element.click()
    except NoSuchElementException:
        pass

def click_close_list():
    the_list = driver.find_element(By.XPATH, "//div[@class='accordion ui fluid']/div[@class='active title']")
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", the_list)
    the_list.click()
    time.sleep(1.5)

def get_suppliers_info(id):
    names = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[1]")
    values = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[2]")
    names_list = [x.text for x in names]

    result_names = ["id"]
    for n in names_list:
        if n in naming:
            result_names.append(naming[n])
    
    result_values = (id, ) + tuple([x.text for x in values])

    print(result_values)
    print("------------------------------------")

    # cursor.execute(f"""INSERT INTO suppliers
    #                ({", ".join(result_names)})
    #                VALUES ({' , '.join(['?' for i in range(len(result_names))])})""", result_values)
    # db.commit()

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
    cursor.execute("""SELECT id, url FROM urls WHERE id = 18""")
    urls = cursor.fetchall()

    for id, url in urls:
        driver.get(url)

        time.sleep(5)

        click_show_more_info()
        get_suppliers_info(id)
        

        click_open_list(2)
        click_pagination_100()
        products = get_products()
        for product in products:
            data = (id, ) + product
            # cursor.execute("""INSERT INTO products
            #                 (supplier_id, okpd2, name)
            #                 VALUES (? , ? , ?)""", data)
            # db.commit()
            print(data)
            print("----------------------------------------------")
        click_close_list()

        click_open_list(3)
        click_pagination_100()
        resources = get_resources()
        for resource in resources:
            data = (id, ) + resource
            # cursor.execute("""INSERT INTO construction_resources
            #                (supplier_id, ksr, name, unit, capacity)
            #                VALUES (? , ? , ? , ? , ?)""", data)
            # db.commit()
            print(data)
            print("----------------------------------------------")
        click_close_list()


main()