# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:33:51 2020

@author: Shasika
"""


from selenium import webdriver as webd
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib.request import urlopen as  uReq
import re
import csv

###################################################################################

def fSoup(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup

def soupFindAll(page_soup, arg1, arg2):
    return page_soup.findAll(arg1,arg2)

def printBreak():
    print ('-----------------------------------------')
    
    
def fIter(phrase, txt_body):
   return re.finditer(phrase, txt_body)

def button1(button):
    #button = str(button)
    button_cont = button.find("data-next-ajax-url=")
    button = button[button_cont:]
    button = button[20:]
    button_low = button.find("data-next-page-url=")  
    button_url = button[:button_low-2]
    return button_url

#####################################################################################

def fPage(urlX):
    #url1 = 'https://www.charleskeith.com/sg/sale/shoes'
    url1 = urlX
    page_soup = fSoup(url1)
    container_1 = soupFindAll(page_soup, "div", {"class" : "col-xs-6"})
    #button = soupFindAll(page_soup, "div", {"class" : "show-more product_list-load_more"})
    print (len(container_1))
    main_arr = []
    n = 0
    #item_arr = []
    for i in range(len(container_1)):  #len(container_1)
        n += 1
        print ("--------- "+ str(n)+" ----------")
        item_arr = []
        #print (container_1)
        container_2 = container_1[i]
        url1 = [i['href'] for i in container_2.find_all('a', href=True)]
        url1 = 'https://m.giordano.com'+str(url1[0])
        #print (url1)
        page_soup2 = fSoup(url1)
        container_3 = soupFindAll(page_soup2, "div", {"id" : "dvProductTitle"})
        name = (container_3[0].text)[19:50]
        #print (name)
        container_4 = soupFindAll(page_soup2, "span", {"id" : "ContentPlaceHolder1_ucProductInfo_lbProductDesc"})
        product_id = container_4[0].text
        #print (product_id)
        item_arr.append(product_id)
        item_arr.append(name[:-2])
        container_5 = soupFindAll(page_soup2, "span", {"id" : "lbCurPrice"})
        price = container_5[0].text
        #print (price)
        item_arr.append(price[1:-1])
        container_6 = soupFindAll(page_soup2, "div", {"class" : "col-xs-3 col-sm-3 col-md-2 col-lg-2"})
        #print (container_6[0])
        
        for i in range(len(container_6)):
            #print (i)
            color_arr = []
            container_7 = str(container_6[i])
            lim1 = container_7.find('onclick')
            tag =  (container_7[lim1+22 : lim1+24])
            #print (tag)
            url2 = url1 + '?StylID=' + product_id + '&SelectColor=' + tag
            #print (url2)
            #url12 = 'https://m.giordano.com/MY/en-US/Product/01017062002/12?StylID=01017062002&SelectColor=13'
            page_soup3 = fSoup(url2)
            container_8 = soupFindAll(page_soup3, "span", {"id" : "ContentPlaceHolder1_ucProductInfo_lbSelColor"})
            color = container_8[0].text
            #print (color)
            color_arr.append(color)
            container_9 = soupFindAll(page_soup3, "div", {"id" : "dvsizeList"})
            #print (len(container_9))
            container_9a = soupFindAll(container_9[0], "div", {"align" : "center"})
            #print (len(container_9a))
            stock_arr = []
            for j in range(len(container_9a)):
                container_10 = container_9a[j]
                size = (container_10.text)[1:-1]
                #print (size)
                stock_arr.append(size)
                #break
            color_arr.append(stock_arr)
            #print (color_arr)
            item_arr.append(color_arr)
        main_arr.append(item_arr)
    return main_arr
    

##################################################################################
def main():   
    i = 0    
    page_url = 'https://m.giordano.com/MY/en-US/CatePage.aspx?BrandID=&SysCateID=&GenderID=&SizeID=&PageID=5&Search=&CateID=GRP02270&Sort=SD#'
    main_arr = fPage(page_url)
    return main_arr
    
arr_ret = main()

##################################################################################

with open('07-07-2020-giordano-mens.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(54):
        ID = arr_ret[i][0]
        name = arr_ret[i][1]
        price = arr_ret[i][2]
        color = []
        for j in range(len(arr_ret[i])-3):
            color.append(arr_ret[i][j+3])
        writer.writerow([ID, name, price, color])
    
    
    
    
    
    
    
