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
    print(sents_stem)
    print(len(sents_stem))
    print(sents_nostem)
    print(len(sents_nostem))

    alen = [len(sents_stem)]*len(sents_stem)
    spos = [i for i in range(len(sents_stem))]
    swcount = [len(s) for s in sents_stem]
    print(alen)
    print(spos)
    print(swcount)

    # return Xtrain, title, author
    Xtrain = pd.DataFrame[sents_stem]
    title = title[0]
    username = username[0]
    return Xtrain, title, username