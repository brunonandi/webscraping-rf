from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

URL_BASE = "https://dados.gov.br/dados/conjuntos-dados/" \
    "cadastro-nacional-da-pessoa-juridica-cnpj"

options = Options()
# options.add_argument("headless")
service = Service("browser_drivers/chrome/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL_BASE)

soup = BeautifulSoup(driver.page_source, "html.parser")

with open("result.txt", "w") as file:
    file.write(soup.prettify())
