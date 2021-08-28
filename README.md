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
# 优点
可以辅助提升GPA，助你成为卷王  
可以爬取整个目录，而不是view code中显示的一层。正常版本在获取目录树时遇到了反爬虫，目前未能破解。
# 常见问题
使用selenium脚本时报错，说find_element_by_xpath('.//pre')未找到相关元素：原因很可能是登录失败，请检查您的用户名和密码  
邮箱验证码获取错误：脚本会不断刷新邮箱，并获取最新一封未读邮件，然后检测该邮件是否包含github验证码。如果之前的验证邮件未读，则可能被程序识别为当前的验证邮件。
