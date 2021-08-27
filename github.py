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
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78',
         'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
         'origin':'https://github.com',
         'referer':'https://github.com/session'
        }
session.cookies['_device_id']='29b922d78b8501b6ca6606e7e9707efd'
session.cookies['tz']='Asia%2FShanghai'
session.cookies['_octo']='GH1.1.339731349.1630050979'
form=session.get('https://github.com/login',headers=headers).text
form=etree.HTML(form)
authenticity_token=form.xpath('.//input[@name="authenticity_token"]/@value')
timestamp=form.xpath('.//input[@name="timestamp"]/@value')
timestamp_secret=form.xpath('.//input[@name="timestamp_secret"]/@value')
field=form.xpath('.//input[@type="text" and contains(@name,"required")]/@name')
with open(args.data_path, "r+") as f:
    data = f.read()
    data = json.loads(data)
    data["authenticity_token"]=authenticity_token[0]
    data["timestamp"]=timestamp[0]
    data["timestamp_secret"]=timestamp_secret[0]
    data['login']=args.login
    data['password']=args.password
    data[field[0]]=''
print(data)
print(session.post('https://github.com/session',data=data,headers=headers).text)
'''
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
'''
