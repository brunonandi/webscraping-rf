from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
import json
from pathlib import Path

ROOT_FOLDER = Path(__file__).parent
CHROME_DRIVER_PATH = ROOT_FOLDER / "chromedriver"
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

    def find_elements(self):
        update_date_list = self.driver.find_elements(
            By.TAG_NAME, "span")

        return update_date_list

    def click_elements(self):
        btn_resources = self.driver.find_element(
            By.CSS_SELECTOR, ".botao-collapse-Recursos")

        btn_resources.click()


def write_file(arq, name):
    with open(name, "w") as file:
        if type(arq) == dict:
            json.dump(arq, file)
            remove_file("raw_data.txt")

        elif type(arq) == list:
            for item in arq:
                file.write(item.text + "\n")

        else:  # verificar se essa condição funciona corretamente
            file.write(arq.text)


def load_file(filename, type):
    with open(ROOT_FOLDER / filename, "r") as file:
        if type == "json":
            json_file = json.load(file)

    return json_file


def remove_file(filename):
    exists = check_if_file_exists(filename)
    if exists:
        Path.unlink(ROOT_FOLDER / filename)


def check_if_file_exists(filename):
    exists = Path(ROOT_FOLDER / filename).is_file()

    return exists


def clean_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

        list_dates = []
        for line in lines:
            if "Última atualização:" in line:
                list_dates.append(line[-11:].replace("\n", ""))

    list_dates = list(dict.fromkeys(list_dates))
    return list_dates


def scraping(check_date, last_check=None, last_update=None):
    chrome = ChromeDriver()
    chrome.go_to_url(URL)
    sleep(3)
    chrome.click_elements()
    sleep(3)

    write_file(chrome.find_elements(), "raw_data.txt")
    scraped_date = min(clean_file("raw_data.txt"))

    if last_check is None and last_update is None:
        info = {"updatedAt": scraped_date,
                "checkedAt": check_date}
        write_file(info, "result.json")

    else:
        if last_check >= check_date and last_update >= scraped_date:
            exit()

        else:
            json_file = load_file("result.json", "json")
            json_file["updatedAt"] = scraped_date
            json_file["checkedAt"] = check_date
            write_file(json_file, "result.json")

    sleep(3)
    chrome.close()


def main():
    today = datetime.strftime(datetime.now(), "%d/%m/%Y")
    file_exists = check_if_file_exists("result.json")
    if file_exists:
        dict_dates = load_file("result.json", "json")
        last_updated_at = dict_dates["updatedAt"]
        last_checked_at = dict_dates["checkedAt"]

        scraping(today,
                 last_check=last_checked_at,
                 last_update=last_updated_at)

    else:
        scraping(today)


if __name__ == "__main__":
    main()
