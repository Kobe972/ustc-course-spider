import requests
import time
from lxml import etree
name="复变函数"
content=''
for page in range(0,20):
    time.sleep(5)
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=requests.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        text=requests.get('https://github.com'+href+'/find/master').text
        html=etree.HTML(text)
        data_url=html.xpath('.//fuzzy-list[@class="js-tree-finder"]/@data-url')
        text=requests.get('https://github.com'+data_url).text
        if name in text:
            content+=href+'\n'
print(content)
