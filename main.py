import urllib.request
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import os.path
from os import path
import json


def loadConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

def main():
    a = loadConfig()
    print(a[1])


if __name__ == "__main__":
    main()
