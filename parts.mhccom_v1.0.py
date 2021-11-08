from urllib.request import Request, urlopen, urljoin, URLError
from urllib.parse import urlparse
import ssl,requests,json,time,csv,random
import re
from bs4 import BeautifulSoup
import threading
import urllib
from urllib.request import Request, urlopen, urljoin, URLError
from urllib.parse import urlparse
import queue
import traceback
import random
import sys
from fake_useragent import UserAgent
import psycopg2
from random import randint
from psycopg2.extras import DictCursor
from psycopg2 import IntegrityError
from multiprocessing import Condition, Process, Pool
import random
import json
import os
from scrapy.http import HtmlResponse
from scrapy.http import HtmlResponse
import requests,os,sys,random,json,hashlib,random
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import sys
import sys,os
path = os.getcwd()#get current directory 
path_element = "/".join(path.split("/")[:-1])
path = path_element+'/config_sql'
print('path is : ',path)
sys.path.append(path)
from func import *

config_name_1= str(sys.argv[1]) 
config_name=config_name_1#get table name 
config_type = str(sys.argv[2])#script is for data or url specify in command 
proxies = 'torguard'

db_user_pass = all_db_details('110_sql')
insert_config(config_name,proxies,db_user_pass)#insert in project 
project_configs = get_my_project_config(db_user_pass,config_name,config_type)#get detail about script config
if project_configs:
    proxy_handler = get_proxy_details(db_user_pass,project_configs[3])
    db_variable = project_configs[8]
    table_name = project_configs[6]
    # db_user_pass = get_db_details(project_configs[7])
else:
    print("Something went wrong with project config !!")
    sys.exit()
    
if config_type != 'data': tb_name = '{}_location'.format(table_name)
else: tb_name = table_name
# created table of this table name

headers = get_headers()
#Getting headers 
session = requests.session()

for n, val in enumerate(db_variable):
        listOfGlobals = globals()
        globals()[val] = ''

columns=[]
def proxyList():
    proxyList = ["br.torguard.com","br2.torguard.com","ch.torguard.com","ca.torguard.com","cavan.torguard.com","mx.torguard.com","us-atl.torguard.com","us-la.torguard.com",
                 "us-fl.torguard.com","us-dal.torguard.com","us-nj.torguard.com","us-ny.torguard.com","us-chi.torguard.com","us-lv.torguard.com","us-sf.torguard.com",
                 "us-sa.torguard.com","us-slc.torguard.com","aus.torguard.com","bg.torguard.com","bul.torguard.com","cz.torguard.com","dn.torguard.com","fn.torguard.com","fr.torguard.com",
                 "ger.torguard.com","gre.torguard.com","hg.torguard.com","ice.torguard.com","ire.torguard.com","it.torguard.com","md.torguard.com","nl.torguard.com","no.torguard.com",
                 "pl.torguard.com","pg.torguard.com","ro.torguard.com","ru.torguard.com","slk.torguard.com","sp.torguard.com","swe.torguard.com","swiss.torguard.com","tk.torguard.com",
                 "ukr.torguard.com","uk.torguard.com","au.torguard.com","hk.torguard.com","id.torguard.com","jp.torguard.com","sk.torguard.com","nz.torguard.com","sg.torguard.com",
                 "sg2.torguard.com","tw.torguard.com","th.torguard.com","in.torguard.com","isr-loc1.torguard.com","sa.torguard.com","uae.torguard.com"]

    ports = ['6060','1337','1338','1339','1340','1341','1342','1343']
    # proxyData = "user6172786:H4cOb9dG@{}:{}".format(random.choice(proxyList),random.choice(ports))
    proxyData = "user6172786:H4cOb9dG@{}:{}".format('us-dal.torguard.com',random.choice(ports))
    proxy_handler={ "https": "https://"+proxyData,"http": "http://"+proxyData}
    return proxy_handler

session = requests.Session()
ua = UserAgent()
headers = get_headers()
headers['origin'] = "https://parts.mhc.com"

