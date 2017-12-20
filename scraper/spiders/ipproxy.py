# -*- coding: utf-8 -*-
#scraper liste de pr
import scrapy


class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['http://free-proxy-list.net/']

    def parse(self, response):
    
        ips = response.css('table[id*="proxylisttable"] tr')
        
        fichier = open("proxylist.txt", "w")
        
        for ip in ips:
            ext = ip.css('td::text').extract()
            if len(ext) >0:
                add = ext[0]
                port = ext[1]
                print(add + ":" + str(port))
                fichier.write("http://" + add + ":" + str(port) + "\n")
            #port = ip.css('td::text').extract()[1]
            ##print(add)
        fichier.close()
            
        yield {
            "ip": add,
            "port": port
        }
    pass




