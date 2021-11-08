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
    proxies = {"http":"http://kenproxyrack:24f9a7-b90669-298d41-03f7a9-d2cb14@usa.rotating.proxyrack.net:333",
	   "https":"http://kenproxyrack:24f9a7-b90669-298d41-03f7a9-d2cb14@usa.rotating.proxyrack.net:333"}
    return proxies

session = requests.Session()
ua = UserAgent()
headers = get_headers()
headers['origin'] = "https://www.drivetrainamerica.com"

def get_page_response(url,postmethod,data):
    Flag=True
    count  = 1
    while Flag:
        try:
            user_agent=ua.random
            headers['User-Agent'] = user_agent
            # print("url==",url)
            if postmethod == "get":
                response=session.get(url,headers=get_headers(),proxies=proxyList())
            if postmethod == "post":
                response=session.post(url,headers=get_headers(),data=data,proxies=proxyList())
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
                name=resp.xpath("//div[@class='productView-product']/h1/text()").extract()[0]
                name=name.strip()
                print("NAME===============",name)
                listOfGlobals['Short Description']=name
            except:
                print("N/A")
            # try:
            #     price=resp.xpath("//meta[@property='product:price:amount']/@content").extract()[0]
            #     price=price.strip()
            #     print("RETAIL PRICE==============",price)
            #     listOfGlobals['Retail Price']=price
            # except:
            #     print("N/A")
            try:
                item_condition=resp.xpath('//meta[@itemprop="itemCondition"]/@content').extract()[1]
                item_condition=item_condition.strip()
                print("ITEM NI CONDITION",item_condition)
                listOfGlobals['New OR Used']=item_condition
            except:
                print("N/A")
            try:
                In_Stock = resp.xpath("//meta[@property='og:availability']/@content").extract()[0]
                if "instock" in In_Stock:
                    In_Stock = 'Yes'
                elif In_Stock or In_Stock!='N/A':
                    In_Stock = 'No'
                else:
                    In_Stock = 'N/A'
                print("STOCK===============",In_Stock)
                listOfGlobals['In Stock']=In_Stock
            except:
                print("N/A")
            # try:
            #     currency_code=resp.xpath('//meta[@itemprop="priceCurrency"]/@content').extract()[0]
            #     print("CURRENCY CODE",currency_code)
            #     listOfGlobals['Currency Code']=currency_code
            # except:
            #     print("N/A")
            # avaible_qty=resp.xpath('//label[@class="form-label form-label--alternate"]/span/text()').extract()[0]
            # print(avaible_qty)
            try:
                Available_qty=resp.xpath('//input[@class="form-input form-input--incrementTotal"]/@value').extract()[0]
                print("AValable qtyyy==================",Available_qty)
                listOfGlobals['Min Order QTY']=Available_qty
                eum_1=Available_qty
                print("EA UOM NOUMBER=========================",eum_1)
                listOfGlobals['Number of EA UOM 1']=eum_1
            except:
                print("N/A")
            try:
                path=resp.xpath('//ul[@class="breadcrumbs"]/li/a/span/text()').extract()
                Category=path[1]
                print(Category)
                listOfGlobals['Category']=Category
                # sub_cat=path[2]
                # print(sub_cat)
                path=' >> '.join(path)
                print(path)
                listOfGlobals['Path']=path
            except:
                print("N/A")
            # try:
            #     available_qty=resp.xpath('//span[@class="VariationProductInventory"]/text()').extract()[0]
            #     print("[][][][][][][][][][][][][][][][]================090909090 : ",available_qty)
            # except:
            #     print("N/A")
                description=resp.xpath('//div[@class="tabs-contents"]/div[@class="tab-content is-active"]/text()').extract()
                description=' | '.join(description).replace('| |',' ').replace('|\n',' ').replace('|\n\n',' ').replace('\n\n\n',' ').replace('\n\n',' ').replace('|\n\n',' ').replace('\n',' ')
                description=description.strip()
                print("================================",description)
                sample=description.split('|')
                for dd in sample:
                    if 'APPLICATION' in dd:
                        print('>>>>>>>',dd)
                listOfGlobals['Long Description']=description
            try:
                desc_1=resp.xpath('//div[@class="tabs-contents"]/div[@class="tab-content is-active"]/p//text()').extract()
                desc_1= ' | '.join(desc_1).replace("  |   |   | "," | ").replace(' |   |   |  ',' | ').replace(' |   |  ',' | ')
                desc_1=desc_1.strip()
                print("FOR 9 url the description is : ",desc_1)
                try:
                    # des=desc_1.split("|")
                    # print("=============================================",des)
                    if 'OEM MFG' in desc_1:
                        # print("migration towards here   ::")
                        des12=desc_1.split('OEM MFG:')[1]
                        print("oem",des12)
                except:
                    pass
            except:
                pass
                try:
                    if 'OEM' in description:
                        des=description.split('OEM')[1].split()
                        # print(des)
                        if len(des[0])>2:
                            oem=des[0]
                        elif len(des[1])>2:
                            oem=des[1]
                        print("OEM number=================",oem)
                        listOfGlobals['OEM Part No']=oem
                except:print("N/A")
                try:
                    if 'Application' in description:
                        app=description.split('Application:')[1].replace(' |','')
                        print("AAAAPPLLICATIONSSSSS==",app)
                        listOfGlobals['Applications']=app
                    # if 'APPLICATION' in description:
                    #     app1=description.split('APPLICATION:')[1].split()
                    #     if len(des[0])>0:
                    #         paap=des[0]
                    #     print("AAAppllicationssssss :: ",paap)
                except:
                    print("N/A")
            att_json=resp.xpath("//script[contains(text(),'var BCData')]//text()").extract()
            listToStr = ''.join(map(str, att_json))
            json_d1=listToStr.replace('\n','').replace('var BCData = ','').rstrip(';')
            # print('>>>>',json_d1)
            json_data=json.loads(json_d1,strict=False)
            # print(json_dd_data)
            try:
                sku=json_data['product_attributes']['sku']
                print(sku)
                listOfGlobals['Item Number']=sku
            except:
                print("N/A")
            try:
                price=json_data['product_attributes']['price']['without_tax']['value']
                print("PRICE===========",price)
                listOfGlobals['Retail Price']=price
            except:
                print("N/A")
            try:
                upc=json_data['product_attributes']['upc']
                print(upc)
                listOfGlobals['UPC']=upc
            except:
                print("N/A")
            # try:
            #     weigth=json_data['product_attributes']['weight']['formatted']
            #     print(weigth)
            #     # listOfGlobals['Weight UOM 1']=weigth
            # except:
            #     print("N/A")
            try:
                currency_code=json_data['product_attributes']['price']['without_tax']['currency']
                print("curencyyyyy==========",currency_code)
                listOfGlobals['Currency Code']=currency_code
            except:
                print("N/A")
            try:
                available_qty=json_data['product_attributes']['stock']
                if available_qty==0:
                    print("N/A")
                    listOfGlobals['Case Quantity']=available_qty
                else:
                    print(available_qty)
                    listOfGlobals['Case Quantity']=available_qty
            except:
                print("N/A")
            # try:
                # stock=available_qty
                # print(stock)
                # listOfGlobals['Short Description']=name
            # except:
                # print("N/A")
            # in_stock = json_data['product_attributes']['instock']
            # print(in_stock)
            try:
                photo_1=resp.xpath('//li[@class="productView-thumbnail"][1]/a/@href').extract()[0]
                if 'freightliner-logo_' in photo_1:
                    print("N/A")
                else:
                    print(photo_1)
                    listOfGlobals['Photo 1']=photo_1
            except:
                print("N/A")
            try:
                photo_2=resp.xpath('//li[@class="productView-thumbnail"][2]/a/@href').extract()[0]
                print(photo_2)
                listOfGlobals['Photo 2']=photo_2
            except:
                print("N/A")
            try:
                photo_3=resp.xpath('//li[@class="productView-thumbnail"][3]/a/@href').extract()[0]
                print(photo_3)
                listOfGlobals['Photo 3']=photo_3
            except:
                print("N/A")
            try:
                image=photo_1
                print("IMAGE",image)
                listOfGlobals['Photo 1']=image
            except:
                print("N/A")
            try: 
                source='drivetrainamericacom'
                print(source)
                listOfGlobals['Source']=source
            except:
                print("N/A")
            try:
                source_url=url
                print("SOURCE URL :",source_url)
                listOfGlobals['Source URL']=source_url
            except:
                print('N/A')
            try:
                discount_you_save_amount = "N/A"
                listOfGlobals['Discount']=discount_you_save_amount
                discount_you_save_percentage = "N/A"
                listOfGlobals['Discount%']=discount_you_save_percentage
                unit_of_measure = "N/A"
                listOfGlobals['Unit of Measure 1']=unit_of_measure
                # weight = "N/A"
                # listOfGlobals['Weight UOM 1']=weight
                shipping_information = "N/A"
                listOfGlobals['Shipping Information']=shipping_information
                shipping_cost = "N/A"
                listOfGlobals['Shipping Cost']=shipping_cost
                cross_references = "N/A"
                listOfGlobals['Cross References']=cross_references
                warranty_information = "N/A"
                listOfGlobals['Warranty']=warranty_information
                # manufacturer_number="N/A"
                # listOfGlobals['Manufacturer Part No']=manufacturer_number
                location="N/A"
                listOfGlobals['Location']=location
                # extra="N/A"
                # listOfGlobals['Attribute Type 1,Attribute Value 1 to 50']=extra
            except:
                pass
            try:
                # print(db_variable)
                # listOfGlobals['UNSPSC']=''
                input_columns = [listOfGlobals[r] for r in db_variable ]
                print(input_columns)
                # insert_db(db_user_pass,tb_name,input_columns,db_variable)
                # update_db(db_user_pass,tb_name,url)
            except Exception as e:
                print(e)
def main():
    try:
        # urllist=from_queue_locations(db_user_pass,tb_name)
        # print(len(urllist))
        # for ur in urllist:
        #     # ########print(ur[1])
        #     get_data(ur[1])
# get_data(['https://parts.mhc.com/products/3000-watt-bluetooth%C2%AE-power-inverter-with-4-ac-2-usb-and-app-interface'])
#         # urlList=multiinstance_and_multirequest(int(sys.argv[3]), int(sys.argv[4]),db_user_pass,tb_name)
#         # print(urlList)
#         # p = Pool(int(sys.argv[5]))
#         # p.map(get_data, urlList)#call main funtion      
        get_data('https://www.drivetrainamerica.com/01-28042-000-freightliner-idler-pulley/')
        # get_data(['https://www.bigmachineparts.com//collections/freightliner/products/abs-electrical-and-air-assembly-3-in-1-cable-15ft-451098']) 
    except:
        status='2'
        pass
        # # status=2
        # completed_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # update_spider_jobs(db_user_pass,job_name,status,completed_date)#update status in table
        # logger1.exception(traceback.print_exc())
main()