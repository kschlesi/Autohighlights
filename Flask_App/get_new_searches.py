# python file to read in newly scraped text / author / title and create Xtrain for the model

from Flask_App import NLP
from textblob import textblob

def parse_new_search_data(in_url):
	'''pulls records for given url from new search database, parses text, computes and returns Xtrain'''

	# search for and pull text, title, author

	# parse text into sentences (break on '/n')

	# compute alength, sposition, swcount, sentiment, polarity for each sentence

	# return Xtrain, title, author