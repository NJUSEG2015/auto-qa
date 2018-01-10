
import os
import time
import subprocess
import pytesseract
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


if __name__ == "__main__":

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


