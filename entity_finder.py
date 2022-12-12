
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException



class EntityFinder():
    """
    This class is used to find entities.
    """
    def __init__(self, windows=True):
        self.windows = windows
        pass

    def get_entity_by_region_and_star(self, region, star):
        """
        This function is used to find hotel entities by region and star.
        :param region: Hotel region (city)
        :param star: Hotel attribute (star)
        :param windows: True if you are using windows, False if you are using linux
        :return: (name, entity) tuples
        """
        options = webdriver.ChromeOptions()
        #options.add_argument("start-maximized")
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        if self.windows:
            #pip install webdriver-manager
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        else:
            # sudo apt install chromium-chromedriver
            driver = webdriver.Chrome(options=options)
        region_url = f"https://www.google.com/travel/hotels/hotels+in+{region}"
        driver.get(region_url)
        hotel_class_xpath = '//span[text()="Hotel class"]/..'
        hotel_class_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, hotel_class_xpath)))
        hotel_class_element.click()
        star_button_xpath = f'//span[text()="{star}-star"]'
        star_click_script = f'document.evaluate(\'{star_button_xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();'
        driver.execute_script(star_click_script)
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, "body")
        previous_scroll_height = 0
        stop = False
        while True:
            body.send_keys(Keys.END)
            for i in range(6):
                body.send_keys(Keys.UP)
            current_scroll_height = driver.execute_script("return document.body.scrollHeight")
            if current_scroll_height != previous_scroll_height:
                cant_scroll_count = 0
                if len(driver.find_elements(By.XPATH, '//h2[text()="Places that don\'t exactly match your search"]')) > 0:
                    stop = True
            else:
                cant_scroll_count += 1
            if cant_scroll_count > 50:
                stop = True
            
            previous_scroll_height = current_scroll_height + 0
            if stop:
                break

        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)\
                .until(EC.presence_of_element_located((By.XPATH, '//a[@class="Kz2OTe znMx9d"]')))
        elements = driver.find_elements(By.XPATH, '//a[@class="Kz2OTe znMx9d"]')
        name_entity = [
            (
                re.split(", .*\xa0\w", el.get_attribute("aria-label"))[0], el.get_attribute("data-embedded-entity-key")
            ) for el in elements
        ]
        clear_hotel_class_xpath = '//*[@aria-label="Clear Hotel class"]'
        clear_hotel_class_script = f'document.evaluate(\'{clear_hotel_class_xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()'
        driver.execute_script(clear_hotel_class_script)
        driver.close()
        print(f"{time.time()} last time")
        return name_entity