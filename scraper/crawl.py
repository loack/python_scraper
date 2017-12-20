from selenium import webdriver
from pyvirtualdisplay import Display



display = Display(visible=0, size=[800, 600])
display.start()
print("lancement")
driver = webdriver.Firefox()   

driver.get("http://www.industrie-expo.com/liste-catalogue-exposants/")  

print("")
  
pageid = 2
while True:
    try:
        driver.execute_script("searchExposant(" + str(pageid) + ", '#')")
        pageid += 1
        print(pageid)
    except:
        break
        

driver.close()
display.close()
#http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python

