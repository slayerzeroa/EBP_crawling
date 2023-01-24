'''
Author : slayerzeroa
Date : 2022-09-26
네이버 블로그 포스팅 자동화
'''

#pip install gensim==3.8.3
#pip install webdriver_manager
#pip install -U pyautoit


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
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from translate_content import start
import autoit
import os

# 네이버 자동 로그인

id = ''
password = ''

# 네이버 자동 로그인 가정

# 셀레니움
driver_1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver_1)

# 1. 네이버 접속
main_url = "http://naver.com"
blog_url = "https://blog.naver.com/gorapa_"
driver_1.get(main_url)

# 2. 로그인 버튼 클릭
elem = driver_1.find_element(By.CLASS_NAME, 'link_login')
elem.click()

# 3. id 복사 붙여넣기
elem_id = driver_1.find_element(By.ID, 'id')
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = driver_1.find_element(By.ID, 'pw')
elem_pw.click()
pyperclip.copy(password)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 5. 로그인 버튼 클릭
driver_1.find_element(By.ID, 'log.login').click()
time.sleep(10)

# 6. 블로그 접속
driver_1.get(blog_url)
# 프레임 이동
driver_1.switch_to.frame("mainFrame")

# 7. 글쓰기 버튼 클릭
elem = driver_1.find_element(By.XPATH, '//*[@id="post-admin"]/a[1]')
elem.click()
time.sleep(5)

# 8-1. 사진 첨부
driver_1.find_element(By.XPATH, '//button[contains(@class,"se-")]').click()
time.sleep(5)
handle = "[CLASS:#32770; TITLE:열기]"
time.sleep(5)
autoit.win_active("열기")
time.sleep(5)
img_path = "C:\\Users\\PSYDUCK\\PycharmProjects\\EBP_crawling\\pictures\\logo.PNG"
autoit.control_send(handle, "Edit1", img_path)
time.sleep(5)
autoit.control_click(handle, "Button1")
time.sleep(5)


# 네이버 컨텐츠 마련
translate_contents, translate_title = start()
print(translate_title)
print(translate_contents)


# 8. 내용 작성
action.send_keys("\n").perform()
time.sleep(5)
action.send_keys(translate_contents).perform()
time.sleep(5)
action.send_keys("\n").perform()
time.sleep(5)

# 9. 제목 작성
driver_1.find_element(By.XPATH, "//span[text()='제목']").click()
time.sleep(5)
action.send_keys(translate_title).perform()
time.sleep(5)


# 잡다한 sub panel 끄기
driver_1.find_element(By.CLASS_NAME, "se-help-panel-close-button").click()
time.sleep(5)

# 10. 발행 버튼 클릭
driver_1.find_element(By.XPATH, "//span[text()='발행']").click()
time.sleep(2)

# 11. 카테고리 버튼 클릭
driver_1.find_element(By.XPATH, "//span[text()='뉴스번역']").click()
time.sleep(2)
#
# # 12. 번역 카테고리 선택
# driver_1.find_element(By.XPATH, "//span[text()='번역']").click()
# time.sleep(2)

# 13. 발행
driver_1.find_element(By.CLASS_NAME, "confirm_btn__Dv9du").click()
time.sleep(10)

driver_1.close()