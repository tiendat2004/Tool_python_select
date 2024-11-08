import re
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import easyocr
import cv2
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import pyautogui
import io
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

service = Service(ChromeDriverManager().install())
web = webdriver.Chrome(service=service)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'D:/2024/Python_tool/hoadon'  # Thư mục chứa các tệp PDF
files = os.listdir(path)  # Lấy danh sách các tệp trong thư mục

for file in files:
    if file.endswith('.pdf'):
        f = os.path.join(path, file) 
        with pdfplumber.open(f) as pdf:
         page = pdf.pages[0]
         text = page.extract_text()
            

        Mst = re.findall(r'\d{10}', text)[0]
        MauSo = re.findall(r'\d\w{4,}/[0-9]{3,}', text)[0]
        KyHieuHD = re.findall(r'\w{2,4}/\w{3}', text)[1]
        SoHD = re.findall(r'\d{7}', text)[0]
        web.get('https://tracuuhoadon.gdt.gov.vn/tc1hd.html')
        sleep(2)
        mst = web.find_element(By.ID, "tin")
        ms = web.find_element(By.ID, "mau")
        kyhieu = web.find_element(By.ID, "kyhieu")
        sohd = web.find_element(By.ID, "so")
        btn = web.find_element(By.ID, "searchBtn")
        Captcha = web.find_element(By.ID, "captchaCodeVerify")
        sleep(2)
        mst.send_keys(Mst)
        ms.send_keys(MauSo)
        kyhieu.send_keys(KyHieuHD)
        sohd.send_keys(SoHD)
        sleep(1)
        web.get_screenshot_as_file("Anh.png")
        imgCv2 = cv2.imread("Anh.png")
        imgCrop = imgCv2[492:522,507:656]
        cv2.imwrite('Anh.png', imgCrop)
        reader = easyocr.Reader(['en', 'vi'],gpu=False)
        result = reader.readtext('Anh.png')
        text = result[0][-2]
        Captcha.send_keys(text)
        btn.click()
        sleep(1)
        mXt = web.find_element(By.ID, "lbLoiCode").text
        if mXt == "Sai mã xác thực!":
            for i in range(1, 10):
                web.get('https://tracuuhoadon.gdt.gov.vn/tc1hd.html')
                sleep(1)
                mst = web.find_element(By.ID, "tin")
                ms = web.find_element(By.ID, "mau")
                kyhieu = web.find_element(By.ID, "kyhieu")
                sohd = web.find_element(By.ID, "so")
                btn = web.find_element(By.ID, "searchBtn")
                Captcha = web.find_element(By.ID, "captchaCodeVerify")
                sleep(2)
                mst.send_keys(Mst)
                ms.send_keys(MauSo)
                kyhieu.send_keys(KyHieuHD)
                sohd.send_keys(SoHD)
                sleep(1)
                web.get_screenshot_as_file("Anh.png")
                imgCv2 = cv2.imread("Anh.png")
                imgCrop = imgCv2[492:522,507:656]
                cv2.imwrite('Anh.png', imgCrop)
                reader = easyocr.Reader(['en', 'vi'],gpu=False)
                result = reader.readtext('Anh.png')
                text = result[0][-2]
                Captcha.send_keys(text)
                btn.click()
                sleep(1)
                mXt = web.find_element(By.ID, "lbLoiCode").text
                if mXt != "Sai mã xác thực!":
                    pyautogui.hotkey('ctrl', 'p', 'enter')
                    break
                print('ok')
        else:
            pyautogui.hotkey('ctrl', 'p', 'enter')
web.quit()
