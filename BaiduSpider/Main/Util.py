from Main.ClassUtil import Share

__author__ = 'lisongfeng'
import Queue
import string
import threading
from selenium import webdriver
import time
import re
import urllib2
from bs4 import BeautifulSoup
class QueueList:
    array = Queue.Queue(10000)
    result = Queue.Queue(10000)
    fans =  Queue.Queue(10000)
    def saveId(self,url):
        return self.array.put_nowait(url)
    def getId(self):
        return self.array.get()

    def saveFan(self,id):
        return self.fans.put_nowait(id)
    def getFan(self):
        return self.fans.get()

    def save(self,name,url):
        if name == None or url == None:
            return
        print 'got result :' + name +" : "+url
        if self.result.qsize() >= 30:
            f = open("file.txt",'a')
            while self.result.qsize() > 0:
                str = self.result.get()
                f.write(str+"\n")
            f.close()
        self.result.put_nowait(name + "|" + url)

def generateFansUrl(uk):
    url='http://yun.baidu.com/pcloud/friendpage?type=fans&uk='+uk
    return url
def generateContentUrl(uk):
    return 'http://yun.baidu.com/share/home?uk='+uk+'#category'
def getShareObjList(uk):
    browser = webdriver.Firefox()
    url = generateFansUrl(uk)
    browser.get(url)
    p = browser.page_source
    soup = BeautifulSoup(p,'html.parser')
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

        if shareObj.regist > '50' and shareObj.fans > '5':
            userlists.append(shareObj)
    browser.close()
    return userlists



