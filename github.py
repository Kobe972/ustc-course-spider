import argparse
import requests
import time
import os
import json
from lxml import etree
from mail import Email #如果不用科大邮箱，mail.py取最新一封邮件的代码可能也要改。科大邮箱默认最新未读邮件索引是1

parser = argparse.ArgumentParser(description='Ustc-course Spyder')
parser.add_argument('data_path', help='path to your own data used for post method', type=str)
parser.add_argument('login', help='email address or github name', type=str)
parser.add_argument('password', help='your password of GitHub', type=str)
parser.add_argument('mailpassword', help='your password of your USTC email', type=str)
args = parser.parse_args()
name="数据结构"
content=''
progress=0
flag=0
session=requests.Session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

#登录github
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

def check(path,sub_tree,name):
    if name in path:
        return True
    path_tree = os.listdir(path)     #获取当前目录下的文件和目录

    for item in path_tree:
        if name in item:
            return True
        subtree= path+'\\'+item
            if os.path.isdir(subtree):      #判断是否为目录
                return dir_tree(subtree,sub_tree+1)   #递归深度优先遍历
            else:
                return False

#输入邮箱验证码
if 'Device verification code' in text:
    text=etree.HTML(text)
    authenticity_token=text.xpath('.//input[@name="authenticity_token"]/@value')
    email = args.login
    password = args.mailpassword
    pop3_server = "mail.ustc.edu.cn" #如果不用科大邮箱，这里要改
    LT=None
    while LT==None:
        LT=Email(email,password,pop3_server).get_LT()
    data={'authenticity_token':authenticity_token[0],
          'otp':LT}
    session.post('https://github.com/sessions/verified-device',data=data)
    
#搜索仓库
for page in range(0,20):
    url='https://github.com/search?p='+str(page+1)+'&q=ustc+course&type=Repositories'
    text=session.get(url).text
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in repo:
        text=session.get('https://github.com'+href).text
        os.system('git clone '+'https://github.com'+href+'.git --bare')
        if check('.'+href):
            content+=href+'\n'
        os.system('rm -rf .'+href)
        '''
        html=etree.HTML(text)
        branch=html.xpath('.//span[@class="css-truncate-target"]/text()')
        if(len(branch)==0): #空仓库没有branch
            print('An error occurred in',href,',maybe it is an empty repository.')
            progress+=1
            continue
        text=session.get('https://github.com'+href+'/find/'+branch[0]).text
        html=etree.HTML(text)
        data_url=html.xpath('.//fuzzy-list[@class="js-tree-finder"]/@data-url') #获取完整文件列表
        if(len(data_url)==0):
            print('Error!')
            print('The spyder has explored',progress,'repositories.')
            print('Useful repositories:')
            print(content)
        text=session.get('https://github.com'+data_url[0],headers=headers).text
        if flag==0:
            print('data-url:',data_url[0])
            print('json:',text)
            flag=1
        if name in text:
            content+=href+'\n'
        progress+=1
        '''
print(content)
