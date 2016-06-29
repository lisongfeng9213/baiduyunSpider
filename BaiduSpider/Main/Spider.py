#coding=utf-8
__author__ = 'lisongfeng'

from Main import Util
from Main.Util import QueueList

import threading
from selenium import webdriver
from bs4 import BeautifulSoup


def parseUrl(parseUtil):
#    print("parsing html")
    browser = webdriver.Firefox()

    uk = parseUtil.getId()
    url = Util.generateContentUrl(uk)
    browser.get(url)

    p = browser.page_source
    soup = BeautifulSoup(p,'html.parser')
    # print soup
    links = soup.find_all("dd")
    for link in links:
        if link.text == u'没有分享':
            continue
        linkUrl =  link.get("_link")
        titleNode = link.find(class_="col file-col")
        title = titleNode.get("title")
        parseUtil.save(linkUrl,title)
    browser.close()
    return

def multiThread(parseUtil):
    threads = []
    while True:
        if len(threads) <= 10:
            t1 = threading.Thread(target=parseUrl,args=(parseUtil,))
            t2=threading.Thread(target=parseFans,args=(parseUtil,))
            t3 = threading.Thread(target=parseUrl,args=(parseUtil,))

            threads.append(t1)
            threads.append(t2)
            threads.append(t3)

            t1.start()
            t2.start()
            t3.start()

        else:
#            threads = filter(lambda x: x.is_alive()==True, threads)
            for thread in threads:
                if thread.is_alive():
                    continue
                else:
                    threads.remove(thread)

def fansThread(parseUtil):
    threads = []
    while True:
        if threads.__len__() <= 20:
            uk = parseUtil.getFan()
            t1 = threading.Thread(target=parseFans,args=(parseUtil,))

            threads.append(t1)
            t1.start()

        else:
            for thread in threads:
                if thread.is_alive():
                    continue
                else:
                    threads.remove(thread)

def parseFans(parseUtil):
    uk = parseUtil.getFan()
    fanList = Util.getShareObjList(uk)
    for fan in fanList:
        parseUtil.saveFan(fan.uk)
        parseUtil.saveId(fan.uk)

if __name__ == '__main__':
    parseUtil = QueueList()
    parseUtil.saveId('772704687')
    parseUtil.saveId('1732993866')
    parseUtil.saveFan('772704687')
    parseUtil.saveFan('1732993866')
    multiThread(parseUtil)
    fansThread(parseUtil)

