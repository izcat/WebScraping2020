from requests_html import HTMLSession
import requests
import datetime
import time
import re
from mymail import myMail


# 获取昨日数据链接
def getURL(date):
	"""
	获取日期为date的武汉疫情信息所在网页URL
	网站未更新时返回None
	para: datetime.date
	return: str / None
	"""
	matchRe = '<a href="(http://[^\s]+)" title="(.*)">' 
	url = 'http://wjw.wuhan.gov.cn/front/web/list3rd/yes/803'
	# 必须要定制HTTP请求头
	headers = {'user-agent': 'my-app/0.0.1'}
	r = requests.get(url, headers=headers)
	html = r.text

	allnews = re.findall(matchRe, html)

	for url, title in allnews:
		if title.startswith('武汉市新冠肺炎疫情动态（2020年%d月%d日）' % (date.month, date.day)):
			return url

	return None

def everydayRun():
	print('entering everydayRun')
	today = datetime.date.today()
	yesterday = today + datetime.timedelta(days=-1)

	isUpdated = False
	while not isUpdated:
		url = getURL(yesterday)
		if url==None:
			# 每半小时检查一次
			print('waiting for 30 min')
			time.sleep(1800)
			continue

		isUpdated = True
		session = HTMLSession()
		r = session.get(url)	
		elements = r.html.find('div#detailContent')

		# print(elements[0].text)
		print('sending email')
		email = myMail()
		email.Send('zongeek@sina.com', 'zongyc@foxmail.com,2075733309@qq.com', '42ebf40ceee2567a',
					elements[0].text, '昨日武汉疫情')



lastDay = datetime.date.today() + datetime.timedelta(days=-1)
# 获取昨日数据链接
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
		everydayRun()
		

autoRun()