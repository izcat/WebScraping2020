import requests
import datetime
import time
import re
from lxml import etree
from mymail import myMail


# 获取昨日数据链接
def getURL(date):
	"""
	获取日期为date的武汉疫情信息所在网页URL
	网站未更新时返回None
	para: datetime.date
	return: str / None
	"""
	url = 'http://wjw.wuhan.gov.cn/front/web/list3rd/yes/803'
	# 必须要定制HTTP请求头
	headers = {'user-agent': 'my-app/0.0.1'}
	r = requests.get(url, headers=headers)
	html = r.text

	# 正则表达式 匹配新闻列表
	matchRe = '<a href="(http://[^\s]+)" title="(.*)">' 
	allnews = re.findall(matchRe, html)

	for url, title in allnews:
		title = title.strip()
		if title.startswith('武汉市新冠肺炎疫情动态（2020年%d月%d日）' % (date.month, date.day)):
			return url

	return None

# 获取疫情页面的文本
def getMsgText(url):
	# url = 'http://wjw.wuhan.gov.cn:80/front/web/showDetail/2020031110061'
	headers = {'user-agent': 'my-app/0.0.1'}
	r = requests.get(url, headers=headers)
	
	html = r.content
	html = etree.HTML(html)

	# result = html.xpath('//div[@id="detailContent"]/div[@class="TRS_Editor"]//span')
	# result = html.xpath('//div/div/p/span')
	# news = list(map(lambda x:str(x.text), result))
	# news = ''.join(news)
	# print(news)
	
	# 分段读取新闻
	result = html.xpath('//div[@id="detailContent"]/div[@class="TRS_Editor"]/p')
	news = ''
	for p in result:
		para = ''
		for span in p.getchildren():
			if span.text==None:
				continue
			try:
				para += span.text
			except Exception as e:
				print(e)
			# print(span.text)
		# print(para)
		news += para+'\n'
	news = news.strip('\n')
	# print(news)
	return news


# 获取昨日数据链接
def everydayRun(yesterday):
	print('entering everydayRun')

	isUpdated = False
	while not isUpdated:
		url = getURL(yesterday)
		if url==None:
			# 每半小时检查一次
			print('waiting for 30 min')
			time.sleep(1800)
			continue

		isUpdated = True
		msgText = getMsgText(url)

		print('sending email')
		email = myMail()
		email.Send('zongeek@sina.com', 'zongyc@foxmail.com', '42ebf40ceee2567a',
					msgText, '昨日武汉疫情')



lastDay = datetime.date.today() + datetime.timedelta(days=-1)
# 每日运行检测网站是否更新
def autoRun():
	while True:
		today = datetime.date.today()
		global lastDay

		# 没有到新的一天
		if today.day==lastDay.day:
			print('waiting for 5 hours')
			time.sleep(5*3600)
			continue

		# 新的一天开始了
		if datetime.datetime.now().hour<9:
			print('waiting until 9:00')
			time.sleep((9-datetime.datetime.now().hour)*3600)
			continue

		# 新的一天9点过后 准备检查网站
		lastDay = today
		everydayRun(today+datetime.timedelta(days=-1))
		
if __name__=='__main__':
	autoRun()
