import socket
from _thread import *
import threading
from bs4 import BeautifulSoup
import requests
import re
import pickle

def WebCrawl(url):
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')

		# prints any titles from the first page hit.
		title = soup.find_all('title')
		links = soup.find_all('a', attrs={'href': re.compile("^http")})

		tf_results = []
		results = []
		add_list = []
		keyword1='covid-19'
		keyword2='coronavirus'

		for link in links:
			address = link.get('href')
			try:
				new_page = requests.get(address)
				new_soup = BeautifulSoup(new_page.text, 'html.parser')
				title2 = new_soup.find_all('title')
				texts2 = new_soup.find_all('p')
				links2=new_soup.find_all('a', attrs={'href': re.compile("^http")})

				for idx in range(len(texts2)):
					L = texts2[idx].get_text()
					tf_value = (keyword1.lower() in L.lower()) or (keyword2.lower() in L.lower())
					tf_results.append(tf_value)

					if tf_value == True:
						results.append(texts2[idx])
			except Exception as ie:
				pass

			if any(True == s for s in tf_results):
				add_list.append([address,results])

	except Exception as ie:
		pass

	return add_list


print_lock = threading.Lock()

def threaded(c):
	HEADERSIZE = 10
	while True:
		url = c.recv(4096)
		if not url:
			print('Bye')
			print_lock.release()
			break
		my_url=url.decode('utf-8')
		print('the website you are crawling is: ')
		print(my_url)
		url_list= WebCrawl(my_url)
		print('crawled links #. is : ')
		print(len(url_list))
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
