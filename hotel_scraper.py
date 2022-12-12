from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os




class HotelScraper():
    def __init__(self, windows=True):
        self.windows = windows
        pass

    def scrape_with_reviews(self, entity, n_reviews):
        """
        This function is used to scrape hotel informations with n reviews.
        :param entity: Hotel entity
        :return: None
        """

        ## Check if file exists
        if os.path.exists(f"{entity}.html"):
            return None

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
        hotel_reviews_page = f"https://www.google.com/travel/hotels/entity/{entity}/reviews"
        driver.get(hotel_reviews_page)
        time.sleep(4)
        body = driver.find_element(By.TAG_NAME, "body")
        review_count_xpath = '//div[@class="FzERAb"]//div[@class="sSHqwe"][text()]'
        review_count = driver.find_elements(By.XPATH, review_count_xpath)[0].text.split(" ")[0] if len(driver.find_elements(By.XPATH, review_count_xpath))>0 else "0"
        review_count = int(review_count.replace(",", "").replace(".", ""))
        review_count = review_count if review_count < n_reviews else n_reviews
        print("review_count", review_count)
        review_loop_count = round(review_count/10) - 10
        page_scroll_change_count = 0
        stop = False
        start_time = time.time()
        previous_scroll_height = 0
        while True:
            body.send_keys(Keys.END)
            #time.sleep(0.1)
            body.send_keys(Keys.UP)
            #time.sleep(0.1)
            current_scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if current_scroll_height != previous_scroll_height:
                page_scroll_change_count += 1
                cant_scroll_count = 0
                if page_scroll_change_count > review_loop_count:
                    XPATH = '//div[@class="Svr5cf bKhjM"]'
                    lenn = len(driver.find_elements(By.XPATH, XPATH))
                    
                    if lenn + 15 < review_count:
                        stop = False
                    else:
                        stop = True
                    #print(lenn, review_count, stop)
            else:
                cant_scroll_count += 1

            if cant_scroll_count > 50:
                stop = True
            previous_scroll_height = current_scroll_height * 1

            if stop:
                break

        scroll_time = time.time() - start_time
        print(f"entity: {entity}")
        print(f"Scroll time: {scroll_time}")
        print(f"Review count: {review_count}")
        print(f"Scroll time per review: {scroll_time/review_count}")

        return driver.page_source