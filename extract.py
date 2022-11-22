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
	df['keylines'] = df.translated.apply(sanitize_tokens)
	return df


def print_data(df:pd.DataFrame):
	for row in df.itertuples():
		keylines = '\n'.join(row.keylines)
		if keylines == '': keylines = "No keylines found"
		print(
			f'{row.Index}\n{row.claim}\n{row.url}\n{row.translated}\nLabel: {row.label}\n{keylines}\n'
		)


if __name__ == '__main__':
	#save_pkl('train', nrows=nrows)
	#save_translation('train')
	trainDf = extract('train')
	print_data(trainDf)
	
	
		