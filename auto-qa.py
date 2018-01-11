#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import subprocess
import pytesseract
import urllib.request
import urllib.parse
import urllib.error
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screen():
    output = subprocess.getoutput("idevicescreenshot")
    png = output.split()[-1]
    os.rename(png, "screen.png")

def check_image(image):
    return True

def image_to_text(image):
    im = image.crop((0, 150, 750, 360))
    im.save("question.png")
    text = pytesseract.image_to_string(im, "chi_sim")
    text = "".join(text.split())
    text.replace("唧","哪")
    text.replace("_","一")
    print(text)
    return text


def open_browser(driver, text):
    url = "https://www.baidu.com"
    url += "/s?wd=" + text
    driver.get(url)


def answer(question, options):

    contents = list()
    url = "http://www.baidu.com/s?wd=" + urllib.parse.quote(question)
    print(url)
    with urllib.request.urlopen(url) as response:
        html = response.read()
    content = html.decode('utf-8')
    content = content.replace('\n', '').replace('\r', '')
    contents.append(content)

    href_regex = r'<h3.*?>.*?href\s*=\s*"(.*?)".*</h3>'
    h3_regex = r'<h3.*?/h3>'

    search_res = list()
    matches = re.findall(h3_regex, content)
    for m in matches:
        href = re.findall(href_regex, m)
        search_res.extend(href)

    #search_res = search_res[:3]
    for url in search_res:
        print(url)
        try:
            with urllib.request.urlopen(url) as response:
                char_set = (response.headers.get_content_charset())
                if not char_set:
                    char_set = 'utf-8'
                try:
                    content = response.read().decode(char_set)
                except UnicodeDecodeError:
                    content = response.read().decode('gbk')
            contents.append(content)
        except urllib.error.HTTPError:
            continue

    for option in options:
        appearance = 0
        for content in contents:
            appearance += content.count(option)
        print(option + ':' + str(appearance))


if __name__ == "__main__":

    '''
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    text = ""
    while True: 
        input("[Enter]")
        take_screen()
        image = Image.open("./screen.png")
        if check_image(image):
            current = image_to_text(image)
            if current == text:
                continue
            text = current
            open_browser(browser, text)
    '''

    options = ['杨贵妃', '西施', '嫦娥']
    answer('梨花带雨 形容 哪位 美女',options)


