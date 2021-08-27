import argparse
import requests
import time
import json
from lxml import etree

parser = argparse.ArgumentParser(description='Ustc-course Spyder')
parser.add_argument('data_path', help='path to your own data used for post method', type=str)
parser.add_argument('login', help='email address or github name', type=str)
parser.add_argument('password', help='your password', type=str)
args = parser.parse_args()
name="复变函数"
content=''
session=requests.Session()
form=session.get('https://github.com/login').text
form=etree.HTML(form)
authenticity_token=form.xpath('.//input[@name="authenticity_token"]/@value')
timestamp=form.xpath('.//input[@name="timestamp"]/@value')
timestamp_secret=form.xpath('.//input[@name="timestamp_secret"]/@value')
with open(args.data_path, "r+") as f:
    data = f.read()
    data = json.loads(data)
    data["authenticity_token"]=authenticity_token
    data["timestamp"]=timestamp
    data["timestamp_secret"]=timestamp_secret
    data['login']=args.login
    data['password']=args.password
session.post('https://github.com/session',data=data)
print(session.get('https://github.com').text)
for page in range(0,20):
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=session.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        time.sleep(1)
        text=session.get('https://github.com'+href+'/find/master').text
        html=etree.HTML(text)
        data_url=html.xpath('.//fuzzy-list[@class="js-tree-finder"]/@data-url')
        text=session.get('https://github.com'+data_url[0]).text
        if name in text:
            content+=href+'\n'
print(content)
