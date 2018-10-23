# 获取斗图网的表情
# 使用进程池
import requests
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}

# 日常加请求 agent

def urllist():
	# 构造url列表
	urlist = []
	url0 = 'http://www.doutula.com/photo/list/?page='
	for i in range(1, 10):  # [1, 1960]
		urlist.append(url0 + str(i))
	return urlist

def getpagecontent(url):
	pic_name = []
	pic_src = []
	ht = requests.get(url, headers=head)
	ht.encoding = 'utf-8'
	hts = BeautifulSoup(ht.text, 'lxml')
	# 用 lxml 来解析，据说会快些
	a_tag = hts.find_all('a', attrs={'class': "col-xs-6 col-sm-3"})
	for tag in a_tag:
		# 有些a标签里只有一个 img 标签，所以采用正则来找图片链接和名称
		tagstr = str(tag)
		pic_name.append(re.compile('alt="(.*?)"').findall(tagstr)[0])
		pic_src.append(re.compile('data-original="(.*?)"').findall(tagstr)[0])
	return [pic_name, pic_src]

def write(link):
	# 把每页的图片下载
	for item in range(len(link[0])):
		picname = 'C:\\Users\\qiuchun' \
				  'liu\\Desktop\\doutu' \
				  'pic\\' + link[0][item].replace('?', '') + '.' + link[1][item].split('.')[-1].rstrip('!dta')
		# 创建图片名称，注意后面去掉名称里不合法的字符，比如 ？
		piclink = link[1][item]
		# 找图片链接
		with open(picname, 'wb') as pic:
			pic.write(requests.get(piclink).content)
			# 用 requests 方法来下载文件，urllib 不可用，不知为什么
		print('\r进度: {:.2f}%'.format(item * 100 / len(link[0])), end='')
		# 显示本页下载的进度

def main(url):
	linklis = getpagecontent(url)
	write(linklis)

if __name__ == '__main__':
	starttime = time.time()
	pool = Pool()
	pool.map(main, [it for it in urllist()])
	endtime = time.time()
	totaltime = endtime - starttime
	print('\n', totaltime)
