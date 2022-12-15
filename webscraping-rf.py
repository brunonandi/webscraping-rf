from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import json
import os

URL = "https://dados.gov.br/dados/conjuntos-dados/" \
    "cadastro-nacional-da-pessoa-juridica-cnpj"


class ChromeDriver:
    def __init__(self):
        self.driver_path = "chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def go_to_url(self, site):
        self.driver.get(site)

    def close(self):
        self.driver.quit()

    def show_resources(self):
        btn_resources = self.driver.find_element(
            By.CSS_SELECTOR, ".botao-collapse-Recursos")
        btn_resources.click()

    def find_elements_last_update_date(self):
        update_date_list = self.driver.find_elements(
            By.TAG_NAME, "span")

        return update_date_list


def create_txt_file(value, filename):
    with open(filename, "w") as file:
        if type(value) == list:
            for item in value:
                file.write(item.text + "\n")

        else:
            json.dump(value, file)
            os.remove("results.txt")


def cleanup_txt(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

        list_dates = []
        for line in lines:
            if "Última atualização:" in line:
                last_update_date = line[-11:]
                list_dates.append(last_update_date.replace("\n", ""))

    list_dates = list(dict.fromkeys(list_dates))
    return list_dates


def main():
    chrome = ChromeDriver()
    chrome.go_to_url(URL)
    sleep(3)
    chrome.show_resources()
    sleep(3)

    create_txt_file(chrome.find_elements_last_update_date(), "results.txt")
    last_update_date = min(cleanup_txt("results.txt"))
    validation_date = datetime.strftime(datetime.now(), "%d/%m/%Y")

    info = {"updatedAt": last_update_date,
            "checkedAt": validation_date}
    create_txt_file(info, "last_update_date.json")

    sleep(1)
    chrome.close()


if __name__ == "__main__":
    main()
