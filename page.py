from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3


driver = webdriver.Firefox()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

db = sqlite3.connect('minstroy.db')
cursor = db.cursor()

WARNING = '\033[93m'
GREEN = '\033[92m'
HEADER = '\033[95m'
RED = '\033[91m'
END = '\033[0m'

naming = {
        "Полное наименование": "full_name",
        "Юридический адрес": "legal_address",
        "ИНН": "inn",
        "ОГРН": "ogrn",
        "ОГРНИП": "ogrnip",
        "Фактический адрес": "actual_address",
        "ОПФ юридического лица": "opf_legal",
        "КПП": "kpp",
        "ОКВЭД2": "okved2",
        "ТНВЭД": "tnved",
        "Вид транспорта": "transport",
        "Контактная информация": "contact",
        'Адрес сайта в информационно-телекоммуникационной сети "Интернет"': "network"
    }

def click_show_more_info():
    try:
        more_info = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='entity-card__info-more']")))
        wait.until(EC.element_to_be_clickable(more_info))
        more_info.click()
    except NoSuchElementException:
        pass
            
def get_suppliers_info(supplier_id):
    names = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[1]")
    values = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[2]")
    names_list = [x.text for x in names]

    result_names = ["id"]
    for n in names_list:
        if n in naming:
            result_names.append(naming[n])

    result_values = (supplier_id, ) + tuple([x.text for x in values])

    for i, j in zip(result_names, result_values):
        print(f"{HEADER}{i}{END}", j)

    cursor.execute(f"""INSERT INTO suppliers
                   ({", ".join(result_names)})
                   VALUES ({' , '.join(['?' for i in range(len(result_names))])})""", result_values)
    db.commit()

def check_lists():
    elements = driver.find_elements(By.XPATH, "//div[@class='accordion ui fluid']/div[@class='title']")
    return len(elements) == 3

def click_open_list(num):
        the_list = wait.until(EC.presence_of_element_located((By.XPATH, f"(//div[@class='accordion ui fluid']/div[@class='title'])[{num}]"))) # 1 - warehouses 2 - products, 3 - resourses
        driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", the_list)
        wait.until(EC.element_to_be_clickable(the_list))
        the_list.click()

def click_pagination_100():  
        active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
        try:
            element = active.find_element(By.XPATH, ".//div[@class='ui mini pagination menu']/a[4]")
            driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", element)
            wait.until(EC.element_to_be_clickable(element))
            element.click()
            driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", element)
        except NoSuchElementException:
            pass

def get_number_of_records():
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    try:
        element = active.find_element(By.XPATH, ".//strong")
        nums = element.text.split()
        print(f"{GREEN}Notes: {nums[2]}{END}")
        return int(nums[2]) == int(nums[4])
    except NoSuchElementException:
        return True

def click_pagination_next():
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    try:
        element = active.find_element(By.XPATH, ".//i[@class='chevron right icon']/parent::a")
        driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", element)
        wait.until(EC.element_to_be_clickable(element))
        element.click()
        driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", element)
    except NoSuchElementException:
        pass

def click_close_list():
    the_list = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='accordion ui fluid']/div[@class='active title']")))
    driver.execute_script("arguments[0].scrollIntoView({'block':'center'})", the_list)
    wait.until(EC.element_to_be_clickable(the_list))
    the_list.click()

def get_warehouses(supplier_id):
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        name = elem.find_element(By.XPATH, "(./td[1])/div").text
        address = elem.find_element(By.XPATH, "(./td[2])/div").text
        warehouse = (supplier_id, ) + (name, address)
        cursor.execute("""INSERT INTO warehouses
                    (supplier_id, name, address)
                    VALUES (? , ? , ?)""", warehouse)
        print(warehouse)
        print("----------------------------------------------")
    db.commit()

def get_products(supplier_id):
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        okpd2 = elem.find_element(By.XPATH, "(./td[1])/div").text
        name = elem.find_element(By.XPATH, "(./td[2])/div").text
        product = (supplier_id, ) + (okpd2, name)
        cursor.execute("""INSERT INTO products
                        (supplier_id, okpd2, name)
                        VALUES (? , ? , ?)""", product)
        print(product)
        print("----------------------------------------------")
    db.commit()


def get_resources(supplier_id):
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        ksr = elem.find_element(By.XPATH, "(./td[1])/div").text
        try:
            name = elem.find_element(By.XPATH, "(./td[2])/div").text
        except NoSuchElementException:
            return False
        try:
            unit = elem.find_element(By.XPATH, "(./td[3])/div").text
        except NoSuchElementException:
            unit = None
        try:
            capacity = elem.find_element(By.XPATH, "./td[4]").text
        except NoSuchElementException:
            capacity = None
        resource = (supplier_id, ) + (ksr, name, unit, capacity)
        cursor.execute("""INSERT INTO construction_resources
                    (supplier_id, ksr, name, unit, capacity)
                        VALUES (? , ? , ? , ? , ?)""", resource)
        print(resource)
        print("----------------------------------------------")
    db.commit()
    return True


cursor.execute("""SELECT id, url FROM urls WHERE id > 3075;""")
urls = cursor.fetchall()

for supplier_id, url in urls:
    driver.get(url)

    try:
        click_show_more_info()
    except TimeoutException:
        continue
    get_suppliers_info(supplier_id)

    
    if check_lists():
        click_open_list(1)
        click_pagination_100()
        get_warehouses(supplier_id)
        while not get_number_of_records():
            click_pagination_next()
            get_warehouses(supplier_id)
        click_close_list()

        
        click_open_list(2)
        click_pagination_100()
        get_products(supplier_id)
        while not get_number_of_records():
            click_pagination_next()
            get_products(supplier_id)
        click_close_list()


        click_open_list(3)
        click_pagination_100()
        if get_resources(supplier_id):
            while not get_number_of_records():
                click_pagination_next()
                get_resources(supplier_id)
            click_close_list()
        else:
            print(f'{WARNING}There are no names in the "Construction Resources" table. Page refresh.{END}')
            time.sleep(10)
            driver.refresh()
            click_open_list(3)
            click_pagination_100()
            if get_resources(supplier_id):
                while not get_number_of_records():
                    click_pagination_next()
                    get_resources(supplier_id)
                click_close_list()
            else:
                print(f'{RED}There are no names in the "Construction Resources" table. Page refresh.{END}')
                time.sleep(10)
                driver.refresh()
                click_open_list(3)
                click_pagination_100()
                if get_resources(supplier_id):
                    while not get_number_of_records():
                        click_pagination_next()
                        get_resources(supplier_id)
                    click_close_list()