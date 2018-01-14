#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import string
import functools

import _thread
import http.server

from PIL import Image
from zhon import hanzi
import jieba
import jieba.analyse
import subprocess
import pytesseract

from answer import answer
import highlightserver


def load_config(name):
    with open("config.json", 'r') as f:
        config = json.load(f)
    if name not in config:
        exit()
    config = config[name]
    return config['x1'], config['y1'],config['x2'],config['y2']


def take_screenshot():
    os.system("idevicescreenshot screen.png")


def split_option(option):
    for p in string.punctuation:
        option = option.replace(p, ' ')
    return option.split()


def extract_quote(question):
    quotes = []
    questions = []
    while "“" in question and "”" in question:
        questions.append(question[: question.index("“")])
        quotes.append(question[question.index("“") + 1 : question.index("”")])
        question = question[question.index("”") + 1:]
    questions.append(question)
    return questions, quotes


def split_question(question):

    questions, quotes = extract_quote(question)

    words = []
    for q in questions:
        words.extend(jieba.analyse.extract_tags(q))
    words.extend(quotes)

    stop_words = ["什么", "哪些", "哪个", "以下", "下列"]
    return [ w for w in words if w not in stop_words ]


def image_to_text(config):

    image = Image.open("screen.png")
    image = image.crop(config)
    image.save("question.png", dpi=(326, 326))

    text = subprocess.getoutput("tesseract question.png stdout -l chi_sim 2>/dev/null")
    text = text.split("\n\n")

    question, options = text[0], "\n".join(text[1:])

    question = "".join(question.split())
    if question.startswith("10.") or question.startswith("11.") or question.startswith("12."):
        question = question[3:]
    elif ('1' <= question[0] <= '9') and question[1] == '.':
        question = question[2:]

    options = [ i.strip() for i in options.split("\n") if i.strip() != "" ]
    options = [ "".join(i.split()) for i in options]

    print(question)
    print(options)

    question = split_question(question)
    options = [split_option(c) for c in options]

    return question, options


def open_browser(text):
    url = "https://www.baidu.com/s?wd=" + text
    subprocess.Popen(["google-chrome", url, "--allow-running-insecure-content"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def backup_screen(backup):
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    subprocess.Popen(["cp", "screen.png", backup + "/screen-" + current_time + ".png"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    subprocess.Popen(["cp", "question.png", backup + "/question-" + current_time + ".png"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: python3 " + sys.argv[0] + " app_name")
        print("app_name: watermelon | superman | rush")
        exit()

    config = load_config(sys.argv[1])

    jieba.initialize()

    backup = time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(backup):
        os.mkdir(backup)

    _thread.start_new_thread(highlightserver.run, ())

    while True:

        input("[Enter]")

        # take_screenshot()
        t1 = time.time()

        question_key_words, options_key_words = image_to_text(config)

        if question_key_words == "":
            continue

        if len(options_key_words) == 0:
            key_word_set = ""
        else:
            key_word_set = set("".join(functools.reduce(lambda x, y: x + y, options_key_words)))
        highlightserver.highlight_key_words = ",".join(key_word_set)

        open_browser(" ".join(question_key_words))
        print(time.time() - t1) 
        
        backup_screen(backup)
        answer(question_key_words, options_key_words)


