from Main.ClassUtil import Share

__author__ = 'lisongfeng'


#coding=utf-8
import threading
from selenium import webdriver
import Util
import time
import re
import urllib2
from bs4 import BeautifulSoup

browser = webdriver.Firefox()

#url = "http://yun.baidu.com/share/home?uk=222226216&third=1&view=share"
#url = 'http://yun.baidu.com/share/home?uk=1732993866&view=fans'
url='http://yun.baidu.com/pcloud/friendpage?type=fans&uk=1732993866'
browser.get(url)
js="var q=document.documentElement.scrollTop=10000"
browser.execute_script(js)
#time.sleep(20)
p = browser.page_source
soup = BeautifulSoup(p,'html.parser')
#print soup.prettify()
#print soup
links = soup.find_all("li",'share-personage-item fl')
userlists=[]
for link in links:
    tag = link.find('p','share-personage-msg clear')
    shareList = tag.find_all('a')
    shareObj = Share(0,0,0)
    ukNode=shareList[0].get("href")
    shareObj.uk=ukNode.split("uk=")[1].split("&")[0]

    registNode=shareList[2]
    registNum=registNode.find('b').text
    shareObj.regist=registNum
    fansNode=shareList[3]
    fansNum=fansNode.find('b').text
    shareObj.fans=fansNum

    if shareObj.regist > 5:
        userlists.append(shareObj)
userlists.sort()
userlists.filter()
print(userlists)
