from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import Session
from models import engine, Urls
import json


def click_filter():
    price_posted_check_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='hidden'][@value='PricePosted']/parent::div/parent::div")))
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','behavior':'smooth'})", price_posted_check_box)
    wait.until(EC.element_to_be_clickable(price_posted_check_box))
    price_posted_check_box.click()

def get_suppliers():
    navigation = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='item'][@type='lastItem']")))
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','behavior':'smooth'})", navigation)
    total_pages = int(navigation.get_attribute("value"))
    current_page = 0

    while current_page != total_pages:
        supliers = driver.find_elements(By.XPATH, "//a[@class='text-blue1 text-xl']/parent::div")
        for elem in supliers:
            name = elem.find_element(By.XPATH, "./a[@class='text-blue1 text-xl']").text
            address = elem.find_element(By.XPATH, "./div[@class='text-gray6 mb-2.5']").text
            tags = [x.text for x in elem.find_elements(By.XPATH, "./div[@class='flex']/div[@class='mr-3 pl-4 pr-4 p-1 text-xs bg-gray13']")]
            url = elem.find_element(By.XPATH, "./a[@class='text-blue1 text-xl']").get_attribute("href")

            print(name, address, tags, url, sep='\n')
            print("-----------------------------------")

            supplier_url = Urls(name=name, address=address, tags=json.dumps(tags, ensure_ascii=False), url=url)
            session.add(supplier_url)

        current_page += 1
        next_page = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='item'][@type='nextItem']")))
        wait.until(EC.element_to_be_clickable(next_page))
        next_page.click()


url = "https://fgiscs.minstroyrf.ru/monitoring"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.maximize_window()
driver.get(url)
click_filter()

with Session(engine) as session:
    get_suppliers()
    session.commit()

