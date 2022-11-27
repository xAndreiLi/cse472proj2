import pandas as pd
import numpy as np

from utils import *


def save_translation(src:str):
	df:pd.DataFrame = pd.read_pickle(f'./data/{src}.pkl')
	set_progEnd(len(df.text))
	df['sents'] = df.text.apply(tokenize)
	df['translated'] = df.sents.apply(translate_language)
	df.to_pickle(f'./data/{src}.pkl')


def extract(src:str) -> pd.DataFrame:
	df:pd.DataFrame = pd.read_pickle(f'./data/{src}.pkl')
	df['fragments'] = df.translated.apply(filter_fragments)
	df['stemmed'] = df.fragments.apply(stem_words)
	df['filtered'] = df.stemmed.apply(filter_stems)
	df.to_pickle(f'./data/{src}.pkl')
	return df


def print_data(df:pd.DataFrame):
	for row in df.itertuples():
		fragments = '\n'.join(row.fragments)
		if fragments == '': fragments = "No fragments found"
		print(
			f'{row.Index}\n{row.claim}\n{row.url}\n' + 
			f'{row.translated}\nLabel: {row.label}\nFragments\n{fragments}\n' +
			f'Stems:\n{row.stemmed}\nFiltered:\n{row.filtered}'
		)

def print_results(df:pd.DataFrame):
	for row in df.itertuples():
		print(
			f'{row.Index}\n{row.url}\n' + 
			f'Label: {row.label}\n' +
			f'Filtered:\n{row.filtered}'
		)


if __name__ == '__main__':
	#save_pkl('train', './data/train3.pkl', include=[i for i in range(2000,3000)])
	save_translation('train1')
	trainDf = extract('train1')
	# print_data(trainDf)
	#print_results(trainDf)
	
	
		