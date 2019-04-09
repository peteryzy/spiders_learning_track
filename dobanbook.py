import requests
import re
import os
import time
import random


class DobanBook:
	def __init__(self):
		self.url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
		 	AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36'}
		self.url_2 = 'https://book.douban.com'
		self.list_tags = []
		self.ip = ['116.209.52.224','110.73.1.183']
	

	def crawl_page(self):
		html = requests.get(self.url,headers = self.headers)
		return html.text


	def select_tag(self):
		pattern = re.compile(r'<td><a href="(.*?)>.*?</td>',re.S)
		tags = re.findall(pattern,self.crawl_page())
		for i in tags:
			a =i.strip('"')
			self.list_tags.append(a)
		return self.list_tags


	def save_url_to_file(self):
		if os.path.exists('url.txt'):
			print("文件已存在！")
		with open ('url.txt','w+') as file:
			for item in self.select_tag():
				file.write(self.url_2+item+'\n')


	def request_inner_page(self):
		title_pattern = re.compile(r'<a href="https://book.douban.com/subject/.*? title="(.*?)".*?>.*?</a>.*?\
			<span class="rating_nums">(.*?)</span>.*?<span class="pl">'
								   r'(.*?)</span>',re.S)
		try:
			if os.path.exists('url.txt'):
				i = 0
				with open('url.txt','r+') as file:
					for url in file.readlines():
						url_2 = url.strip('\n') + '?start=%d&type=T' % (i)
						print(url_2)
						while True:
							text = requests.get(url_2,proxies = {'http':random.choice(self.ip)},headers = self.headers).text
							print(url.strip('https://book.douban.com/tag/?start=%d&type=T' %(i)))
							titles = re.findall(title_pattern,text)
							#print(text)
							for title in titles:
								yield {
									'title':title[0],
									'point':title[1],
									'comment':title[2].strip()
								}
							i += 20
							time.sleep(5)
						
						
						
		except:
			print("文件不存在！")

	
	def main(self):
		for title in self.request_inner_page():
			print(title)


if __name__ == '__main__':
	f = DobanBook()
	f.main()

	
