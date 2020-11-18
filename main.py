import sys
import requests
import os.path
from os import path
import json
from urllib.parse import unquote
from urllib.parse import urlparse


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

def loadConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = ''

    with open('token.txt','r') as f:
        bot_token = f.read().strip()
    
    with open('user.txt','r') as f:
        bot_chatID = f.read().strip()
   
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + unquote(bot_message)
    response = requests.get(send_text)
    return response.json()


def sendNotification(url):
    print("CHANGE IN URL:  %s" % (url))
    #file = "sound.mp3"
    #os.system("afplay " + filei)
    domain = urlparse(url).netloc
    print(telegram_bot_sendtext("CHANGE IN URL " + domain))


def writeFile(fileName, text):
    f = open(fileName, "w")
    f.write(text)
    f.close()

def checkPattern(url, pattern, cookies=[]):
    req = requests.get(url, verify=False, cookies=cookies, headers=headers)
    page = req.text
    #writeFile("test.html", page)
    if (page.find(pattern) < 0):
        sendNotification(url)
    else:
        print("Pattern found")

def checkFileChange(url, file_name, cookies=[]):
    req = requests.get(url, verify=False, cookies=cookies, headers=headers)
    page = req.text

    if (not os.path.isfile(file_name)):
        writeFile(file_name, page)
    else:
        my_file = open(file_name, "r")
        file_content = my_file.read()
        if (page.strip() == file_content.strip()):
            print("Same file")
        else:
            sendNotification(url)
            writeFile(file_name, page)


def main():
    a = loadConfig()

    for website in a:
        print(website)
        cookies = []
        if ("cookies" in website):
            cookies = website['cookies']

        if ("pattern" in website):
            checkPattern(website['url'], website['pattern'], cookies)
        else:
            checkFileChange(website['url'], website['file'], cookies)

if __name__ == "__main__":
    main()
