from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm
from lxml import etree
import time
from mail import Email #如果不用科大邮箱，mail.py取最新一封邮件的代码可能也要改。科大邮箱默认最新未读邮件索引是1

GitAccount=input('请输入GitHub用户名：') #github账户
GitPasswd=input('请输入GitHub密码：') #github密码
EmailAccount=input('请输入GitHub绑定的邮箱用户名（不含@mail.ustc.edu.cn），输入前请确保最新未读邮件不是GitHub验证码。如果不是科大邮箱需要重新绑定或重新申请账号：')+'@mail.ustc.edu.cn' #邮箱账户，如果Chrome登录github不需要验证则可以放空
EmailPasswd=input('请输入邮箱密码：') #邮箱密码
names=[] #匹配条件，即合格的文件名必须至少包含列表中的一个字符串，这是为了防止中英文、习惯用语等导致的不匹配
tmp=input('输入文件名中要包含的字符串，输完一个字符串按回车输另一个，按两次回车结束输入。比如搜数据结构相关资料，\
则应输入“数据结构”、回车、“Structure”、回车、回车：')
while tmp!='':
    names.append(tmp)
    tmp=input()
search=input('输入搜索关键字，推荐“ustc course”：')
search=search.replace(' ','+') #转换成url要求的格式
req_timeout=20
content=''

option = webdriver.ChromeOptions()
option.add_argument('headless')# 添加无头模式
option.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=option)
driver.implicitly_wait(req_timeout)

driver.get('https://github.com')
if 'Where' in driver.title:
    driver.get('https://github.com/login')
    driver.find_element_by_name("login").send_keys(GitAccount)
    driver.find_element_by_name("password").send_keys(GitPasswd)
    driver.find_element_by_name("commit").click()
    if 'Where' in driver.title: #如果需要邮箱验证。一般不需要
        pop3_server = "mail.ustc.edu.cn" #如果不用科大邮箱，这里要改
        time.sleep(3)
        LT=None
        while LT==None:
            LT=Email(EmailAccount,EmailPasswd,pop3_server).get_LT()
        driver.find_element_by_name("otp").send_keys(LT)
        time.sleep(1)

#搜索仓库
for page in tqdm(range(0,20),ncols=70,leave=False):
    url='https://github.com/search?p='+str(page+1)+'&q='+search+'&type=Repositories'
    driver.get(url)
    text=driver.page_source
    html=etree.HTML(text)
    repo=html.xpath('.//a[@class="v-align-middle"]/@href')
    for href in tqdm(repo,ncols=70,leave=False):
        driver.get('https://github.com'+href)
        text=driver.page_source
        html=etree.HTML(text)
        branch=html.xpath('.//span[@class="css-truncate-target"]/text()')
        if(len(branch)==0): #空仓库没有branch
            continue
        driver.get('https://github.com'+href+'/find/'+branch[0])
        text=driver.page_source
        html=etree.HTML(text)
        data_url=html.xpath('.//fuzzy-list[@class="js-tree-finder"]/@data-url') #获取完整文件列表
        driver.get('https://github.com'+data_url[0]) #获取所有目录
        text=driver.find_element_by_xpath('.//pre').text
        text=text.lower()
        for name in names:
            if name in text:
                with open('findings.txt','a') as fd:
                    fd.write('https://github.com'+href+'\n')
                break
print('在目录下的findings.txt查找搜索结果')
driver.close()
