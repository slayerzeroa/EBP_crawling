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
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
from translate_content import start

# 네이버 컨텐츠 마련
translate_contents, translate_title = start()
print(translate_title)
print(translate_contents)

# 네이버 자동 로그인

id = 'naver_id'
password = 'naver_password'

# 네이버 자동 로그인 가정

# 셀레니움
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver)

# 1. 네이버 접속
main_url = "http://naver.com"
blog_url = "https://blog.naver.com/slayerzeroa"
driver.get(main_url)

# 2. 로그인 버튼 클릭
elem = driver.find_element(By.CLASS_NAME, 'link_login')
elem.click()

# 3. id 복사 붙여넣기
elem_id = driver.find_element(By.ID, 'id')
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = driver.find_element(By.ID, 'pw')
elem_pw.click()
pyperclip.copy(password)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 5. 로그인 버튼 클릭
driver.find_element(By.ID, 'log.login').click()
time.sleep(10)

# 6. 블로그 접속
driver.get(blog_url)
# 프레임 이동
driver.switch_to.frame("mainFrame")

# 7. 글쓰기 버튼 클릭
elem = driver.find_element(By.XPATH, '//*[@id="post-admin"]/a[1]')
elem.click()
time.sleep(5)

# 9. 내용 작성
action.send_keys(translate_contents).perform()

time.sleep(4)

# 8. 제목 작성
driver.find_element(By.XPATH, "//span[text()='제목']").click()
time.sleep(1)
action.send_keys(translate_title).perform()


