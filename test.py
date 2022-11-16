from langdetect import detect
import requests, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("https://www.snopes.com/fact-check/congress-exempt-vaccine-mandate/")
time.sleep(3)
html = driver.page_source
print(html)
page = bs(html, 'html.parser')
text = page.get_text()
print(text)
print(detect(text))