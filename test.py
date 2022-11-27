import requests, time
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures, TrigramAssocMeasures, TrigramCollocationFinder
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

# #save_translation('traintest')
# df:pd.DataFrame = pd.read_pickle('./data/traintest.pkl')
# df['fragments'] = df.translated.apply(filter_fragments)

# df = df[['claim', 'url', 'label', 'fragments']]
# df.to_csv('./data/traintest.csv')

# df:pd.DataFrame = pd.read_pickle('./data/test0.pkl')
# errDf = df[df['title'].str.contains('not found')]
# newUrls = [

# ]
df = pd.read_pickle('./data/train1.pkl')
df['fragments'] = df.translated.apply(filter_fragments)

print(df.columns)

df = df[['fragments', 'label']]
df.rename(columns={
	'fragments':'text'
}, inplace=True)

df.to_csv('./data/train1.csv')


# frames = []
# for i in range(0,8):
# 	path = f'./data/test{i}.pkl'
# 	dfSeg = pd.read_pickle(path)
# 	frames.append(dfSeg)
# df = pd.concat(frames)

# df.to_pickle('./data/test.pkl')

# df:pd.DataFrame = pd.read_pickle('./data/testfinal.pkl')

# print(df.text[568])


# include = [
# 	55,
# 	153,
# 	449,
# 	469,
# 	494,
# 	550,
# 	598,
# ]

# newUrls = [
# 	'https://timesofindia.indiatimes.com/times-fact-check/news/fake-alert-notice-declaring-holidays-in-4-indian-states-due-to-coronavirus-is-fake/articleshow/74624054.cms',
# 	'https://timesofindia.indiatimes.com/times-fact-check/news/fake-alert-news-of-baba-ramdev-overdosing-on-cow-urine-to-prevent-coronavirus-is-fake/articleshow/74551698.cms',
# 	'https://timesofindia.indiatimes.com/times-fact-check/news/fake-alert-china-seeking-court-approval-to-kill-20000-coronavirus-patients/articleshow/74002017.cms',
# 	'https://timesofindia.indiatimes.com/times-fact-check/news/fake-alert-no-chinese-president-pm-did-not-visit-any-mosque-to-pray-post-coronavirus-outbreak/articleshow/73978293.cms',
# 	'https://www.aap.com.au/factcheck/the-who-has-not-labelled-coronavirus-a-plague-and-the-virus-has-not-killed-75000-people/',
# 	'https://fullfact.org/health/coronavirus-government-laboratory/',
# 	'https://www.poynter.org/?ifcn_misinformation=a-saudi-arabian-study-for-a-mers-vaccine-is-linked-to-the-outbreak-of-coronavirus'
# ]

# save_pkl('test', './data/testfix.pkl', include=include, newUrls=newUrls)



# df:pd.DataFrame = pd.read_csv


# for url in errDf.url:
# 	print(url)


def get_tokens():

	df:pd.DataFrame = pd.read_pickle('./data/train1.pkl')

	false = df.loc[df.label==0]
	misleading = df.loc[df.label==1]
	true = df.loc[df.label==2]
	unproven = df.loc[df.label==3]

	falseTokens = []
	misTokens = []
	trueTokens = []
	unpTokens = []

	data = {
		'false':[false,falseTokens], 
		'misleading':[misleading,misTokens], 
		'true':[true,trueTokens], 
		'unproven':[unproven,unpTokens]
		}

	for df, tok in data.values():
		for trans in df.translated:
			text = ' '.join(trans)
			text = text.translate(str.maketrans('', '', string.punctuation))
			tokens = word_tokenize(text)
			tokens = [word.lower().strip() for word in tokens 
						if (word.isalpha())]
			tok.append(tokens)


	pd.to_pickle(data, './data/data.pkl')


def analyze():
	data:dict = pd.read_pickle('./data/data.pkl')
	trigram_measures = TrigramAssocMeasures()

	for df, tok in data.values():
		finder = TrigramCollocationFinder.from_documents()
	

	# allTokens = pd.read_pickle('./data/misleadingTokens.pkl')

	
	# triFinder = TrigramCollocationFinder.from_words(allTokens)
	# triCols = sorted(triFinder.nbest(trigram_measures.raw_freq, 30))



def save_csv():
	df = pd.read_pickle('./data/train1.pkl')
	df = df[['claim', 'url', 'label', 'translated']]
	df.to_csv('./data/train1.csv')

def article_body():
	df:pd.DataFrame = pd.read_pickle('./data/train1.pkl')
	df.iloc[30:31]
	print(df.fragments[30])
