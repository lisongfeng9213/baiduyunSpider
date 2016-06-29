__author__ = 'lisongfeng'
#coding=utf-8
import string
import threading
from selenium import webdriver
import time
import re
import urllib2
from bs4 import BeautifulSoup
class Share:
    uk=''
    fans=''
    regist=''
    def __init__(self,uk,fans,regist):
        self.uk=uk
        self.fans=fans
        self.regist=regist
    def __lt__(self, other):
         return string.atoi(self.regist) < string.atoi(other.regist)
    def __str__(self):
        return "uk: " + self.uk +" regist " + self.regist +  " fans :" + self.fans
