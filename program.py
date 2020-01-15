import requests
import os
import time
from bs4 import BeautifulSoup

headers1={
'authority': '4.bp.blogspot.com'
,'method': 'GET'
,'path': '/-T-9CDqQRjsE/W1H2rxTSPHI/AAAAAAAKghE/i5PiIAFLt4o6KvwZy2DZYoagYK81DMiDgCLcBGAs/s1600/nioi001_022_MRM.jpg'
,'scheme': 'https'
,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
,'accept-encoding': 'gzip, deflate, br'
,'accept-language': 'zh-CN,zh;q=0.9'
,'cache-control': 'max-age=0'
,'if-none-match': "va8229"
,'referer': 'https://myreadingmanga.info/ura-urethan-akari-seisuke-tooi-nioi-onmyou-taisenki-dj-jp/'
,'upgrade-insecure-requests': '1'
,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
headers2={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

def try_get(url,header,_time):
	try:
		response=requests.get(url,headers=header,timeout=_time)
		if response.status_code == 200:
			return response
	except:
		return None


def requests_get(url,header,_time):
	time.sleep(1)
	for i in range (1,11):
		print('trying',i)
		response=try_get(url,header,_time)
		if (response == None): continue
		return response
	print('get url fail')


def creat_soup(str):
	return BeautifulSoup(requests_get(str,headers2,10).text,'html.parser')

def download(url,name):
	web=requests_get(url,headers2,10)
	with open(name,'wb') as file:
		file.write(web.content)

def search_class(tag,list):
	if tag.get('class') != None:
		if tag.get('class') == list:
			return 1;
	return 0;

def trans_name(num):
	if num<10: return '00'+str(num)
	if num<100: return '0'+str(num)
	return str(num)

abp=os.path.abspath
joi=os.path.join

def get_res(url,web_head,dir_name,startp):
#	url='https://www.yaoihavenreborn.com/doujinshi/cub-doujinshi'
#	web_head='https://www.yaoihavenreborn.com'
	web=creat_soup(url) 
	countp=1
	for tag in web.find_all('h5'):
		if(countp<startp):
			countp += 1;
			dir_name +=1
			continue;

		sec_url = web_head + tag.parent.get('href')
		print(sec_url)
		sec_web = creat_soup(sec_url)
		comic_name = sec_url.rpartition('/')[-1]
		download_path = abp(trans_name(dir_name)+'-'+comic_name)

		try: os.mkdir(download_path);
		except: pass

		page_count = 1; first_page = 0;

		print('downloading',dir_name,comic_name)

		for tag in sec_web.find_all('img'):
			if first_page == 0:
				if search_class(tag,['img-fluid']):
					img_url = web_head + tag.get('src')
					img_path = joi(download_path,trans_name(page_count)+'.jpg')
					img_path2 = abp(trans_name(dir_name)+'.jpg')

					download(img_url,img_path)
					download(img_url,img_path2)

					page_count += 1
					first_page = 1
			else:
				if search_class(tag,['img-fluid','lazy']):
					img_url = web_head + tag.get('data-src')
					img_path = joi(download_path,trans_name(page_count)+'.jpg')

					download(img_url,img_path)

					print('page',page_count,'finish.')
					page_count += 1;

		print('comic',dir_name,'finish.')
		dir_name += 1;



url = 'https://www.yaoihavenreborn.com/doujinshi/cub-doujinshi?page='
page_num = 3
web_head = 'https://www.yaoihavenreborn.com'
#get_res(url+'3',web_head,101,15)
get_res(url+'4',web_head,151,25)
				
'''
url='https://www.yaoihavenreborn.com/doujinshi/tight-coupling'
web = creat_soup(url)
print(web.title.contents)
'''