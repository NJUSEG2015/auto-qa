
import os
import time
import jieba
import jieba.analyse
import subprocess
import pytesseract
from PIL import Image


def take_screenshot():
    #output = subprocess.getoutput("idevicescreenshot screen.png")
    os.system("idevicescreenshot screen.png")


def split_word(words):
    words = jieba.analyse.extract_tags(words)
    stop_words = ["什么", "哪些", "哪个", "以下"]
    return [ w for w in words if w not in stop_words]


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

    question = split_word(question)
    candidates = [split_word(c) for c in candidates]

    print(question, candidates)

    return text


def open_browser(text):

    url = "https://www.baidu.com/s?wd=" + text
    subprocess.Popen(["google-chrome", url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


if __name__ == "__main__":

    jieba.initialize()

    text = ""
    while True: 

        input("[Enter]")

        t1 = time.time()
        take_screenshot()
        print(time.time() - t1)

        current = image_to_text()
        t2 = time.time()
        print(t2 - t1)
        exit()
        if current == text:
            continue
        text = current
        open_browser(text)


