# 武汉新冠肺炎疫情信息爬取

身处疫情中心，在家无聊写了个小程序，每天自动抓取[武汉卫健委](http://wjw.wuhan.gov.cn/front/web/list3rd/yes/803)公布的武汉地区的最新具体数据。

获取网站上的公布的数据后，自动转发到我的邮箱。

&nbsp;

## 代码模块

- main.py ：利用`requests_html`库，进行网站爬虫抓取疫情数据的逻辑
- mymail.py：邮箱功能的实现，将邮件从新浪邮箱转发到QQ邮箱
- anslyse.py：分析data.txt内的每日疫情数据，利用`plt`展现每日变化结果

&nbsp;

## 踩坑

- session对象的属性`links` 和 `absolute_links` 返回的是集合set，即使转成list也是无序的

  因此从html源文件中读取到第 k 条新闻title与links[k]并不一一对应

- 解决方法：

  - [x] 使用正规式解析新闻列表元素
  - [ ] 尝试打开所有链接，检查新的页面是否是疫情信息发布页面

- 腾讯云服务器上无法运行以上代码，报错信息：ImportError: cannot import name ‘Coroutine’

  具体在 from typing import Coroutine 原因不明

- 解决方法：

  - [x] 改用requests库
  
    没有了requests_html十分方便的text方法获取元素内容，利用xpath手动解析

&nbsp;

## 结果展示
  邮件列表
![自动接收的邮件列表](https://images.cnblogs.com/cnblogs_com/izcat/1649447/o_200311143517mails.png)



&nbsp;

## 收获

- 能够使用Python编写简单的爬虫程序，抓取想要的信息
- 简单实践了Python发送邮件
- 熟悉了正则表达式的使用，根据需要分离有效数据
- 优化代码过程中，熟悉了map、zip等操作，简短的代码体现出了Python语言的优雅简洁之美

&nbsp;

（完）