'''
Author : slayerzeroa

Date : 2022-09-26

네이버 블로그 포스팅 자동화
'''

#pip install gensim==3.8.3
#pip install webdriver_manager

import requests
from bs4 import BeautifulSoup as BS
from gensim.summarization.summarizer import summarize
import docx
from datetime import date
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 셀레니움
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(3)

# link list
# link-title 딕셔너리
link_list = []
link_title = {}

def start():
    # CNN 비즈니스 탭 링크
    main_url = 'https://edition.cnn.com/business'
    driver.get(main_url)
    html = driver.page_source
    soup = BS(html, 'html.parser')
    tags = soup.select('#us-zone-1 > div.l-container > div > div.column.zn__column--idx-1 > ul > li:nth-child(1) > article > div > div.cd__content > h3')[0].find_all('a')
    for tag in tags:
        link_list.append(tag['href'])
        link_title[tag['href']] = tag.text  # 링크-타이틀 매칭

    headline_link = 'https://edition.cnn.com'+link_list[0]
    webpage = requests.get(headline_link)
    print(webpage)
    soup = BS(webpage.content, "html.parser")

    # CNN 본문내용 html class
    data = soup.find_all(class_= "zn-body__paragraph")
    data_text_all = ""

    title = soup.find("h1", class_="pg-headline")
    title_text = title.get_text()
    title_text = title_text.lstrip()
    # html 데이터에서 본문 텍스트만 뽑아오기
    for data_text in data:
      data_text = data_text.get_text()
      data_text_all = data_text_all + data_text

    # gensim summarize
    news_summarize = summarize(data_text_all, ratio=0.2, word_count = 350)

    # Papago API
    request_url = "https://openapi.naver.com/v1/papago/n2mt" #네이버 papago open api 사용
    headers = {"X-Naver-Client-Id": "f7l3yl8HU0pLQGLkXWEw", "X-Naver-Client-Secret": "KntXXNjbCh"} # id, secret id
    params = {"source": "en", "target": "ko", "text": news_summarize} # 언어 Domain, Codomain, Text
    response = requests.post(request_url, headers=headers, data=params)

    # API 오류 나면 이곳에서 확인
    result = response.json()
    translate_result = result['message']['result']['translatedText']

    params = {"source": "en", "target": "ko", "text": title_text} # 언어 Domain, Codomain, Text
    response = requests.post(request_url, headers=headers, data=params)
    result = response.json()
    translate_title = result['message']['result']['translatedText']

    return(translate_result, translate_title)