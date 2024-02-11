from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from typing import List
import time
import pathlib
import os
import shutil
from re import sub

tempo_output_folder = "D:\\Desktop\\BigData\\webscraping\\scrape_csv\\palaystat_tempo"
output_folder = "D:\\Desktop\\BigData\\webscraping\\scrape_csv\\palaystat"
pathlib.Path(tempo_output_folder).mkdir(parents=True, exist_ok=True)
pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("prefs", {"download.default_directory" : tempo_output_folder})
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(300)
root_url = "https://palaystat.philrice.gov.ph/profile/"

def snake_case(string: str):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return sub(r'\W+', '_', string).lower().strip('_')

def go_to_card_link(xpath: str):
    driver.get(root_url)
    card_link = driver.find_element(By.XPATH, xpath)
    print("go_to_card_link", card_link)
    card_link.click()

def main():
    driver.get(root_url)
    try:
        # table_links: List[WebElement] = []
        table_links: List[tuple[str, str]] = []
        # Get links
        # https://palaystat.philrice.gov.ph/profile/
        # class="page-body" > a
        #     class="item-list" > a
        card_links = driver.find_elements(By.XPATH, "//div[@class='page-body']//a")
        print("Got card_links")

        for i, card_link in enumerate(card_links):
            go_to_card_link(xpath="(//div[@class='page-body']//a)[{}]".format(i + 1))
            items = driver.find_elements(By.XPATH, "//div[@class='item-list']//a")
            category = snake_case(driver.find_element(By.XPATH, "//div[@class='page-header']//h1").text)
            table_links += [(category, item.get_attribute('href')) for item in items]

        # Go through links
        for category, table_link in table_links:
            driver.get(table_link)
            print("going to ", table_link)
            # for each: parent = class="form-group"
            # click class="btn-group"
            #     then in class="multiselect-container dropdown-menu show"
            #         click > button class="multiselect-option dropdown-item"
            # click to close class="multiselect-container dropdown-menu show"
            btn_groups = driver.find_elements(By.XPATH, "//div[@class='form-group']//button[@class='multiselect dropdown-toggle custom-select text-center']")
            for btn in btn_groups:
                btn.click()
                # options = wait.until(EC.presence_of_all_elements_located(By.XPATH, "//div[@class='multiselect-container dropdown-menu show']/button"))
                options = driver.find_elements(By.XPATH, "//div[@class='multiselect-container dropdown-menu show']/button")
                for option in options:
                    option.click()
                btn.click()

            # wait for table
            # <button id="download">
            # <a id="csv">
            driver.find_element(By.ID, "submit").click()
            driver.find_element(By.ID, "download").click()
            driver.find_element(By.ID, "csv").click()

            # filename
            filename = snake_case(driver.find_element(By.ID, "table-title").text) + ".csv"

            # Wait for download to finish
            wait_time = 0
            while True:
                if any(fname.endswith('.csv') for fname in os.listdir(tempo_output_folder)):
                    break
            
            # Rename and move file
            temp_file = os.listdir(tempo_output_folder)[0]
            folder_path = output_folder + "\\" + category
            pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
            shutil.move(tempo_output_folder + "\\" + temp_file, folder_path + "\\" + filename)


    except Exception as e:
        print("Something went wrong")
        print(e)
    
    print("Finished")

if __name__ == "__main__":
    main()
    # print(snake_case("Average active ingredients (kg/ha) of pesticides used per chemical type, by cropping season"))
    driver.close()


# urls = ['', 'https://palaystat.philrice.gov.ph/statistics/']