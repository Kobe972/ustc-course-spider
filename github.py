import requests
import time
from lxml import etree
name="复变函数"
content=''
for page in range(0,9):
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=requests.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        text=requests.get('https://github.com'+href).text
        if name in text:
            content+=href+'\n'
print(content)
time.sleep(300)
content=''
for page in range(9,18):
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=requests.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        text=requests.get('https://github.com'+href).text
        if name in text:
            content+=href+'\n'
print(content)
time.sleep(300)
content=''
for page in range(18,20):
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=requests.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        text=requests.get('https://github.com'+href).text
        if name in text:
            content+=href+'\n'
print(content)
