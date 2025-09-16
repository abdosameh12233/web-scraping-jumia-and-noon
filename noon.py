from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time 
import pandas as pd
product_name=input('Enter the product name: ')
num_of_pages=int(input('enter number of pages: '))
for i in range(1,num_of_pages+1):
    url=f'https://www.noon.com/egypt-en/search/?q={product_name}&page={i}'
    service=Service(ChromeDriverManager().install())
    browser=webdriver.Chrome(service=service)
    browser.get(url)
    time.sleep(5)
    items={}
    items['description']=[]
    items['num_of_ratings']=[]
    items['rating']=[]
    items['price_after_discount']=[]
    items['price_before_discount']=[]
    items['is_bestseller']=[]
    items['product_category']=[]
    products=browser.find_elements(By.CLASS_NAME,'ProductDetailsSection_wrapper__yLBrw')
    images=browser.find_elements(By.CLASS_NAME,'ProductImageHeader_wrapper__uAS4Q')
    product_img=zip(products,images)   
    for product,img in product_img:
        soup=BeautifulSoup(product.get_attribute('outerHTML'),'html.parser')
        best_seller=BeautifulSoup(img.get_attribute('outerHTML'),'html.parser')
        items['description'].append(soup.find('h2',{'class':'ProductDetailsSection_title__JorAV'}).text)
        if soup.find('div',{'class':'RatingPreviewStar_textCtr__sfsJG'}):
            items['num_of_ratings'].append(soup.find('span').text)
            items['rating'].append(soup.find('div',{'class':'RatingPreviewStar_textCtr__sfsJG'}).text)
        else:
            items['num_of_ratings'].append(0)
            items['rating'].append(0)
        if best_seller.find('span',{'class','BestSellerTag_text__1MRSg'}):
            items['is_bestseller'].append('Yes')
        else:
            items['is_bestseller'].append('No')
        if soup.find('span',{'class':'Price_oldPrice__ZqD8B'}):
            items['price_before_discount'].append(soup.find('span',{'class':'Price_oldPrice__ZqD8B'}).text)
        else:
            items['price_before_discount'].append(soup.find('strong',{'class':'Price_amount__2sXa7'}).text)
        items['price_after_discount'].append(soup.find('strong',{'class':'Price_amount__2sXa7'}).text)
        items['product_category'].append(product_name)
    df=pd.DataFrame(items)
    with open('noon.csv','a',newline='',encoding='utf-8-sig') as f:
        df.to_csv(f,encoding='utf-8-sig')
    print(i)
        
