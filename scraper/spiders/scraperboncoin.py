# -*- coding: utf-8 -*-
import scrapy


class ScraperboncoinSpider(scrapy.Spider):

    name = 'scraperboncoin'
    allowed_domains = ['leboncoin.fr']
    start_urls = ['http://leboncoin.fr/']
    item_urls = []
    
    def start_requests(self):
        url_base = "https://www.leboncoin.fr/ventes_immobilieres/offres/rhone_alpes/?o="
        max = 1
        urls = []
        i = 0
 
        while i <= max:
            urls.append(url_base + str(i))
            i += 1
        print("urls à etudier : ")    
        print(urls)
        print("-----------------------------")
        print("crawl des pages de référence")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
            
            
    def parse(self, response):
        # listes des annonces de la page
        items = response.css('a.list_item::attr(href)').extract()
        
        for url in items:
            url = 'http:' + url  
            yield scrapy.Request(url=url, callback=self.parse_item)
        
        #self.item_urls.append(items)
        #print(self.item_urls)
        
    def parse_item(self, response):
        # extraire les infos de chacunes des annonces 
        name = response.css('h1[itemprop="name"]::text').extract_first()
        name = name.strip()
        #prix = response.css('h2.item_price::attr(content)').extract_first()
        #address = response.css('span[itemprop="address"]::text').extract_first()
        lines = response.css('div.line')
        url = ""
        data = []
        infos = ''
        for li in lines:
            prop = li.css('span.property::text').extract_first()
            val = li.css('span.value::text').extract_first()
            if val is not None:
                if prop is not None:
                    prop = prop.strip()
                    val = val.strip()
                    infos = infos + val + ','
                    data.append([prop,val])
                    
        description = response.css('p.value::text').extract_first()
        
        infos = '\n'+name + ',' + url + ',' + infos + ',' + description
        with open("data.csv", "a") as fichier:
	           fichier.write(infos)
	    	           
        yield {
            'Titre' : name,
            #'Data' : data,
            #'Description' : description.strip(),
            
        }
        
        # python json2csv/gen_outline.py --collection nodes test.js
        #python json2csv/json2csv.py test.json