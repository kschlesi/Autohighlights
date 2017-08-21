# python function to run text scraper

import scrapy
import logging
from Flask_App.autoscraper.spiders.url_text_spider import URLTextSpider
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


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)
