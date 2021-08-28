# 介绍
在ustc-course相关的180+个仓库上爬取需要的课程资料，为了提升速度以及避免使用协议带来的困难，项目部署在github action上。  
当前遇到的困难：未能破解github的if-none-match反爬虫机制，具体表现为请求data-url后返回为空（headers中没有if-none-match项，不知道怎么得到它的值），欢迎pull request。  
然而，我写了一个selenium版本，经测试有效。
# 使用说明
## 正常版本
命令行启动：
```shell
github.py data.json(表单文件地址) github用户名 github密码 ustc邮箱密码
```
这里github的用户名必须为邮箱，否则请自行修改代码  
workflow启动：在Settings/Secrets设置三个Secret：LOGIN、PASSWORD、MAILPASSWORD，对应用户名、github密码、邮箱密码，然后在Action启动workflow  
## selenium脚本
编辑代码，将开头用户名、密码信息填写完整，并填上你像搜的课程，运行文件，搜索结果见同目录下的findings.txt。注意两种方式下必须保证脚本和mail.py在同一目录下。
