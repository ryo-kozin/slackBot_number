#!/usr/bin/python3
# coding: UTF-8
import flask
from flask import request, Response
import json
import requests
import codecs
import time
import sys
import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import traceback
import urllib
# import unicode
# import mysql.connector as MySQLdb
#設定ファイルの読み込み(iniファイルはフルパスにしないと動かない)
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/slackbot_config.ini', encoding='utf-8')


WEB_HOOK_URL = config.get('WEBHOOK','URL2')

# f = sys.argv[1].encode('utf-8')
# get = urllib.parse.quote(f)

user = sys.argv[1]
ts = sys.argv[2]
get = sys.argv[3]
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("/var/www/html/chromedriver", chrome_options=chrome_options)

try:

    # google = "https://www.google.co.jp"
    # driver.get(google)
    # search_bar = driver.find_element_by_name("q")
    # search_bar.send_keys(get)
    # search_bar.submit()
    # themes = driver.find_elements_by_xpath("//div[@class=\'r\']/a/h3")
    # urls = driver.find_elements_by_xpath("//div[@class=\'r\']/a")

    google =  "https://www.google.com/search?q={}&safe=off".format(get)
    driver.get(google)
    themes = driver.find_elements_by_xpath("//div[@id=\"rso\"]/div/div/div[1]/a/h3/span")
    urls = driver.find_elements_by_xpath("//*[@id=\"rso\"]/div/div/div[1]/a")
    print(themes)
    print(urls)
    li = []

    num = 0

    for theme, url in zip(themes, urls):
        if num > 4:
            break
        th = theme.text
        ur = url.get_attribute('href')
        li.append([th, ur])
        num += 1
        word = '以下が参考資料です！\n'

    a = int(1)

    for response in li:
        word += str(a) + '<' + response[1] + '|' + response[0] + '> \n'
        a += 1

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "thread_ts": ts,
        "blocks": [
            {
                "type": "section",
                "block_id": "section1",
                "text": {
                    "type": "mrkdwn",
                    "text": word
                }
            }
        ]
    }))
    driver.quit()

except Exception as e:
    print('type:' + str(type(e)))
    print('args:' + str(e.args))
    print('e:' + str(e))
    requests.post(WEB_HOOK_URL, data=json.dumps({
        "thread_ts" : ts,
        "text": "不具合が起こっています。管理者にお問い合わせ下さい。"
    }))