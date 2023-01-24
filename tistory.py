'''
Author : slayerzeroa
Date : 2023-01-24
티스토리 블로그 포스팅 반자동화
'''

#pip install gensim==3.8.3
#pip install webdriver_manager
#pip install -U pyautoit


import requests
from bs4 import BeautifulSoup as BS
from gensim.summarization.summarizer import summarize
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
import clipboard

# # 네이버 컨텐츠 마련
# translate_contents, translate_title = start()
# print(translate_title)
# print(translate_contents)

id = ""
password = ''

# 셀레니움
driver_1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver_1)

# 1. 티스토리 로그인 접속
login_url = "https://www.tistory.com/auth/login"
driver_1.get(login_url)

# 2. 카카오 로그인 접속
elem = driver_1.find_element(By.CLASS_NAME, 'txt_login')
elem.click()

# 3. 아이디, 비밀번호 입력
elem_id = driver_1.find_element(By.NAME, 'loginKey')
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

elem_pw = driver_1.find_element(By.NAME, 'password')
elem_pw.click()
pyperclip.copy(password)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. 로그인 버튼 클릭
driver_1.find_element(By.CLASS_NAME, 'btn_g.highlight').click()
time.sleep(10)

# 5. 프로필 클릭
driver_1.find_element(By.CLASS_NAME, 'thumb_profile').click()

# 6. 작성 클릭
driver_1.find_element(By.CLASS_NAME, 'img_common_tistory.link_edit').click()

time.sleep(2)
autoit.send("{Enter}")
time.sleep(2)
# 7. 카테고리 선정
driver_1.find_element(By.ID, 'category-btn').click()
driver_1.find_element(By.XPATH, "//span[text()='- 번역']").click()

# 8. 내용 마련
translate_contents, translate_title = start()

# 9. 내용 및 제목 작성

driver_1.find_element(By.ID, "post-title-inp").click()
time.sleep(5)
action.send_keys(translate_title).perform()
time.sleep(5)


driver_1.find_element(By.ID, 'kakao-editor-container').click()
action.send_keys("\n").perform()
time.sleep(5)
action.send_keys(translate_contents).perform()
time.sleep(5)
action.send_keys("\n").perform()
time.sleep(5)

driver_1.find_element(By.ID, 'mceu_0-open').click()
time.sleep(5)
driver_1.find_element(By.ID, 'attach-image').click()
handle = "[CLASS:#32770; TITLE:열기]"
time.sleep(5)
autoit.win_active("열기")
time.sleep(5)
img_path = "C:\\Users\\PSYDUCK\\PycharmProjects\\EBP_crawling\\pictures\\logo.PNG"
autoit.control_send(handle, "Edit1", img_path)
time.sleep(5)
autoit.control_click(handle, "Button1")
time.sleep(5)


# 10. 완료 버튼 누르기
driver_1.find_element(By.ID, "publish-layer-btn").click()
time.sleep(5)
driver_1.find_element(By.ID, "publish-btn").click()
time.sleep(5)