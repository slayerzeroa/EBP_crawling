import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

import schedule

import gspread
from oauth2client.service_account import ServiceAccountCredentials

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("window-size=1400, 1500")

# 서울대 경영대학 공지사항
def snu_biz_notice():
    title_list = []
    date_list = []
    from_list = []
    for i in range(1, 4):
        url = f'https://cba.snu.ac.kr/newsroom/notice?bbsid=notice_ko&page={i}'
        # get the data from the website
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # find the data
        titles = soup.find_all('span', {'class': ""})

        dates = soup.find_all('td', {'class': "text-center hidden-xs-down FS12"})

        for title, date in zip(titles, dates):
            title = str(title)
            title_list.append(re.sub('<.+?>', '', title))

            date = str(date)
            date_list.append(re.sub('<.+?>', '', date))

            from_list.append("서울대학교 경영대학")

    return pd.DataFrame({"제목":title_list, "마감일":date_list, "출처":from_list})

def kaist_biz_notice():
    url = 'https://cdc.kaist.ac.kr/'
    # get the data from the website
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # find the data
    titles = soup.find_all('a')
    title_list = []
    date_list = []
    from_list = []
    for title in titles:
        title = str(title)
        title_list.append(re.sub('<.+?>', '', title))
    # print the data
    title_list = title_list[33:-15]

    idx = 0
    for title in title_list:
        # remove the space and \n and \t and \r
        title = title.replace(" ", "")
        title = title.replace("\n", "")
        title = title.replace("\t", "")
        title = title.replace("\r", "")
        title_list[idx] = title
        date_list.append("?")
        from_list.append("KAIST 경영대학")
        idx += 1
    return pd.DataFrame({"제목":title_list, "마감일":date_list, "출처":from_list})

