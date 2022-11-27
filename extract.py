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
	df:pd.DataFrame = pd.read_pickle('./data/testfinal.pkl')
	print(df.columns)
	df = df[['fragments']]
	df.rename(columns={
		'fragments':'text'
	}, inplace=True)
	df.to_csv('./data/testfinal.csv')
	# errDf.translated[292] = translate_language(errDf.sents[292])
	# errDf.fragments[292] = filter_fragments(errDf.translated[292])
	# errDf.translated[438] = translate_language(errDf.sents[438])
	# errDf.fragments[438] = filter_fragments(errDf.translated[438])
	# df.update(errDf)
	# df.to_pickle('./data/testfinal.pkl')
	
		