
from flask import render_template, request, redirect, send_file, url_for
from Flask_App import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import pickle
from Flask_App import a_Model as mod
#from Flask_App import get_new_searches as gns
from Flask_App import run_text_scraper as rts
from ast import literal_eval

#user = 'ubuntu' #add your username here (same as previous postgreSQL)                      
user = 'kimberly'
host = 'localhost'
dbname = 'medium'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)
fname = ('./Flask_App/static/Models/rfm_model.pkl')
ntop = 12
demo_url = "https://medium.com/personal-growth/the-simple-way-i-overcame-my-writers-block-and-beat-procrastination-b4afa12eaae9"
with open(fname,'rb') as f:
   model = pickle.load(f)

@app.route('/')
@app.route('/index')
@app.route('/input')
def url_input():
    return render_template("input.html",in_url="")

@app.route('/output')
def compute_output():
#pull 'in_url' from input field and store it
    in_url = request.args.get('in_url')
    print(in_url)

# try finding it in table....

    #just select the matching url from the articles table
    query = "SELECT postid, title, username, highlight, popdate, nlikes, rawtext, origdb FROM articles WHERE url='%s'" % in_url
    query_results=pd.read_sql_query(query,con)

    if query_results.shape[0] > 0:
        q_results_dict = []
        for i in range(0,query_results.shape[0]):
            q_results_dict.append(dict(title=query_results.iloc[i]['title'], 
                                      username=query_results.iloc[i]['username'], 
                                      highlight=query_results.iloc[i]['highlight'],
                                      popdate=query_results.iloc[i]['popdate'],
                                      nlikes=query_results.iloc[i]['nlikes']
                                      ))
        # grab information about sentences
        xquery = '''SELECT a.apid as apid, alength, sposition, swcount, polarity, subjectivity
                    FROM (SELECT postid as apid FROM articles WHERE url='%s' ) AS a 
                    INNER JOIN sentences_sanal ON a.apid = sentences_sanal.postid;''' % in_url 
        Xtrain = pd.read_sql_query(xquery,con)

# if not in table, auto-scrape and save info
    else:
    
    # start scrapy spider 'url_text_spider' (puts info in new_searches table in medium db)
        r = rts.run_text_scraper(in_url=in_url,user=user)

    # then search db, process text, calculate sentence information, construct Xtrain
        #Xtrain, title, username = gns.parse_new_search_data(in_url)
        Xtrain = []
        title = []
        username = []

# apply model, get htext....
    dfHrecList = mod.apply_model(Xtrain=Xtrain,model=model,ntop=ntop)

    # grab text of highlight sentences
    if True: 
        art_info = query_results[['postid','rawtext','origdb']]
    else:
        art_info = 1;
    htext_dict = mod.get_htext(recdflist=dfHrecList,art_info=art_info)

# render output
    return render_template("output.html", q_results_dict = q_results_dict, htext_dict = htext_dict, in_url=in_url)

@app.route('/output_alt')
def switch_output():
    # get necessary args
    in_url = request.args.get('in_url')
    q_results_dict = request.args.get('q_results_dict')
    q_results_dict = literal_eval(q_results_dict)
    htext_dict = request.args.get('htext_dict')
    htext_dict = literal_eval(htext_dict)
    page_no = request.args.get('page_no')
    page_no = int(page_no)

    # change dict order
    new_dict = {}
    new_dict[0] = htext_dict[page_no]
    new_dict[page_no] = htext_dict[0]
    if page_no==1:
        new_dict[2] = htext_dict[2]
    elif page_no==2:
        new_dict[1] = htext_dict[1]

    return render_template("output.html", q_results_dict = q_results_dict, htext_dict = new_dict, in_url=in_url)

@app.route('/input_demo')
def url_input_demo():
    return render_template("input.html",in_url=demo_url)

@app.route('/fbpost')
def facebook_post():
    to_url = request.args.get('to_url')
    return redirect(to_url, code=302)


