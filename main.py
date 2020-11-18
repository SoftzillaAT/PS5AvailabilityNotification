import sys
import requests
import os.path
from os import path
import json
from urllib.parse import unquote
from urllib.parse import urlparse

def loadConfig():
    with open(os.getcwd() + '/config.json') as json_file:
        return json.load(json_file)

def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = ''

    with open(os.getcwd() + '/token.txt','r') as f:
        bot_token = f.read().strip()
    
    with open(os.getcwd() + '/user.txt','r') as f:
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
    f = open(os.getcwd() + "/" + fileName, "w")
    f.write(text)
    f.close()

def checkPattern(url, pattern):
    req = requests.get(url, verify=False)
    page = req.text
    #writeFile("test.html", page)
    if (page.find(pattern) < 0):
        sendNotification(url)
    else:
        print("Pattern found")

def checkFileChange(url, file_name):
    req = requests.get(url, verify=False)
    page = req.text

    if (not os.path.isfile(file_name)):
        writeFile(file_name, page)
    else:
        my_file = open(os.getcwd() + "/" + file_name, "r")
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
        if ("pattern" in website):
            checkPattern(website['url'], website['pattern'])
        else:
            checkFileChange(website['url'], website['file'])

if __name__ == "__main__":
    main()