def get_page_response(url,postmethod,data):
    Flag=True
    count  = 1
    while Flag:
        try:
            user_agent=ua.random
            headers['User-Agent'] = user_agent
            # print("url==",url)
            if postmethod == "get":
                response=session.get(url,headers=get_headers())#,proxies=proxyList())
            if postmethod == "post":
                response=session.post(url,headers=get_headers(),data=data)#,proxies=proxyList())
            if response.status_code == 200 or response.status_code == 404:
                # print ("response",response.status_code)
                Flag=False
        except Exception as e:
            print("error111",e)
            pass
        count += 1
        if count > 50:
            Flag = False
    return response
        
def get_data(url):
        # url=url[0]
        print("URL is as follow",url)
        data=""
        response=get_page_response(url,postmethod="get",data=data)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'html.parser')
            resp = HtmlResponse(url="my HTML string", body=response.text, encoding='utf-8')
            try:
                In_Stock = resp.xpath("//meta[@property='product:availability']//@content").extract()[0].strip()
                if "instock" in In_Stock:
                    In_Stock = 'Yes'
                elif In_Stock or In_Stock!='N/A':
                    In_Stock = 'No'
                else:
                    In_Stock = 'N/A'
                print("In_Stock is:",In_Stock)
                listOfGlobals['New OR Used']=In_Stock
            except:
                pass
            try:
                Price=resp.xpath('//div[@class="ProductInfo-price"]//p/text()').extract_first()
                Price=Price.replace('$','').strip()
                print("Retail Price : ",Price)
                listOfGlobals['Retail Price']=Price
            except:
                print("N/A")
                pass
            try:
                Path=resp.xpath('//nav[@class="breadcrumb"]/a/text()').extract()
                Category=Path[1]
                print("CATEGORY=====",Category)
                listOfGlobals['Category']=In_Stock
                Path=' > '.join(Path)
                print("Path : " ,Path)
                listOfGlobals['Path']=Path
                # manu=resp.xpath("//div[@class='ProductSectionHeading ProductInfo-subTitle']//text()").extract()[0].strip()
                # print("==============================",manu)
            except:
                print("N/A")
                pass
            try:
                Part_Description_ele = resp.xpath("//div[@class='ProductInfo-description'][1]//div//text()").extract()
                Part_Description_ele = ''.join(Part_Description_ele)
                Part_Description = "|".join(Part_Description_ele.strip().replace("\n","").split("•"))
                print("Part_Description is=================:",Part_Description)
                if Part_Description.strip().startswith("|"):
                    Part_Description = Part_Description.strip()[1:].strip()
                print("Part_Description is:",Part_Description)
                listOfGlobals['Long Description']=Part_Description
                # Detailed_description=Part_Description
                # print("Detailed_description : ",Detailed_description)
                # listOfGlobals['New OR Used']=In_Stock
            except:
                print("N/A")
                pass
            jd_data=resp.xpath('//script[@type="application/json"][3]/text()').extract()[0]
            # print(jd_data)
            json_data=json.loads(jd_data, strict=False)
            # print("==========================",json_data)
            try:
                brand=json_data['product']['vendor']
                print("Brand : ",brand)
                listOfGlobals['Brand']=brand
            except:
                print("N/A")
                pass
            try:
                name=json_data['product']['title']
                print("Product name : ",name)
                listOfGlobals['Short Description']=name
            except:
                print("N/A")
                pass
            try:
                sku=json_data['product']['variants'][0]['sku']
                print("Sku number is : ",sku)
                listOfGlobals['Item Number']=sku
            except:
                print("N/A")
                pass
            try:
                photo1=json_data['product']['images'][0]
                print("Photo 1 :",photo1)
                listOfGlobals['Photo 1']=photo1
            except Exception as e:
                print("N/A")
                # print(e)
                # photo1="N/A"
                pass
            try:
                photo2=json_data['product']['images'][1]
                print("Photo 2 :",photo2)
                listOfGlobals['Photo 2']=photo2
            except Exception as e:
                print("N/A")
                # photo2="N/A"
                pass
            try:
                photo3=json_data['product']['images'][2]
                print("Photo 3 :",photo3)
                listOfGlobals['Photo 3']=photo3
            except Exception as e:
                print("N/A")
                # photo3="N/A"
                pass
            try:
                source_url=url
                print("SOURCE URL : ",source_url)
                listOfGlobals['Source URL']=source_url
            except:
                print("N/A")
                pass
            try:
                website="mhccom"
                print("Source : ",website)
                listOfGlobals['Source']=website
            except:
                print("N/A")
                pass
            try:
                currency_code=json_data['shop']['currency']
                print("Currency code : ",currency_code)
                listOfGlobals['Currency Code']=currency_code
            except:
                print("N/A")
                pass
            try:
                sub_category=json_data['product']['type']
                print("SubCategory : ",sub_category)
                listOfGlobals['Sub-category']=sub_category
            except:
                print("N/A")
                pass
            try:
                Image=json_data['product']['featured_image']
                print("Image : ",Image)
                listOfGlobals['Photo 1']=Image
            except:
                print("N/A")
                pass
            try:
                if brand !="N/A":
                    Manufracturer=brand
                print("Manufracturer : ",Manufracturer)
                listOfGlobals['Manufacturer']=Manufracturer
            except:
                print("N/A")
                pass
            try:
                discount_you_save_amount = "N/A"
                listOfGlobals['Discount']=discount_you_save_amount
                discount_you_save_percentage = "N/A"
                listOfGlobals['Discount%']=discount_you_save_percentage
                unit_of_measure = "N/A"
                listOfGlobals['Unit of Measure 1']=unit_of_measure
                weight = "N/A"
                listOfGlobals['Weight UOM 1']=weight
                shipping_information = "N/A"
                listOfGlobals['Shipping Information']=shipping_information
                shipping_cost = "N/A"
                listOfGlobals['Shipping Cost']=shipping_cost
                cross_references = "N/A"
                listOfGlobals['Cross References']=cross_references
                warranty_information = "N/A"
                listOfGlobals['Warranty']=warranty_information
                manufacturer_number="N/A"
                listOfGlobals['Manufacturer Part No']=manufacturer_number
                location="N/A"
                listOfGlobals['Location']=location
                extra="N/A"
                listOfGlobals['Attribute Type 1,Attribute Value 1 to 50']=extra
            except:
                pass
            input_columns = [listOfGlobals[x] for x in db_variable ]
            print(input_columns)
            insert_db(db_user_pass,tb_name,input_columns,db_variable)
            update_db(db_user_pass,tb_name,url)

def main():
    try:
        urllist=from_queue_locations(db_user_pass,tb_name)
        print(len(urllist))
        for ur in urllist:
            # print(ur[1])
            get_data(ur[1])
# get_data(['https://parts.mhc.com/products/3000-watt-bluetooth%C2%AE-power-inverter-with-4-ac-2-usb-and-app-interface'])
#         # urlList=multiinstance_and_multirequest(int(sys.argv[3]), int(sys.argv[4]),db_user_pass,tb_name)
#         # print(urlList)
#         # p = Pool(int(sys.argv[5]))
#         # p.map(get_data, urlList)#call main funtion      
        # get_data(['https://www.bigmachineparts.com/collections/freightliner/products/abs-sensor-970-5005'])
        # get_data(['https://www.bigmachineparts.com//collections/freightliner/products/abs-electrical-and-air-assembly-3-in-1-cable-15ft-451098']) 
    except:
        status='2'
        pass
        # # status=2
        # completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # update_spider_jobs(db_user_pass,job_name,status,completed_date)#update status in table
        # logger1.exception(traceback.print_exc())
main()
# get_data(['https://parts.mhc.com/products/3000-watt-bluetooth%C2%AE-power-inverter-with-4-ac-2-usb-and-app-interface'])