import requests, time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from googletrans import Translator 
from utils import *
from extract import *

df = pd.read_pickle('./data/train1.pkl')
print_data(df.iloc[0:5])

# include = [1,5,7,9,12,13,14,16,21,35,38,43,45,46]
include = [i for i in range(100)]
# save_pkl('train', out="./data/devtest.pkl", include=include)
# save_translation('train1')
# df = extract('train1')
# print_data(df)

# tr = Translator()
# text = "un bulo."
# print(tr.translate(text))

# for i in range(0,10):
# 	print_progress(i,9,"Test")
# 	time.sleep(.5)

# driver = init_browser()
# driver.get("https://lupa.uol.com.br/jornalismo/2021/09/13/verificamos-video-medica-seguranca-vacinas")
# timeout = time.time() + 10

# print(driver.page_source)
# time.sleep(100000)

# 09201db8-154e-49bd-9a36-fe681aef4aef
# d771f83c-c237-425c-831d-2278ec788823
