import re, time
import pandas as pd, requests
from bs4 import BeautifulSoup as bs
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# 
def scrape_article(url):
	try:
		driver.get(url)
	except:
		return "Connection Error"

	time.sleep(5)
	html = driver.page_source

	page = bs(html, 'html.parser')
	aTags = page.find_all('a')
	for a in aTags:
		a.decompose()
	article = page.find('article')
	if article != None:
		text = article.text
	else:
		text = page.text
	text = " ".join(text.split())
	midText = text[len(text)//2:]
	lang = detect(midText)
	falseDict = {"en":"false", "ar":"زائف", "pt":"falso", "zh":"假的", "hr":"lažan", "cs":"nesprávný|falešný", "da":"falsk", "nl":"vals", "es":"falso",
				"fi":"väärä", "fr":"faux", "de":"falsch", "el":"ψευδής", "it":"falso", "ja":"偽りの", "ko":"그릇된", "no":"falsk", "pl":"fałszywy",
				"ro":"greșit", "ru":"ложный", "sv":"falsk", "th":"(เท็จ|ไม่จริง|ไม่ถูก)", "tr":"sahte", "uk":"хибний", "vi":"sai", "id":"benar", "hi":"असत्य", 
				"te":"తప్పు"}

	trueDict = {"en":"true", "ar":"حَقِيقِيّ", "pt":"verdadeiro", "zh":"真实的", "hr":"istinito", "cs":"pravdivý", "da":"sand", "nl":"waar", "es":"verdadero", 
				"fi":"tosi", "fr":"vrai", "de":"wahr", "el":"αληθινός", "it":"vero", "ja":"本当の", "ko":"진실한", "no":"sann", "pl":"prawdziwy|prawda", 
				"ro":"adevarat", "ru":"истинный", "sv":"sant", "th":"ถูกต้อง", "tr":"gerçek", "uk":"правда", "vi":"thật", "id":"salah", "hi":"सच्ची",
				"te":"నిజం"}
	
	try:
		matches = re.findall(rf'({re.escape(falseDict[lang])})|({re.escape(trueDict[lang])})', text, flags=re.IGNORECASE)
	except:
		return lang + " not found"
	trueCount = 0
	falseCount = 0
	for match in matches:
		if(match[1] != ''):
			trueCount += 1
		else:
			falseCount += 1
	return (trueCount, falseCount, lang)
	
	

if __name__ == "__main__":
	# testDf = pd.read_csv("data/test.csv", nrows=20)
	trainDf = pd.read_csv("data/train.csv", nrows=10)
	trainDf['TF'] = trainDf['Fact-checked Article'].apply(scrape_article)
	trainDf.to_csv("./test.csv")
	driver.close()

