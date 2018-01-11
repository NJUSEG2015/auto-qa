#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import string
from zhon import hanzi
import jieba
import jieba.analyse
import subprocess
import pytesseract
import urllib.request
import urllib.parse
import urllib.error
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screenshot():
    os.system("idevicescreenshot screen.png")


def split_option(option):
    for p in string.punctuation:
        option = option.replace(p, ' ')
    for p in hanzi.punctuation:
        option = option.replace(p, ' ')
    return option.split()

def split_question(question):

    question = jieba.analyse.extract_tags(question)
    stop_words = ["什么", "哪些", "哪个", "以下", "下列"]
    return [w for w in question if w not in stop_words]


def image_to_text():

    image = Image.open("./screen.png")
    image = image.crop((0, 180, 750, 1000))
    text = pytesseract.image_to_string(image, "chi_sim")

    text = text.split("\n\n")

    question, candidates = text[0], text[1:]
    question = "".join(question.split())
    if '.' in question:
        question = question[question.index('.'):]
    candidates = [ "".join(c.split()) for c in candidates ]
    print(question)
    print(candidates)

    question = split_question(question)
    option = [split_option(c) for c in candidates]

    return question, option


def open_browser(text):
    url = "https://www.baidu.com/s?wd=" + text
    subprocess.Popen(["google-chrome", url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def answer(question_key_words, options_key_words):

    params = ' '.join(question_key_words)
    url = "http://www.baidu.com/s?wd=" + urllib.parse.quote(params)
    print(url)
    contents = list()
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

    search_res = search_res[:2]
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

    for option in options_key_words:
        appearance = 0
        for content in contents:
            for w in option:
                appearance += content.count(w)
        print(' '.join(option) + ':' + str(appearance))


if __name__ == "__main__":

    jieba.initialize()

    text = ""
    while True:

        input("[Enter]")

        t1 = time.time()
        take_screenshot()

        question_key_words, options_key_words = image_to_text()
        print(time.time() - t1)
        # open_browser(" ".join(question_key_words))

        answer(question_key_words, options_key_words)
        print(time.time() - t1)

