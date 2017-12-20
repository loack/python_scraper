# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from pyvirtualdisplay import Display


class MailcrawlSpider(scrapy.Spider):
    name = 'mailcrawl'
    
    allowed_domains = ['industrie-expo.com']
    #start_urls = ['http://www.industrie-expo.com/liste-catalogue-exposants/']
    
    def start_requests(self):
        
        self.setUp()
        self.driver.get("http://www.industrie-expo.com/liste-catalogue-exposants/")
        
        pageid = 2
        while True:
            try:
                driver.execute_script("searchExposant(" + str(pageid) + ", '#')")
                pageid += 1
                print(pageid)
            except:
                break
        
        self.tearDown()
        
        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
              
    def setUp(self):
        self.display = Display(visible=0, size=[800, 600])
        self.display.start()
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()
        self.display.quit()
