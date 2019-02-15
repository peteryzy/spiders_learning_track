import os
import re
import time
import lxml
import random
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def parse_a_page(url):
	try:
		html = requests.get(url)
		if html.status_code == 200:
			soup_prettify = BeautifulSoup(html.text,'lxml')
			return soup_prettify.prettify()
	except TimeoutError:
		pass



def write_in_file(page_source):
	pattern = re.compile(r'<a\shref="(https://www.mzitu.com/\d{4,7})".*?</a>',re.S)
	regex = re.findall(pattern,page_source)
	with open('requests_url.txt','w+') as f:
		for i in regex:
			f.writelines(i+"\n")
	return regex

def mkdir(i):
	new_dir = os.mkdir("C://Users/peter/Desktop/a/"+str(i))
	os.chdir(new_dir)
	i+=1

def request_image(i):
	'''
	proxy = {"https": "121.61.1.79:9999",
			 "https": "42.123.125.181:8088",
			 "https": "61.135.155.82:443",
			 "https": "219.134.90.116:42931",
			 "https": "223.241.116.249:8010",
			 "https": "115.151.1.11:808",
			 "https": "61.145.69.27:42380",
			 "https": "115.151.2.239:9999",
			 }
	'''
	user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
		"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"]


	f = open('requests_url.txt','r+')
	read = f.readlines()
	inner_page = requests.get(read[i])
	inner_page_soup = BeautifulSoup(inner_page.text,'lxml')
	max_span = inner_page_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
	for page in range(1,int(max_span)+1):
		page_url = read[i][:-1]+"/"+str(page)

		pic_real = requests.get(page_url)
		pic_real_soup = BeautifulSoup(pic_real.text,'lxml')
		pic_real_address = pic_real_soup.find('div',class_='main-image').find('img')['src']
		UA = random.choice(user_agent_list)  # 获取随机的User_Agent
		headers = {'User_Agent': UA,
				   'Referer': str(pic_real_address)}
		#referer = {'Referer': str(pic_real_address)}
		img_source = requests.get(pic_real_address,headers = headers)
		name = pic_real_address[-7:]
		img = open(name,'ab')
		img.write(img_source.content)
		img.close()

def main(i):
	#time_start = time.time()
	#print(time_start)
	start_url ="https://www.mzitu.com/all"
	page_source = parse_a_page(start_url)
	requests_url = write_in_file(page_source)
	request_image(i)
	#time_end = time.time()
	#print(time_end)
	for i in range(500):
		if (i%10==0):
			print("休息0. 1s")
			time.sleep(0.1)
	print("继续")

if __name__=='__main__':
	pool = Pool()
	pool.map(main,[i for i in range(500)])

	#main()

