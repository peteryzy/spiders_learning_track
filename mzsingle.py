import requests
from bs4 import BeautifulSoup

def get_a_page(url,headers):
	html=requests.get(url,headers = headers)
	html.encoding="utf8"
	soup=BeautifulSoup(html.text,'lxml')
	return soup

def wash(html):
	all_a = html.find('div', class_='all').find_all('a') ##意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
	all_a.pop(0)
	for a in all_a:
		#title=a.get_text()
		href=a["href"]
		pic=requests.get(href)
		html_Soup = BeautifulSoup(pic.text, 'lxml')
		max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
		#print(max_span)
		for page in range(1, int(max_span)+1):
			page_url = href + '/' + str(page)
			#print(page_url)
			pic_real=requests.get(page_url)
			pic_real_soup=BeautifulSoup(pic_real.text,'lxml')
			pic_real_address=pic_real_soup.find('div',class_='main-image').find('img')['src']
			print(pic_real_address)
			
			name=pic_real_address[-9:-4]
			referer = {'Referer':str(pic_real_address)}
			img=requests.get(pic_real_address,headers = referer)
			f=open(name+'.jpg','ab')
			f.write(img.content)
			f.close()
        	
		#print(href)
		#print(href)

if __name__=="__main__":
	url="http://www.mzitu.com/all"
	headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
	html=get_a_page(url,headers)
	wash(html)
	