from requests_html import HTMLSession
import datetime
import time
import re
from mymail import myMail


# 获取昨日数据链接
def getURL(yesterday):
	print('entering getURL')
	url = "http://wjw.wuhan.gov.cn/front/web/list3rd/yes/803"
	session = HTMLSession()
	r = session.get(url)
	elements = r.html.find('div.xxgksublist')

	# 原始HTML格式
	html = str(elements[0].html)
	lines = html.split('</a>')

	for line in lines:
		titles = re.findall('武汉市新冠肺炎疫情动态（2020年%d月%d日）' % (yesterday.month, yesterday.day), line)
		if len(titles)==0 :
			continue

		# print(titles)
		url = 'http://wjw.wuhan.gov.cn:80/front/web/showDetail/'
		res = re.findall(url+'(\d+)', line)
		# print(url+res[0])

		return url+res[0]
	return None

# print(getURL())

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