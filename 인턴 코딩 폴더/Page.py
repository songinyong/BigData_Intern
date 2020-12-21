# -*- coding: utf-8 -*-
import requests 
from urllib.parse import urlparse

import re
from bs4 import BeautifulSoup

#url에서 페이지 번호를 붙혀서 리턴해주는 함수
def PageChange(url, num):
    purl = url + '&pageNo=' + str(num)
    nospaceURL = re.sub('|\t|\r|\n', '', purl)
    return nospaceURL

#api에서 제공해주는 전체 페이지 수를 리턴해주는 함수 
def PageCount(url):
    result = requests.get(urlparse(url).geturl(), headers={})

    xml_obj = result.text
    soup = BeautifulSoup(xml_obj, 'html.parser')

    pages = soup.select_one('totalcount').get_text()
    return pages

#api를 통해 전체 정보값을 받아오는 함수 / 원하는 속성값을 순차적으로 리스트에 저장 
def loopSearch(url, attr):
    list = []
    pages = PageCount(url)
    for i in range(1,int((int(pages)/10))+1):
        url2 = PageChange(url, i)
        result = requests.get(urlparse(url2).geturl(), headers={})

        xml_obj = result.text
        soup = BeautifulSoup(xml_obj, 'html.parser')
        item = soup.select('item')
        
        for info in item:
            for j in range(0, len(attr)):
                list.append(info.select_one(attr[j]).get_text())
      
    return list

