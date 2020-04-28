import socket
from _thread import *
import threading
from bs4 import BeautifulSoup
import requests
import re
import pickle

import sys
sys.setrecursionlimit(10 ** 8)

def WebCrawl(url):
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		#title = soup.find_all('title')
		links = soup.find_all('a', attrs={'href': re.compile("^http")})

		tf_results = []
		url_list = []
		target=[]
		keyword1='covid-19'
		keyword2='coronavirus'
		for link in links:
			address = link.get('href')
			try:
				# get texts of address to decide whether this address is about covid - 19
				page2 = requests.get(address)
				soup2 = BeautifulSoup(page2.text, 'html.parser')
				#title2 = soup2.find_all('title')
				#links2=soup2.find_all('a', attrs={'href': re.compile("^http")})
				texts2 = soup2.find_all('p')
                # loop through texts
				for idx in range(len(texts2)):
					L = texts2[idx].get_text()
					tf_value = (keyword1.lower() in L.lower()) or (keyword2.lower() in L.lower())
					tf_results.append(tf_value)
					if tf_value == True:
						target.append(L)
			except Exception as ie:
				pass

			if any(True == s for s in tf_results):
				url_list.append([address,target])

	except Exception as ie:
		pass

	return url_list


print_lock = threading.Lock()

def threaded(c):
	HEADERSIZE = 100
	while True:
		url = c.recv(40960)
		if not url:
			print('Bye')
			print_lock.release()
			break
		my_url=url.decode('utf-8')
		print('the website you are crawling is: ', my_url)
		url_list= WebCrawl(my_url)
		print('crawled links #. is : ', len(url_list))

		msg=pickle.dumps(url_list)
		msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
		c.send(msg)
		print('data sent!')
	c.close()

def Main():
	host = ""
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)
	s.listen(5)
	print("socket is listening")
	while True:
		c, addr = s.accept()
		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])
		start_new_thread(threaded, (c,))
	s.close()

if __name__ == '__main__':
	Main()
