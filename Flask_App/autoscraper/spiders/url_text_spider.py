'''this is a python scraper. given a url, it will grab relevant information about the article and return a db row'''

import scrapy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

class URLTextSpider(scrapy.Spider):
    name = "URLTextSpider"

    def __init__(self, in_url=None, user=None, db=None):
        scrapy.Spider.__init__(self)
        print('Spider Initialized...')
        self.the_url = in_url
        self.user = user
        self.db = db

        # set whether article is from medium.com
        self.isMedium = True

        # set whether db should be connected to...
        if user is None or db is None:
            self.engine = None
        else:
            self.engine = create_engine('postgres://%s@localhost/%s'%(user,db))
            ## create a database (if it doesn't exist)
            if not database_exists(self.engine.url):
                create_database(self.engine.url)

    def start_requests(self):
        urls = [
            self.the_url
        ]
        for a_url in urls:
            yield scrapy.Request(url=a_url, callback=self.parse)

    def parse(self, response):
        # if article is from Medium...
        print('Got Article...')
        if self.isMedium:
            # get text
            text = "/n".join(response.xpath('//p[@class]/text()').extract())
            # get title
            title = response.css('.graf--title::text').extract()[0]
            # get author
            username = response.xpath('//a[@data-action="show-user-card"]/text()').extract()[0]

        # if not Medium...
        elif not self.isMedium:
            # get text
            #try:
            text = "/n".join(response.xpath('//p/text()').extract())
            #except:
            #    text = None
            # get title
            title = response.xpath('//title/text()').extract()
            # get author
            try:
                username = response.xpath('//author/text()').extract()
            except:
                username = None

        # organize info into dataframe
        dfA = pd.DataFrame([self.the_url,username,title,text])
        dfA = dfA.T
        dfA.columns = ['url', 'username', 'title', 'rawtext']            

        # save info to csv
        filename = 'new_searches.txt'
        with open(filename,'a+') as f:
            f.write(self.the_url + '\t' + 
                    username + '\t' + 
                    title + '\t' + 
                    text + '\n')

        # save info to database
        if self.engine is not None:
            dfA.to_sql('new_searches', self.engine, if_exists='append')

