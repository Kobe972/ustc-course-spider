# 更新
该版本使用了github的api，相比之前的selenium版本，速度快了十倍左右，而且不需要账号密码及邮箱验证，有效防止了程序的不稳定，新版程序几乎不会无缘无故运行失败（脚本运行过多导致请求超限除外）。
# 介绍
本项目专门为考试周找不到往年试卷的科大学生定制，它可以在ustc-course相关的230+个仓库上高效爬取需要的课程资料，为了提升速度以及避免使用proxy带来的困难，项目部署在github action上。  
# 使用说明
命令行启动：
```shell
python main.py <TOKEN>
```
其中TOKEN是GitHub的token，可以去设置页面生成。  
可以修改源码第3、4行个性化搜索，设置想搜的学科甚至是外校的仓库（如把搜索关键词由'ustc course'改为'pku course'可搜索北大的学习资料，不过一般都不需要）  
workflow启动：  
1、将代码fork到自己的仓库。  
2、点击Actions选项卡，点击`I understand my workflows, go ahead and enable them`。  
3、在Settings/Secrets设置TOKEN。  
![](img/secret.png)
4、在Action选项卡中启动workflow，运行结果可在日志中看到。
![](img/workflow.png)
![](img/log.png)
# 优点
1、可以辅助提升GPA，助你成为卷王。  
2、比起手动寻找仓库，速度要快几十倍，而且支持并行搜索（同时开启几个workflow即可）。  
3、可以快速得到整个目录树，判断是否是需要的仓库。
# 常见问题
1、token认证失败（直接体现是repo不存在'item'项），原因可能是不小心把token明文发布到了仓库上，需要重新生成token。
# 附注
1、脚本也可做其他用途，比如搜其他学校的课程。它的主要功能是在一堆仓库中找出包含某类文件的仓库（比如文件名含有某些字符串）。  
2、熟悉正则表达式的可以改成更强大的正则表达式搜索。

# Stargazers over time
[![Stargazers over time](https://starchart.cc/Kobe972/ustc-course-spider.svg)](https://starchart.cc/Kobe972/ustc-course-spider)
