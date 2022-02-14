import requests
import argparse
keys=['算法','algorithm'] #这里放文件名中要有的关键字
search='ustc course' #这里放搜索关键字
parser = argparse.ArgumentParser(description='Ustc-course Spyder')
parser.add_argument('token', help='token for your github account', type=str)
args = parser.parse_args()
token=args.token
headers={"Authorization":"token "+token}
search=search.replace(' ','+')
url_list=[]
for page in range(1,11):
    repo=requests.get("https://api.github.com/search/repositories?q="+search+"&per_page=100&page="+str(page),headers=headers).json()
    if(len(repo['items'])==0):
        break
    for item in repo['items']:
        full_name=item['full_name']
        branch=item['default_branch']
        tree_url='https://api.github.com/repos/'+full_name+'/git/trees/'+branch+'?recursive=1'
        content=requests.get(tree_url,headers=headers)
        if 'tree' not in content.json().keys():
            continue
        files=full_name.lower()
        for file in content.json()["tree"]:
            files+=file['path'].lower()
        for key in keys:
            if key in files:
                url_list.append('https://github.com/'+full_name)
for url in url_list:
    print(url)