def snu_career_notice():

    url = 'https://career.snu.ac.kr/student'
    # get the data from the website using selenium


    # 브라우저 실행
    driver = wb.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2) # 2초간 정지

    # 리스트 생성
    article_list = []
    date_list = []
    from_list = []
    driver.implicitly_wait(10)


    # 공개채용 탭 크롤링
    driver.find_element(By.LINK_TEXT, "공개채용").send_keys(Keys.ENTER)
    # 서브 리스트 생성
    sub1_article_list = []
    sub1_date_list = []
    sub1_from_list = []
    for _ in range(10):
        driver.implicitly_wait(10)

        articles = "tit"
        article_raw = driver.find_elements(By.CLASS_NAME, articles)
        break_point = 0
        for i in range(len(article_raw)-12):
            if article_raw[i].text != "":
                if article_raw[i].text in sub1_article_list:
                    break_point = 1
                    break
                sub1_article_list.append(article_raw[i].text)
                sub1_from_list.append("서울대학교 공개채용")
        if break_point == 1:
            break
        date_raw = driver.find_elements(By.CLASS_NAME, 'date')
        for i in range(len(date_raw)):
            if date_raw[i].text != "":
                if date_raw[i].text[0] == "마":
                    sub1_date_list.append(date_raw[i].text)
                if date_raw[i].text == "채용시까지":
                    sub1_date_list.append(date_raw[i].text)
                if date_raw[i].text == "상시/수시채용":
                    sub1_date_list.append(date_raw[i].text)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti1"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti1"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        time.sleep(2)

    ad_flag = (len(sub1_date_list) == len(sub1_article_list))
    if ad_flag == True:
        modified = 0
    else:
        modified = len(sub1_date_list) - len(sub1_article_list)
        
        driver.find_element(By.LINK_TEXT, "공개채용").send_keys(Keys.ENTER)
        # 서브 리스트 생성
        sub1_article_list = []
        sub1_date_list = []
        sub1_from_list = []
        print(modified)
        
        for _ in range(10):
            driver.implicitly_wait(10)
    
            articles = "tit"
            article_raw = driver.find_elements(By.CLASS_NAME, articles)
            break_point = 0
            for i in range(len(article_raw)-(12-modified)):
                if article_raw[i].text != "":
                    if article_raw[i].text in sub1_article_list:
                        break_point = 1
                        break
                    sub1_article_list.append(article_raw[i].text)
                    sub1_from_list.append("서울대학교 공개채용")
            if break_point == 1:
                break
            date_raw = driver.find_elements(By.CLASS_NAME, 'date')
            for i in range(len(date_raw)):
                if date_raw[i].text != "":
                    if date_raw[i].text[0] == "마":
                        sub1_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "채용시까지":
                        sub1_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "상시/수시채용":
                        sub1_date_list.append(date_raw[i].text)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti1"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti1"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            time.sleep(2)
    
    article_list += sub1_article_list
    from_list += sub1_from_list
    date_list += sub1_date_list

    print(len(article_list))
    print(len(from_list))
    print(len(date_list))







    # 인턴십 탭 크롤링
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "인턴십").send_keys(Keys.ENTER)
    time.sleep(2)
    
    # 서브 리스트 생성
    sub2_article_list = []
    sub2_date_list = []
    sub2_from_list = []
    for _ in range(10):
        driver.implicitly_wait(10)
        articles = "tit"
        article_raw = driver.find_elements(By.CLASS_NAME, articles)
        break_point = 0
        for i in range(len(article_raw)-12):
            if article_raw[i].text != "":
                if article_raw[i].text in sub2_article_list:
                    break_point = 1
                    break
                sub2_article_list.append(article_raw[i].text)
                sub2_from_list.append("서울대학교 인턴십")
        if break_point == 1:
            break
        date_raw = driver.find_elements(By.CLASS_NAME, 'date')
        for i in range(len(date_raw)):
            if date_raw[i].text != "":
                if date_raw[i].text[0] == "마":
                    sub2_date_list.append(date_raw[i].text)
                if date_raw[i].text == "채용시까지":
                    sub2_date_list.append(date_raw[i].text)
                if date_raw[i].text == "상시/수시채용":
                    sub2_date_list.append(date_raw[i].text)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti3"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti3"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        time.sleep(2)

    ad_flag = (len(sub2_date_list) == len(sub2_article_list))
    if ad_flag == True:
        modified = 0
    else:
        modified = len(sub2_date_list) - len(sub2_article_list)

        print(modified)

        driver.find_element(By.LINK_TEXT, "인턴십").send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 서브 리스트 생성
        sub2_article_list = []
        sub2_date_list = []
        sub2_from_list = []
        for _ in range(10):
            driver.implicitly_wait(10)
            articles = "tit"
            article_raw = driver.find_elements(By.CLASS_NAME, articles)
            break_point = 0
            for i in range(len(article_raw)-(12-modified)):
                if article_raw[i].text != "":
                    if article_raw[i].text in sub2_article_list:
                        break_point = 1
                        break
                    sub2_article_list.append(article_raw[i].text)
                    sub2_from_list.append("서울대학교 인턴십")
            if break_point == 1:
                break
            date_raw = driver.find_elements(By.CLASS_NAME, 'date')
            for i in range(len(date_raw)):
                if date_raw[i].text != "":
                    if date_raw[i].text[0] == "마":
                        sub2_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "채용시까지":
                        sub2_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "상시/수시채용":
                        sub2_date_list.append(date_raw[i].text)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti3"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti3"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            time.sleep(2)
    
    article_list += sub2_article_list
    from_list += sub2_from_list
    date_list += sub2_date_list


    print(len(article_list))
    print(len(from_list))
    print(len(date_list))






    # 아르바이트 탭 크롤링
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "아르바이트").send_keys(Keys.ENTER)
    
    # 서브 리스트 생성
    sub3_article_list = []
    sub3_date_list = []
    sub3_from_list = []
    for _ in range(10):
        driver.implicitly_wait(10)
        articles = "tit"
        article_raw = driver.find_elements(By.CLASS_NAME, articles)
        break_point = 0
        for i in range(len(article_raw)-12):
            if article_raw[i].text != "":
                if article_raw[i].text in sub3_article_list:
                    break_point = 1
                    break
                sub3_article_list.append(article_raw[i].text)
                sub3_from_list.append("서울대학교 아르바이트")
        if break_point == 1:
            break
        date_raw = driver.find_elements(By.CLASS_NAME, 'date')
        for i in range(len(date_raw)):
            if date_raw[i].text != "":
                if date_raw[i].text[0] == "마":
                    sub3_date_list.append(date_raw[i].text)
                if date_raw[i].text == "채용시까지":
                    sub3_date_list.append(date_raw[i].text)
                if date_raw[i].text == "상시/수시채용":
                    sub3_date_list.append(date_raw[i].text)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti4"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti4"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        time.sleep(2)

    ad_flag = ((len(sub3_date_list) - len(sub3_article_list)) == 0)
    if ad_flag == True:
        modified = 0
    else:
        modified = len(sub3_date_list) - len(sub3_article_list)
        print(modified)
        
        driver.find_element(By.LINK_TEXT, "아르바이트").send_keys(Keys.ENTER)
        
        # 서브 리스트 생성
        sub3_article_list = []
        sub3_date_list = []
        sub3_from_list = []
        for _ in range(10):
            driver.implicitly_wait(10)
            articles = "tit"
            article_raw = driver.find_elements(By.CLASS_NAME, articles)
            break_point = 0
            for i in range(len(article_raw)-(12-modified)):
                if article_raw[i].text != "":
                    if article_raw[i].text in sub3_article_list:
                        break_point = 1
                        break
                    sub3_article_list.append(article_raw[i].text)
                    sub3_from_list.append("서울대학교 아르바이트")
            if break_point == 1:
                break
            date_raw = driver.find_elements(By.CLASS_NAME, 'date')
            for i in range(len(date_raw)):
                if date_raw[i].text != "":
                    if date_raw[i].text[0] == "마":
                        sub3_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "채용시까지":
                        sub3_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "상시/수시채용":
                        sub3_date_list.append(date_raw[i].text)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti4"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti4"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            time.sleep(2)

    article_list += sub3_article_list
    from_list += sub3_from_list
    date_list += sub3_date_list
    
    print(len(article_list))
    print(len(from_list))
    print(len(date_list))
    
    
    
    
    
    
    # 기타 탭 크롤링
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "기타").send_keys(Keys.ENTER)

    # 서브 리스트 생성
    sub4_article_list = []
    sub4_date_list = []
    sub4_from_list = []
    
    for _ in range(10):
        driver.implicitly_wait(10)
        articles = "tit"
        article_raw = driver.find_elements(By.CLASS_NAME, articles)
        break_point = 0

            
        for i in range(len(article_raw)-12):
            if article_raw[i].text != "":
                if article_raw[i].text in sub4_article_list:
                    break_point = 1
                    break
                sub4_article_list.append(article_raw[i].text)
                sub4_from_list.append("서울대학교 기타")
        if break_point == 1:
            break
        date_raw = driver.find_elements(By.CLASS_NAME, 'date')
        for i in range(len(date_raw)):
            if date_raw[i].text != "":
                if date_raw[i].text[0] == "마":
                    sub4_date_list.append(date_raw[i].text)
                if date_raw[i].text == "채용시까지":
                    sub4_date_list.append(date_raw[i].text)
                if date_raw[i].text == "상시/수시채용":
                    sub4_date_list.append(date_raw[i].text)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti5"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="noti5"]/div/div/div/div[1]').send_keys(Keys.ENTER)
        time.sleep(2)
    
    
    ad_flag = (len(sub4_date_list) - len(sub4_article_list) == 0)
    if ad_flag == True:
        modified = 0
    else:
        modified = len(sub4_date_list) - len(sub4_article_list)
        print(modified)

        driver.find_element(By.LINK_TEXT, "기타").send_keys(Keys.ENTER)
    
        # 서브 리스트 생성
        sub4_article_list = []
        sub4_date_list = []
        sub4_from_list = []
        
        for _ in range(10):
            driver.implicitly_wait(10)
            articles = "tit"
            article_raw = driver.find_elements(By.CLASS_NAME, articles)
            break_point = 0
    
            for i in range(len(article_raw)-(12-modified)):
                if article_raw[i].text != "":
                    if article_raw[i].text in sub4_article_list:
                        break_point = 1
                        break
                    sub4_article_list.append(article_raw[i].text)
                    sub4_from_list.append("서울대학교 기타")
            if break_point == 1:
                break
            date_raw = driver.find_elements(By.CLASS_NAME, 'date')
            for i in range(len(date_raw)):
                if date_raw[i].text != "":
                    if date_raw[i].text[0] == "마":
                        sub4_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "채용시까지":
                        sub4_date_list.append(date_raw[i].text)
                    if date_raw[i].text == "상시/수시채용":
                        sub4_date_list.append(date_raw[i].text)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti5"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, '//*[@id="noti5"]/div/div/div/div[1]').send_keys(Keys.ENTER)
            time.sleep(2)
    
    article_list += sub4_article_list
    from_list += sub4_from_list
    date_list += sub4_date_list
    

    print(len(article_list))
    print(len(from_list))
    print(len(date_list))
    
    
    return pd.DataFrame({"제목":article_list, "마감일":date_list, "출처":from_list})




