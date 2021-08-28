# 介绍
在ustc-course相关的180+个仓库上爬取需要的课程资料，为了提升速度以及避免使用协议带来的困难，项目部署在github action上。  

# 使用说明
## 终端版本
命令行启动：
```shell
python terminal_version.py github用户名 github密码 邮箱地址 ustc邮箱密码
```
这里github的用户名必须为邮箱，否则请自行修改代码  
workflow启动：在Settings/Secrets设置四个Secret：LOGIN、PASSWORD、MAIL、MAILPASSWORD，对应github用户名、github密码、邮箱地址、邮箱密码，然后在Action启动workflow，运行结果可在日志中看到。  
## selenium脚本
编辑代码，将开头用户名、密码信息填写完整，并填上你像搜的课程，运行文件，搜索结果见同目录下的findings.txt。注意两种方式下必须保证脚本和mail.py在同一目录下。
# 优点
可以辅助提升GPA，助你成为卷王  
可以爬取整个目录，而不是view code中显示的一层。
# 常见问题
使用selenium脚本时报错，说find_element_by_xpath('.//pre')未找到相关元素：原因很可能是登录失败，请检查您的用户名和密码  
邮箱验证码获取错误：脚本会不断刷新邮箱，并获取最新一封未读邮件，然后检测该邮件是否包含github验证码。如果之前的验证邮件未读，则可能被程序识别为当前的验证邮件。
邮箱登录超时：重新打卡github，尝试再运行
# 附注
经实验验证，部署在github上的脚本比在本地开vpn（clashX）运行速度快将近三倍，因此推荐使用workflow  
如果不知道如何使用workflow，请参考https://github.com/Kobe972/USTC-ncov-AutoReport ，这个仓库中有使用workflow的详细例子
