import csv
import sys
from time import sleep as sl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from gspread.exceptions import WorksheetNotFound
import gspread
import os

def get_csv_filename(bookID):
    return f'Book_{bookID}.csv'

def get_existing_questions(bookID):
    existing_questions = set()
    filename = get_csv_filename(bookID)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # 確保行不是空的
                        existing_questions.add(row[0])  # 添加問題 ID
        except Exception as e:
            print(f"讀取 CSV 文件時發生錯誤: {e}")
    return existing_questions

def output(bookID, qstr, q, a):
    existing_questions = get_existing_questions(bookID)
    filename = get_csv_filename(bookID)
    if qstr not in existing_questions:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            q = q.replace('\n', ' ').strip()
            a = [option.replace('\n', ' ').strip() for option in a]
            writer.writerow([qstr, q] + a)
        print(f"添加新問題到 {filename}: {qstr}")
    else:
        print(f"問題 {qstr} 已存在於 {filename}，跳過")

def init():
    if len(sys.argv) > 1:
        bookID = sys.argv[1]
        print(f"處理 BookID: {bookID}")
    else:
        print("沒有提供 BookID")

    driver = webdriver.Chrome()
    driver.get("https://happyread.kh.edu.tw/readerquiz/khopenid/login_openid.php")
    openID_login = driver.find_element(By.CLASS_NAME, "btnSubmit")
    openID_login.click()
    login_button = driver.find_element(By.CLASS_NAME, "ui-button-text")
    login_button.click()
    username = driver.find_element(By.NAME, "userid")
    password = driver.find_element(By.NAME, "password")
    enter = driver.find_element(By.CLASS_NAME, "btn_submit")
    username.send_keys("")
    password.send_keys("")
    enter.click()
    bt_go = driver.find_element(By.NAME, "bt_go")
    bt_go.click()
    sl(.2)
    get_tr(driver, bookID)

def get_tr(driver, bookID):
    driver.get(f"https://happyread.kh.edu.tw/readerquiz/exam_sheet.php?id={bookID}")
    
    for _ in range(10):
        str_qstr = driver.find_element(By.NAME, "qstr")
        list_qstr = str_qstr.get_attribute("value").split(",")
        tr_list = driver.find_elements(By.TAG_NAME, "tr")
        ans = []
        question = ""
        now_question = -1

        for tr in tr_list:
            tr_text = tr.text.strip()
            if tr_text and tr_text[0] in "123456789":
                question = tr_text

            if tr_text and tr_text[0:3] in ["(1)","(2)","(3)","(4)"]:
                if len(ans) == 4 and question:
                    now_question += 1
                    qstr = list_qstr[now_question]
                    output(bookID, qstr, question, ans)
                    ans = []
                ans.append(tr_text)

        # 處理最後一個問題（如果有）
        if len(ans) == 4 and question:
            now_question += 1
            qstr = list_qstr[now_question]
            output(bookID, qstr, question, ans)

        # 遍歷完所有 tr 後刷新頁面
        driver.refresh()
        sl(.1)

init()