def start():
    print("서울대학교 크롤링 시작")
    snu_biz = snu_biz_notice()
    print("서울대학교 크롤링 완료")
    
    print("카이스트 크롤링 시작")
    kaist_biz = kaist_biz_notice()
    print("카이스트 크롤링 완료")
    
    print("서울대학교 경력개발 크롤링 시작")
    snu_career = snu_career_notice()
    print("서울대학교 경력개발 크롤링 완료")
    
    
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'univ-biz-notice-e42ba2261df5.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1pHPcLwIVds0T-WW7B_kB_oOXj6KtOoM_mpTB8xNqH2Y/edit#gid=0'
    # 스프레스시트 문서 가져오기 
    doc = gc.open_by_url(spreadsheet_url)
    # 시트 선택하기
    worksheet = doc.worksheet('SNU_BIZ')
    
    # 시트의 모든 데이터 가져오기
    values = worksheet.get_all_values()
    header, rows = values[0], values[1:]
    data = pd.DataFrame(rows, columns=header)
    column_list = ["제목","작성일","출처"]
    data = data[column_list]
    data.head()
    
    worksheet.resize(snu_biz.shape[0]+1,10)
    list_range = f"a2:c{snu_biz.shape[0]+1}"
    cell_list = worksheet.range(list_range)
    
    idx = 0
    for i in range(len(cell_list)//len(column_list)):
        cell_list[(3*i)].value = snu_biz.iloc[idx, 0]
        cell_list[(3*i)+1].value = snu_biz.iloc[idx, 1]
        cell_list[(3*i)+2].value = snu_biz.iloc[idx, 2]
        idx += 1
    
    worksheet.update_cells(cell_list)
    
    
    # 시트 선택하기
    worksheet = doc.worksheet('KAIST_BIZ')
    
    # 시트의 모든 데이터 가져오기
    values = worksheet.get_all_values()
    header, rows = values[0], values[1:]
    data = pd.DataFrame(rows, columns=header)
    column_list = ["제목","마감일","출처"]
    data = data[column_list]
    data.head()
    
    worksheet.resize(kaist_biz.shape[0]+1,10)
    list_range = f"a2:c{kaist_biz.shape[0]+1}"
    cell_list = worksheet.range(list_range)
    
    idx = 0
    for i in range(len(cell_list)//len(column_list)):
        cell_list[(3*i)].value = kaist_biz.iloc[idx, 0]
        cell_list[(3*i)+1].value = kaist_biz.iloc[idx, 1]
        cell_list[(3*i)+2].value = kaist_biz.iloc[idx, 2]
        idx += 1
    
    worksheet.update_cells(cell_list)
    
    
    # 시트 선택하기
    worksheet = doc.worksheet('SNU_CAREER')
    
    # 시트의 모든 데이터 가져오기
    values = worksheet.get_all_values()
    header, rows = values[0], values[1:]
    data = pd.DataFrame(rows, columns=header)
    column_list = ["제목","마감일","출처"]
    data = data[column_list]
    data.head()
    
    worksheet.resize(snu_career.shape[0]+1,10)
    list_range = f"a2:c{snu_career.shape[0]+1}"
    cell_list = worksheet.range(list_range)
    
    idx = 0
    for i in range(len(cell_list)//len(column_list)):
        cell_list[(3*i)].value = snu_career.iloc[idx, 0]
        cell_list[(3*i)+1].value = snu_career.iloc[idx, 1]
        cell_list[(3*i)+2].value = snu_career.iloc[idx, 2]
        idx += 1
    
    print(1)
    worksheet.update_cells(cell_list)
    

# 하루에 한번씩 함수 실행
schedule.every(1).days.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)