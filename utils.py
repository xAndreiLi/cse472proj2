import time, re, string

import pandas as pd, numpy as np
from bs4 import BeautifulSoup as bs
from bs4.element import Comment

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from googletrans import Translator

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer

# Utils module for helper functions

# Global Variables
progress = 1
progEnd = None

# Filter function
def visible_text(element) -> bool:
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def save_pkl(src:str, out:str=None, nrows:int=None, skiprows:int=None, include:list=None) -> None:
	'''
	Add column containing html string to train.csv and save to train.pkl

	Parameters:
		src (str): Name of csv/pkl (train | test)
		[optional]: 
			nrows (int): Number of rows to read from csv
			include (list): List of row indices to save
	'''
	driver = init_browser()

	srcPath = f'./data/{src}.csv'
	if not out: out = f'./data/{src}.pkl'
		
	df = pd.read_csv(srcPath, nrows=nrows, skiprows=skiprows)
	if include: df = df.iloc[include]
	# Rename columns
	df.rename(columns={
		'Country (mentioned)':'country',
		'Review Date':'date',
		'Claim':'claim',
		'Source':'source',
		'Label':'label',
		'Fact-checked Article':'url'
	}, inplace=True)

	# Apply function
	def save_html(url: str) -> str:
		# Reroute to new site url
		if('piaui.folha' in url):
			url = url.replace(
				'piaui.folha.uol.com.br/lupa',
				'lupa.uol.com.br/jornalismo'
			)
		try:
			driver.get(url)
		except :
			return 'Connection Error'
		finally:
			print_progress("Fetching HTML")
		
		text = text_from_html(driver.page_source)
		retry = 0
		while len(text) < 1500:
			if retry > 5:
				break
			time.sleep(1)
			text = text_from_html(driver.page_source)
			retry += 1
		return text

	global progEnd
	progEnd = len(df.url)
	
	df['text'] = df.url.apply(save_html)
	df.to_pickle(out)
	driver.close()

	#https://leadstories.com/hoax-alert/2021/09/fact-check-claim-that-80-percent-of-covid-19-deaths-occurred-within-the-vaccinated-population-in-scotland-is-1.html
	#https://leadstories.com/hoax-alert/2021/09/fact-check-claim-that-80-percent-of-covid-19-deaths-occurred-within-the-vaccinated-population-in-scotland-is-misleading.html


# Get visible text from html
def text_from_html(html) -> str:
    soup = bs(html, 'html.parser')
    text:list[str] = soup.findAll(text=True)
    text = list(filter(visible_text, text)) 
    return u'. '.join(t.strip() for t in text)


def tokenize(text):
	'''
	Separate text into sentences and filter out non-sentences (by length)
	'''
	sents = sent_tokenize(text)
	cutoff = np.percentile([len(sent) for sent in sents], 95)
	sents = list(filter(lambda x:
			(4<len(x)<cutoff),
		sents
	))
	return sents


# Translate text to English
def translate_language(sents:list[str]):
	print_progress("Translating Text")

	tr = Translator()
	# Check if already english from sample of sentences
	try:
		lang = tr.detect(' '.join(sents[5:10])).lang
		if lang == 'en': return sents
	except Exception as err:
		print(err)
		print(sents)
		return "Error"

	chunks = []
	chunk = ''
	for sent in sents:
		if len(chunk)+len(sent) > 4999:
			chunks.append(chunk)
			chunk = ''
		chunk += sent + '\n'
	chunks.append(chunk)

	bulk = ''
	for chunk in chunks:
		try:
			bulk += tr.translate(chunk, src=lang).text
		except Exception as err:
			print(err)
			print(sents)
			return "Error"

	translated = bulk.split('\n')

	return translated


