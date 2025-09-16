import requests
from bs4 import BeautifulSoup
import pandas as pd 
import csv
item=input('Enter the product name: ')
num_of_pages=int(input('enter number of pages: ')) 
def main(link):
    html=requests.get(link)
    soup=BeautifulSoup(html.text,'html.parser')
    products=soup.find_all('div',{'class':'info'})
    dic={}
    dic['discription']=[]
    dic['price_before_discount']=[]
    dic['price_after_discount']=[]
    dic['%_discount']=[]
    dic['product_category']=[]
    dic['rating']=[]
    dic['num_of_ratings']=[]
    for product in products:
        discription=product.find('h3').text
        dic['discription'].append(discription)
        price_after_discount=product.find('div',{'class':'prc'}).text
        dic['price_after_discount'].append(price_after_discount)
        if product.find('div',{'class':'old'}):
            discount=product.find('div',{'class':'bdg _dsct _sm'}).text
            old_price=product.find('div',{'class':'old'}).text 
        else:
            discount='%0'
            old_price=price_after_discount
        dic['%_discount'].append(discount)
        dic['price_before_discount'].append(old_price)
        dic['product_category']=item 
        if product.find('div',{'class':'rev'}):
            rating=product.find('div',{'class':'stars'}).text
            num_of_ratings=product.find('div',{'class':'rev'}).contents[-1].split('(')[-1].split(')')[0]
        else:
            rating='0 out of 5'
            num_of_ratings=0
        dic['rating'].append(rating)
        dic['num_of_ratings'].append(num_of_ratings)    
    df=pd.DataFrame(dic)
    with open('jumia.csv','a',newline='',encoding='utf-8-sig') as f:
        df.to_csv(f,encoding='utf-8-sig')        
for i in range(1,num_of_pages+1):
    url=f'https://www.jumia.com.eg/ar/catalog/?q={item}&page={i}#catalog-listing'
    main(url)
    print(i)
    
