import sys
import requests
import os.path
from os import path
import json

def loadConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

def sendNotification(url):
    print("CHANGE IN URL:  %s" % (url))
    #file = "sound.mp3"
    #os.system("afplay " + file)


def writeFile(fileName, text):
    f = open(fileName, "w")
    f.write(text)
    f.close()

def checkPattern(url, pattern):
    req = requests.get(url)
    page = req.text
    #writeFile("test.html", page)
    if (page.find(pattern) < 0):
        sendNotification(url)
    else:
        print("Pattern found")

def checkFileChange(url, file_name):
    req = requests.get(url)
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
        if ("pattern" in website):
            checkPattern(website['url'], website['pattern'])
        else:
            checkFileChange(website['url'], website['file'])

if __name__ == "__main__":
    main()
