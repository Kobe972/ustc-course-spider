import argparse
import requests
import time
import json
from lxml import etree
from mail import Email

parser = argparse.ArgumentParser(description='Ustc-course Spyder')
parser.add_argument('data_path', help='path to your own data used for post method', type=str)
parser.add_argument('login', help='email address or github name', type=str)
parser.add_argument('password', help='your password of GitHub', type=str)
parser.add_argument('mailpassword', help='your password of your USTC email', type=str)
args = parser.parse_args()
name="复变函数"
content=''
session=requests.Session()
form=session.get('https://github.com/login').text
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
text=session.post('https://github.com/session',data=data).text
if 'Device verification code' in text:
    text=etree.HTML(text)
    authenticity_token=text.xpath('.//input[@name="authenticity_token"]/@value')
    email = args.login
    password = args.mailpassword
    pop3_server = "mail.ustc.edu.cn"
    LT=None
    while LT==None:
        LT=Email(email,password,pop3_server).get_LT()
    data={'authenticity_token':authenticity_token[0],
          'otp':LT}
    session.post('https://github.com/sessions/verified-device',data=data)
for page in range(0,20):
    time.sleep(5)
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=session.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        time.sleep(1)
        print(href)
        text=session.get('https://github.com'+href+'/find/master').text
        html=etree.HTML(text)
        data_url=html.xpath('.//fuzzy-list[@class="js-tree-finder"]/@data-url')
        if(len(data_url)==0):
            print(content)
        text=session.get('https://github.com'+data_url[0]).text
        if name in text:
            content+=href+'\n'
print(content)
