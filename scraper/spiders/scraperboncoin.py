# -*- coding: utf-8 -*-
import scrapy


class ScraperboncoinSpider(scrapy.Spider):

    name = 'scraperboncoin'
    allowed_domains = ['leboncoin.fr']
    start_urls = ['http://leboncoin.fr/']
    item_urls = []
    file_name = "data3.csv"
    head = 
    with open(file_name,'a') as file:
        file.write(head)
    
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
        data = ['','','','','','','','']
        header = ['Titre','Prix','Ville','Type de bien','Pièces','Surface','Description','Url']
        
        #extraction des datas de la feuille
        #propriétés
        lines = response.css('div.line')
        for li in lines:
            prop = li.css('span.property::text').extract_first()
            val = li.css('span.value::text').extract_first()
            
            if val is not None:
                val = val.strip()
                prop = prop.strip()
                try:
                    i = header.index(prop)
                    data[i] = val
                except:
                    None
 
        #ranger les datas
        data[0] = name
        data[6] = response.css('p.value::text').extract_first()
        data[5] = response.url
        print(data)
        
        #ranger les infos pour imprimer dans le fichier
        ligne_infos = '\n'
        for dat in data:
            ligne_infos = ligne_infos + ',' + dat
            
        with open("data3.csv", "a") as fichier:
	           fichier.write(ligne_infos)
	    	           
        yield None
        
        # python json2csv/gen_outline.py --collection nodes test.js
        #python json2csv/json2csv.py test.json