# -*- coding: utf-8 -*-
import scrapy


class ScraperboncoinSpider(scrapy.Spider):

    name = 'scraperboncoin'
    allowed_domains = ['leboncoin.fr']
    start_urls = ['http://leboncoin.fr/']
    item_urls = []
    file_name = "data.csv"
    head = "Titre,Prix,Ville,Type de Bien,Pièces,Surface,Prix m2,Description,Url"
    with open(file_name,'a') as file:
        file.write('# -*- coding: utf-8 -*-')
        file.write('\n')
        file.write(head)
    
    def start_requests(self):
        url_base = "https://www.leboncoin.fr/ventes_immobilieres/offres/rhone_alpes/rhone/?o="
        max = 400
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
        data = ['','','','','','','','','']
        header = ['Titre','Prix','Ville','Type de bien','Pièces','Surface','Prix m2','Description','Url']
        
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
        #if data[5] is not '':
        #   surface = data[5].split(' ')
        #    surface = surface[0]
        #    prix = data[1].split(' ')
        #    prix = int(prix[0]) * 1000
        #    prix = prix/surface
        #    data[6] = str(prix)
 
        #ranger les datas
        data[0] = name
        data[2] = response.css('span.value[itemprop="address"]::text').extract_first().strip()
        data[7] = response.css('p.value::text').extract_first()
        data[8] = response.url
        
        print(data)
        #ranger les infos pour imprimer dans le fichier
        ligne_infos = '\n'
        for dat in data:
            dat = dat.replace(',',' ')
            ligne_infos = ligne_infos + ',' + dat
            
        with open(self.file_name, "a") as fichier:
	           fichier.write(ligne_infos)
	    	           
        yield None
        
        # python json2csv/gen_outline.py --collection nodes test.js
        #python json2csv/json2csv.py test.json