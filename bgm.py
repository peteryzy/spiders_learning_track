import requests
import re
from bs4 import BeautifulSoup
import os
import lxml
from lxml import etree
import pandas as pd 

def crawl_page(url,headers):
	html = requests.get(url,headers = headers)
	return html.text

def regex(text):
	pattern = re.compile(r'<div\sclass="inner".*?<h3>.*?<a\shref="(.*?)".*?</a>.*?</h3>.*?</div>',re.S)
	regex = re.findall(pattern,text)
	return regex

def request_inner_page(real_url_list,headers):
	for real_url in real_url_list:
		html = requests.get(real_url,headers = headers)
		html.encoding ="utf8"
		inner_page_text = html.text
		pattern_2 = re.compile(r'<h1\sclass="nameSingle".*?<a.*?title="(.*?)".*?>(.*?)</a>.*?</h1>.*?'
							   r'<div\sclass="global_score".*?<span.*?>(.*?)</span>.*?</div>.*?'
							   r'<div\sclass="chart_desc".*?<span.*?>(.*?)</span>.*?</div>',re.S)
		regex = re.findall(pattern_2,inner_page_text)

		for item in regex:
			'''
			yield {
				'中文名':item[0],
				'原名':item[1],
				'评分':item[2],
				'评分人数':item[3],
				#'话数':item[4]
			}
			'''

			list = [item[0],item[1],item[2],item[3]]
			rep = [' ' if x == '' in list else x for x in list]
		#print(rep)
			d = {
					'中文名':item[0],
					'原名':item[1],
					'评分':item[2],
					'评分人数':item[3]
				#'话数':item[4]
				}
			print(d)
			df = pd.DataFrame(data=d)
			print(df)
				# '话数':item[4]





		#print(regex)




def main():
	headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	real_url = []
	for i in range(1,2):
		url = "http://bgm.tv/anime/browser?sort=rank&page="+str(i)
		text = crawl_page(url,headers)
		#regex = regex(text)
		url = regex(text)
		for link in url:
			real_url.append("http://bgm.tv"+link)
	real_url_list = real_url
	#request_inner_page(real_url_list,headers)
	#for item in request_inner_page(real_url_list,headers):
	#	print(item)
	request_inner_page(real_url_list,headers)
	#request_inner_page(real_url_list,headers)


if __name__=='__main__':
	main()
