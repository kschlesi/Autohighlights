# python file to read in newly scraped text / author / title and create Xtrain for the model

from Flask_App import NLP
from textblob import TextBlob
from Flask_App import a_Model as mod
import pandas as pd

def parse_new_search_data(in_url,con):
    '''pulls records for given url from new search database, parses text, computes and returns Xtrain'''
    # search for and pull text, title, author
    query = '''
            SELECT url, username, title, rawtext
            FROM new_searches
            WHERE url='%s'
            LIMIT 1
            ''' % in_url
    scrapedDf=pd.read_sql_query(query,con)

    # parse text into sentences (break on '/n')
    print(scrapedDf.rawtext)
    sents_stem = mod.text_sentences(list(scrapedDf.rawtext), origdb=[3], keep_raw=False, to_stem=True)
    sents_nostem = mod.text_sentences(list(scrapedDf.rawtext), origdb=[3], keep_raw=False, to_stem=False)
    sents_stem = sents_stem[0]
    sents_nostem = sents_nostem[0]

    # compute alength, sposition, swcount, sentiment, polarity for each sentence
    alen = [len(sents_stem)]*len(sents_stem)
    spos = [i for i in range(len(sents_stem))]
    swcount = [len(s) for s in sents_stem]
    polarity, subjectivity = calculate_sentiment(sents_nostem)
    print(alen)
    print(spos)
    print(swcount)
    print(polarity)
    print(subjectivity)

    # return Xtrain, title, author
    Xtrain = pd.DataFrame[sents_stem]
    title = title[0]
    username = username[0]
    return Xtrain, title, username

def calculate_sentiment(in_sents):
    '''input is list of sentences. sentence is list of words. They are processed but not stemmed...'''
    blobs = [TextBlob(' '.join(s)) for s in in_sents]

    polarity = []
    subjectivity = []
    for sx,s in enumerate(blobs):
        stmt = s.sentiment
        polarity.append(stmt[0])
        subjectivity.append(stmt[1])        
