#coding=utf-8
# auther: yubb
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Ie()
driver.get("http://sit-report.m.com/20190908/1567926062.html")




'''
html=requests.get("http://sit-report.m.com/20190908/1567926062.html")
etree_html=etree.HTML(html.text)
content=etree_html.xpath('//*[@id="suite_2"]/tbody/tr[1]/td[3]/text()')
print content

'''
