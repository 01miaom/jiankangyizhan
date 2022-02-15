from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
from PIL import Image
import requests

browser=webdriver.Chrome("/usr/local/bin/chromedriver")#需要修改对应browser drive的路径

url="https://hk.sz.gov.cn:8118/userPage/login"
browser.get(url)

zhengjianleixing=Select(browser.find_element_by_id('select_certificate'))
zhengjianleixing.select_by_value('2')

zhengjianhaoma=browser.find_element_by_id('input_idCardNo')
zhengjianhaoma.send_keys('you_ID')#需要在此输入通行证号码

mima=browser.find_element_by_id('input_pwd')
mima.send_keys('password')#需要在此输入密码

#验证码截取
browser.get_screenshot_as_file('spider/screenshot.png')
element = browser.find_element_by_id('img_verify')
left = int(element.location['x'])
top = int(element.location['y'])
right = int(element.location['x'] + element.size['width'])
bottom = int(element.location['y'] + element.size['height'])
im = Image.open('spider/screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('spider/code.png')

#验证码识别
ocr=ddddocr.DdddOcr()
with open('spider/code.png','rb') as f:
    img_bytes=f.read()
res=ocr.classification(img_bytes)
print(res)

yanzhengma=browser.find_element_by_id('input_verifyCode')
yanzhengma.send_keys(res)

browser.find_element_by_id('btn_login').click()

#get time by using taobao api，这一行之前的代码可以在10点前执行
import json
from urllib import request
from urllib.request import Request,urlopen
import time
browser.set_page_load_timeout(200)
browser.set_script_timeout(200)
url="http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
while 1==1:
    r=Request(url)
    js=urlopen(r)
    data=js.read()
    data=str(data)
    timeArray=time.localtime(int(data[149:162]))
    jsTime=time.strftime("%Y-%m-%d %H:%M:%S")
    nowTime=jsTime[11:19]
    if nowTime=="10:00:00":
        browser.find_element_by_id('a_canBookHotel').click()
        element=WebDriverWait(browser,120,0.1).until(
            EC.presence_of_element_located((By.ID,"divSzArea"))
            )
        browser.find_element_by_class_name('orange').click()
        print(nowTime)
        break;

#预定确认页面验证码自动填写和提交
browser.get_screenshot_as_file('spider/screenshot.png')
element = browser.find_element_by_id('img_verify')
left = int(element.location['x'])
top = int(element.location['y'])
right = int(element.location['x'] + element.size['width'])
bottom = int(element.location['y'] + element.size['height'])
im = Image.open('spider/screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('spider/code.png')
ocr=ddddocr.DdddOcr()
with open('spider/code.png','rb') as f:
    img_bytes=f.read()
res=ocr.classification(img_bytes)
print(res)
yanzhengma1=browser.find_element_by_id('checkCode')
yanzhengma1.send_keys(res)
browser.find_element_by_id('btnSubmit').click()
browser.find_element_by_xpath("//span[text()=\"确定\"]").click()
