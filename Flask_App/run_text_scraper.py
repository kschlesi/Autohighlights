# python function to run text scraper

import scrapy
import logging
#from twisted.internet import reactor
#from scrapy.crawler import CrawlerProcess, CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.utils.project import get_project_settings
#from scrapy.settings import Settings
from Flask_App.autoscraper.spiders.url_text_spider import URLTextSpider
#import subprocess
from subprocess import Popen, PIPE, STDOUT


def run_text_scraper(in_url,user=None):
    '''given a url, initializes and starts the text spider and scrapes the page'''
    
    command = ['scrapy', 'crawl', 'URLTextSpider', '-a', 'in_url=' + in_url ,
                                                   '-a', 'user=' + user ,
                                                   '-a', 'db=medium'
              ]

    logging.basicConfig(filename='log_scraper.log',level=logging.DEBUG)

    process = Popen(command, cwd='/Users/kimberly/Documents/Insight/Autohighlights/Autohighlights/Flask_App', 
                             stdout=PIPE, stderr=STDOUT)
    with process.stdout:
        log_subprocess_output(process.stdout)
    exitcode = process.wait() # 0 means success
    print(exitcode)

    # #log.start(loglevel=log.DEBUG)
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    # #spider1 = BBSpider(start_url=url)
    # settings = Settings()
    # settings.set("PROJECT", {"autoscraper"})
    
    # #crawler = CrawlerProcess(settings)
    # crawler = CrawlerRunner(settings)

    # #crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    # #crawler.configure()
    # d = crawler.crawl(URLTextSpider, in_url=in_url, user='kimberly', db='medium')
    # #crawler.start()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run() # the script will block here until the crawling is finished

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)

# def spider_closing(spider):
#     """Activates on spider closed signal"""
#     #log.msg("Closing reactor", level=log.INFO)
#     reactor.stop()