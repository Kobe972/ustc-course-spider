import requests
token="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"
keys=['运筹学']
search='ustc course'
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
        files=''
        for file in content.json()["tree"]:
            files+=file['path']
        for key in keys:
            if key in files:
                url_list.append('https://github.com/'+full_name)
for url in url_list:
    print(url)
