# 介绍
在ustc-course相关的180+个仓库上爬取需要的课程资料，为了提升速度以及避免使用协议带来的困难，项目部署在github action上。  
当前遇到的困难：未能破解github的if-none-match反爬虫机制，具体表现为请求data-url后返回为空（headers中没有if-none-match项，不知道怎么得到它的值），欢迎pull request