def filter_fragments(sents:list[str]) -> list[str]:
	# Separate sentences by commas to narrow down text
	fragments:list[str] = []
	for sent in sents:
		fragments.extend(re.split(r',', sent.lower()))
	
	# Filter for sentence fragments containing keywords and no stopwords
	keywords = [
		'true', 'false', 'mislead', 'fake', 'truth', 'wrong', "baseless",
		'evidence', 'proof', 'misinformation', 'basis', 'inaccurate', 'fallacious',
		'rating', 'labeled', 'bully', 'verdict'
	]
	stopwords = [
		'read', 'fact check', 'more', 'we ', 'previous', 'next'
	]
	fragments = list(filter(lambda x: (
		any(key in x for key in keywords) and not any(stop in x for stop in stopwords)
		), 
		fragments
	))

	return fragments


def stem_words(fragments:list[str]):
	# Word Tokenize for filter and stemming
	stemmed = []
	stemmer = SnowballStemmer('english')
	for frag in fragments:
		frag = frag.translate(str.maketrans('', '', string.punctuation))
		words = word_tokenize(frag)
		stems = []
		for word in words:
			stems.append(stemmer.stem(word))
		stemmed.append(stems)
	
	return stemmed


def filter_stems(stems:list):
	keywords = [
		'true', 'fals', 'fake', 'mislead', 'not', 'misinform', 'no',
		'proof', 'evid', 'lie', 'wrong'
	]
	negators = ['not', 'no']
	negDict = {
			'true':'fals',
			'truth':'fals',
			'proof':'mislead',
			'evid':'mislead',
			'basis':'mislead',
			'misinform':'mislead',
			'mislead':'mislead',
			'fals':'true',
			'fake':'true',
			'wrong':'true',
			'not':'',
			'no':''
		}
	filtered = []
	for sent in stems:
		sentFil = []
		for word in sent:
			if word in keywords: sentFil.append(word)
		for ind, word in enumerate(sentFil):
			if (word in negators):
				sentFil[ind] = ""
				if (ind+1 < len(sentFil)):
					sentFil[ind+1] = negDict[sentFil[ind+1]]

		filtered.extend(sentFil)
		filtered = [word for word in filtered if word != '']
		filtered = [*set(filtered)]
	return filtered



	# 	
		
	# 	for ind, word in enumerate(words):
	# 		if word in negators:
	# 			words[ind] = ""
	# 			words[ind+1] = negDict[words[ind+1]]
		
	# 	if words:
	# 		concluders = ['rating', 'output', 'labeled']
	# 		if (len(words)>1) and (words[0] in concluders): return [words[1]]
	# 		sanitized.append(" ".join(words))
	# # Remove duplicates
	# sanitized = [*set(sanitized)]
	# return sanitized


def print_progress(text:str='Progress'):
	'''
	Prints progress of task on the same line

	Output: "Doing Task: 1/50"

	Parameters:
		[optional]: 
			text (str): Text to print before progress
	'''
	global progress
	global progEnd 
	if progress == progEnd: 
		print(f'{text}: {progress}/{progEnd}', end='\n')
		progress = 1
	else:
		print(f'{text}: {progress}/{progEnd}', end='\r')
		progress += 1


def set_progEnd(end:int) -> None:
	global progEnd
	progEnd = end


def init_browser():
	'''
	Initializes Selenium webdriver and returns the driver object
	'''
	service = ChromeService(ChromeDriverManager(path="./").install())
	options = ChromeOptions()
	options.add_extension('./extensions/ublockChrome.crx')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	capabilities = DesiredCapabilities.CHROME
	capabilities['pageLoadStrategy'] = 'eager'

	driver = webdriver.Chrome(
		service=service,
		options=options,
		desired_capabilities=capabilities
	)
	driver.get("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html#settings.html")
	time.sleep(1)
	frame = driver.find_element(By.ID,'iframe')
	driver.switch_to.frame(frame)

	driver.find_element(By.XPATH,'//input[@data-setting-name="noLargeMedia"]').click()
	driver.find_element(By.XPATH,'//input[@data-setting-name="noRemoteFonts"]').click()
	input = driver.find_element(By.XPATH,'//input[@data-setting-name="largeMediaSize"]')
	input.clear()
	driver.switch_to.default_content()
	return driver