from statistics import median_grouped
import this
from tkinter import N
from unicodedata import name
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)

gaUrl = "https://www.city-data.com/city/Georgia.html"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get(gaUrl)
time.sleep(3)
    
cityNames = []
cityHtml = []

select = Select(driver.find_element(By.ID, 'citySize'))
select.select_by_visible_text('All cities')
cityhtml = driver.page_source
citysoup = BeautifulSoup(cityhtml, 'html5lib')
cities = citysoup.findAll('tr',  {"class":["rB", "rS", "rT"]})
cities = citysoup.findAll('tr',  {"class":["rB", "rS", "rT"]})

data = []
citynames = []
for thing in cities:
    thisname={}
    s = thing.find('a').text
    s = s.replace(' ', '-')
    thisname["name"] = s.partition(',')[0]
    citynames.append(thisname)


for thing in citynames:
    print(thing["name"])
    print("https://www.city-data.com/city/"+thing["name"]+"-Georgia.html")
    response = requests.get("https://www.city-data.com/city/"+thing["name"]+"-Georgia.html")
    thiscitysoup = BeautifulSoup(response.text, 'html5lib')
    item={}
    item["name"]=thing["name"]
    print(item["name"])
    if(thiscitysoup.find('section', id="population-by-sex")):
        income = thiscitysoup.find('section', id="population-by-sex").text
        capitastart = income.find("Males")
        if(capitastart != -1):
            capitatext = income[capitastart:]
            begin = capitatext.find(":")
            end = capitatext.find("(")
            item["Males"] = capitatext[begin+2:end]
            print("males"+capitatext[begin+2:end])
        
        capitastart = income.find("Females")
        if(capitastart != -1):
            capitatext = income[capitastart:]
            begin = capitatext.find(":")
            end = capitatext.find("(")
            item["Females"] = capitatext[begin+2:end]
            print("femals"+capitatext[begin+2:end])
    
    if(thiscitysoup.find('section', id="median-age")):
    
        income = thiscitysoup.find('section', id="median-age").text
        capitastart = income.find("Median resident")
        if(capitastart != -1):
            capitatext = income[capitastart:]
            begin = capitatext.find(":")
            end = capitatext.find("y")
            item["MedianAge"] = capitatext[begin+1:end]
            print("age"+capitatext[begin+1:end])
        
        income = thiscitysoup.find('section', id="median-income").text
        capitastart = income.find("median household income")
        if(capitastart != -1):
            capitatext = income[capitastart:]
            begin = capitatext.find(":")
            end = capitatext.find("(")
            item["Medianincome"] = capitatext[begin+2:end]
            print("income"+capitatext[begin+2:end])


        capitastart = income.find("capita income")
        if(capitastart != -1):
            capitatext = income[capitastart:]
            begin = capitatext.find(":")
            end = capitatext.find("(")
            item["PerCapitaIncome"] = capitatext[begin+2:end]
            print(capitatext[begin+2:end])

        condostart = income.find("condo value")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            end = condotext.find("(")
            item["MeanCondoValue"] = condotext[begin+2:end]
            print(condotext[begin+2:end])

        condostart = income.find("all housing units")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            end = condotext.find(";")
            item["AllUnits"] = condotext[begin+2:end]
            print(condotext[begin+2:end])


        condostart = income.find("detached")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            end = condotext.find(";")
            item["Detached"] = condotext[begin+2:end]
            print(condotext[begin+2:end])

        condostart = income.find("townhouses")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            end = condotext.find(";")
            item["TownHouses"] = condotext[begin+2:end]
            print(condotext[begin+2:end])

        condostart = income.find("5-or")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            end = condotext.find(";")
            item["5-or"] = condotext[begin+2:end]
            print(condotext[begin+2:end])

        condostart = income.find("mobile homes")
        if(condostart != -1):
            condotext = income[condostart:]
            begin = condotext.find(":")
            item["MobileHomes"] = condotext[begin+2:]
            print(condotext[begin+2:])

    if(thiscitysoup.find('section', id="median-rent")):
        income = thiscitysoup.find('section', id="median-rent").text

        startIndex = income.find("gross rent")
        if(startIndex != -1):
            thistext = income[startIndex:]
            begin = thistext.find(":")
            end = thistext.find(";")
            item["MedianRent"] = thistext[begin+2:end]
            print(thistext[begin+2:end])

    if(thiscitysoup.find('section', id="cost-of-living-index")):
        income = thiscitysoup.find('section', id="cost-of-living-index").text

        startIndex = income.find("cost of living")
        if(startIndex != -1):
            thistext = income[startIndex:]
            begin = thistext.find(":")
            end = thistext.find("(")
            item["CostOfLivingIndex"] = thistext[begin+2:end]
            print(thistext[begin+2:end])
    
    if(thiscitysoup.find('section', id="real-estate-taxes")):
        income = thiscitysoup.find('section', id="real-estate-taxes").text

        startIndex = income.find("housing units with mortgages")
        if(startIndex != -1):
            thistext = income[startIndex:]
            begin = thistext.find(":")
            end = thistext.find("(")
            item["TaxesPaidWithMortgage"] = thistext[begin+2:end]
            print(thistext[begin+2:end])

        startIndex = income.find("housing units with no mortgage")
        if(startIndex != -1):
            thistext = income[startIndex:]
            begin = thistext.find(":")
            end = thistext.find("(")
            item["TaxesPaidNoMortgage"] = thistext[begin+2:end]
            print(thistext[begin+2:end])            
    


    
    data.append(item)    
       
    
def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel("newcitydata3.xlsx")

export_data(data)
print("Done.")
            