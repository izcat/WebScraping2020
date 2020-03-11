import re
import matplotlib.pyplot as plt

# plt.rcParams两行是用于解决标签不能显示汉字的问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 调用plt画图
def showPLT(x, y, sig='.', xlabel='', ylabel='', title=''):
	"""
	para: x 横坐标list
	para: y 纵坐标list
	para: sig 画线方式 
	para: xlabel, ylabel, title同plt
	"""
	plt.plot(x, y, sig)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	plt.title(title)
	plt.legend()

	plt.show()


新增确诊病例 = []
新增出院病例 = []
新增死亡病例 = []
新增疑似病例 = []
全市核酸检测 = []
发热门诊接诊 = []
现有确诊病例 = []

确诊率 = []
ConfirmedofDistrict = [list() for i in range(13)]
newConfirmedofDistrict = [list() for i in range(13)]

districtRe = '江岸区(\d+)例、江汉区(\d+)例、硚口区(\d+)例、汉阳区(\d+)例、武昌区(\d+)例、青山区(\d+)例、洪山区(\d+)例、东西湖区(\d+)例、蔡甸区(\d+)例、江夏区(\d+)例、黄陂区(\d+)例、新洲区(\d+)例、武汉开发区\(汉南\)(\d+)例'
districtName = ['江岸区', '江汉区', '硚口区', '汉阳区', '武昌区', '青山区', '洪山区', '东西湖区', '蔡甸区', '江夏区', '黄陂区', '新洲区', '武汉开发区(汉南)']
# districtName = ["Jiang'An", 'JiangHan', 'QiaoKou', 'HanYang', 'WuChang', 'QingShan', 'HongShan', 'DongXihu', 'CaiDian', 'JiangXia', 'HuangPi', 'XinZhou', 'HanNan']
days = []

with open('data.txt', 'r', encoding='UTF-8') as f:
	txt = f.read()
	newConfirmed = re.findall('新增确诊病例(\d+)例', txt)
	newCured = re.findall('新增出院病例(\d+)例', txt)
	newDead = re.findall('新增死亡病例(\d+)例', txt)
	newSuspected = re.findall('新增疑似病例(\d+)例', txt)
	inspectPCR = re.findall('全市核酸检测(\d+)', txt)
	feverEveryday = re.findall('发热门诊接诊(\d+)人', txt)
	totalConfirmed = re.findall('现有确诊病例(\d+)', txt)
	days = re.findall('2020年(\d+)月(\d+)日0-24', txt)
	days = list(map(lambda x:x[0]+'.'+x[1], days))
	
	# print(days)
	eachDistrict = re.findall(districtRe, txt)

	全市核酸检测 = list(map(int, inspectPCR))
	发热门诊接诊 = list(map(int, feverEveryday))
	现有确诊病例 = list(map(int, totalConfirmed))

	# print(inspectPCR)
	print(eachDistrict)
	
	for i in range(len(eachDistrict)):
		eachDistrict[i] = list(map(int, eachDistrict[i]))
		item = eachDistrict[i]
		if item[8]<10:
			for j in range(len(item)):
				newConfirmedofDistrict[j].append(item[j])
			continue
		for j in range(len(item)):
			ConfirmedofDistrict[j].append(item[j])

			if len(ConfirmedofDistrict[j])>1:
				newConfirmedofDistrict[j].append(ConfirmedofDistrict[j][-1]-ConfirmedofDistrict[j][-2])
	# print(len(eachDistrict))



	新增确诊病例 = list(map(int, newConfirmed))
	新增出院病例 = list(map(int, newCured))
	新增死亡病例 = list(map(int, newDead))
	新增疑似病例 = list(map(int, newSuspected))
	# print(新增确诊病例)
	# print(新增出院病例)
	# print(新增死亡病例)
	# print(新增疑似病例)
	# print(txt)

	# txt.find('新增确诊病例')
	
	# data = txt.split('\n\n')

	# print(len(data))

	# for i in data:
	# 	print(i, end='\n----\n')






# 现有确诊变化
def showNowLeft():
	print(现有确诊病例)
	for i in 现有确诊病例:
		print(i)
	aaaa = [新增出院病例[i]+新增死亡病例[i] for i in range(len(新增出院病例))]
	print(aaaa)
	print(新增出院病例)
	days = ['2.2'+str(i) for i in range(1,10)]
	for i in range(1, 6):
		days.append('3.'+str(i))
	# days = list(map(float, days))
	plt.plot(days, 现有确诊病例, label='totalConfirmedCases')
	days += ['3.'+str(i) for i in range(3, 20)]
	plt.xticks(days)
	yyy = [i for i in range(0, 40001, 4000)]
	plt.yticks(yyy)
	plt.legend()
	plt.show()

# 确诊率变化
def showConfirmRatio():
	# print(全市核酸检测)

	for i in range(len(全市核酸检测)):
		# 确诊率.append((新增确诊病例[i]) / 全市核酸检测[i]*100)
		确诊率.append((新增确诊病例[i]+新增疑似病例[i]) / 全市核酸检测[i]*100)

	global days
	showPLT(days, 确诊率, xlabel='日期', ylabel='百分比', title='确诊率')
	# print(确诊率)
	
	# global 发热门诊接诊
	# # 发热门诊接诊 = [item/100 for item in 发热门诊接诊]
	# plt.plot(发热门诊接诊)



# 每个区新增情况
def showNewDistrict():
	import matplotlib.pyplot as plt
	# 2.23日开始
	days = ['2.2'+str(i) for i in range(3,10)]
	for i in range(1, len(newConfirmedofDistrict)-2):
		days.append('3.'+str(i))
	# plt.plot(ConfirmedofDistrict)
	for i in range(len(newConfirmedofDistrict)):
		# if i==2 or i==3 or i==4 or i==6:
			# continue
		plt.plot(days, newConfirmedofDistrict[i], label=districtName[i])

	plt.xlabel('日期')
	plt.ylabel('每日新增确诊')
	plt.legend()
	plt.show()

# 每个区新增情况
def showDistrict():
	import matplotlib.pyplot as plt
	# 2.22开始
	days = ['2.2'+str(i) for i in range(2,10)]
	for i in range(1, len(ConfirmedofDistrict)-2):
		days.append('3.'+str(i))
	# plt.plot(ConfirmedofDistrict)
	for i in range(len(ConfirmedofDistrict)):
		# if i==2 or i==3 or i==4 or i==6:
			# continue
		plt.plot(days, ConfirmedofDistrict[i], label=districtName[i])

	plt.xlabel('日期')
	plt.ylabel('每日新增确诊')
	plt.legend()
	plt.show()


# showDistrict()
showConfirmRatio()