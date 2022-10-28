from multiprocessing.sharedctypes import Value
from platform import release
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import math
from selenium import webdriver


url1 = 'https://mawdoo3.com/%D8%AA%D8%B1%D8%AA%D9%8A%D8%A8_%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A7%D8%AA_%D9%85%D8%B5%D8%B1_%D9%85%D9%86_%D8%AD%D9%8A%D8%AB_%D8%A7%D9%84%D9%85%D8%B3%D8%A7%D8%AD%D8%A9'


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept-Language': 'en-US,en;q=0.5'
}

page1 = requests.get(url1, headers=headers)
soup1 = BeautifulSoup(page1.content, "lxml")
table = soup1.find('table', class_='wikitable').find_all('tr')
regions_db = pd.DataFrame(columns=['name', 'radius', 'latitude', 'longitude'])
ind = 0

for i, region in enumerate(table):
    try:
        regions_db.at[ind, 'name'] = region.find_all('td')[0].text
        regions_db.at[ind, 'radius'] = round(math.sqrt(int(region.find_all('td')[1].text.replace(' ', '').replace('\n','').replace(',',''))/math.pi), 2)
        ind+=1
    except:
        pass
    

driver = webdriver.Edge('E:\Edge Webdriver\msedgedriver')
driver.get("https://www.gps-coordinates.net")
html = driver.page_source

for i in range(1000000000):
    pass

for cont in regions_db['name'].unique():

    for i in range(100000000):
        pass

    input = driver.find_element_by_id("address")
    input.clear()
    input.send_keys(cont+str(" مصر"))
    #print(input.get_attribute("value"))
    forms = driver.find_elements_by_class_name("form-horizontal")
    search_button = forms[0].find_element_by_tag_name("button")
    
    search_button.click()

    for i in range(100000000):
        pass

    lat = driver.find_element_by_id("latitude")
    lon = driver.find_element_by_id("longitude")

    latitude = lat.get_attribute("value")
    regions_db.at[regions_db[regions_db['name']==cont].index[0], 'latitude'] = latitude

    longitude = lon.get_attribute("value")
    regions_db.at[regions_db[regions_db['name']==cont].index[0], 'longitude'] = longitude
    
regions_db.to_csv('regions.csv')