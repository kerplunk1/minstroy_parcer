from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import engine, Urls, Suppliers, Warehouses, Products, ConstructionResources
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def click_show_more_info():
    more_info = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='entity-card__info-more']")))
    wait.until(EC.element_to_be_clickable(more_info))
    more_info.click()
        
def get_suppliers_info():
    names = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[1]")
    values = driver.find_elements(By.XPATH, "//div[@class='entity-card__info-table']/table/tbody/tr/td[2]")
    names_list = [x.text for x in names]
    result_names = ["id"]
    for n in names_list:
        if n in naming:
            result_names.append(naming[n])
    result_values = (supplier_id, ) + tuple([x.text for x in values])
    supplier = Suppliers()
    for i, j in zip(result_names, result_values):
        setattr(supplier, i, j)
        print(f"{HEADER}{i}{END}", j)
    try:   
        session.add(supplier)
        session.commit()
    except IntegrityError:
        pass

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

def get_warehouses():
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        name = elem.find_element(By.XPATH, "(./td[1])/div").text
        address = elem.find_element(By.XPATH, "(./td[2])/div").text
        warehouse = Warehouses(supplier_id=supplier_id, name=name, address=address)
        session.add(warehouse)

def get_products():
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        okpd2 = elem.find_element(By.XPATH, "(./td[1])/div").text
        name = elem.find_element(By.XPATH, "(./td[2])/div").text
        product = Products(supplier_id=supplier_id, okpd2=okpd2, name=name)

        print(supplier_id, okpd2, name)
        print("------------------------------")

        session.add(product)

def get_resources():
    active = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content active']")))
    elements = active.find_elements(By.XPATH, "(.//table[@class='ui table'])[2]/tbody/tr")
    for elem in elements:
        ksr = elem.find_element(By.XPATH, "(./td[1])/div").text
        name = elem.find_element(By.XPATH, "(./td[2])/div").text
        try:
            unit = elem.find_element(By.XPATH, "(./td[3])/div").text
        except NoSuchElementException:
            unit = None
        try:
            capacity = elem.find_element(By.XPATH, "./td[4]").text
        except NoSuchElementException:
            capacity = None
        resource = ConstructionResources(supplier_id=supplier_id, ksr=ksr, name=name, unit=unit, capacity=capacity)

        print(supplier_id, ksr, name, unit, capacity)
        print("------------------------------")

        session.add(resource)


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

driver = webdriver.Firefox()
driver.maximize_window()
wait = WebDriverWait(driver, 10)
fails = []

with Session(engine) as session:
    urls = session.query(Urls.id, Urls.url).filter_by(parse_date=func.current_date())
    # urls = session.query(Urls.id, Urls.url).where(Urls.parse_date == func.current_date(), Urls.id > 292)
    for supplier_id, url in urls:
        try:
            driver.get(url)

            click_show_more_info()
            get_suppliers_info()

            click_open_list(1)
            click_pagination_100()
            get_warehouses()
            while not get_number_of_records():
                click_pagination_next()
                get_warehouses()
            click_close_list()

            click_open_list(2)
            click_pagination_100()
            get_products()
            while not get_number_of_records():
                click_pagination_next()
                get_products()
            click_close_list()

            click_open_list(3)
            click_pagination_100()
            get_resources()
            while not get_number_of_records():
                click_pagination_next()
                get_resources()
            click_close_list()    
            
            session.commit()

        except (NoSuchElementException, TimeoutException):
            session.rollback()
            fails.append((supplier_id, url))

if fails:
    for fail in fails:
        print(f"{RED}{fail}{END}")