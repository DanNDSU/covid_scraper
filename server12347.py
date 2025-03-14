# Base code is from https://www.geeksforgeeks.org/socket-programming-multi-threading-python/# Base code is from https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Crawl and scrape tutorials and base code:
# https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3


import socket
from _thread import *
import threading
from bs4 import BeautifulSoup
import requests
import re
import pickle
from datetime import datetime, timedelta
import random

def WebCrawl(url):
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')

		# prints any titles from the first page hit.
		titles = soup.find_all('title')
		links = soup.find_all('a', attrs={'href': re.compile("^http")})

		tf_results = []
		url_list = []
		keyword1='covid-19'
		keyword2='coronavirus'

		# This works to place a time-out stop on the server.
		start_time = datetime.now()
		random_number = random.randint(0, 3000)

		for link in links:
			current_time = datetime.now()
			if current_time > start_time + timedelta(milliseconds = 20000 + random_number):
				break

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

					if (keyword1.lower() in L.lower()) or (keyword2.lower() in L.lower()):
						target = L
						url_list.append([address,target])
						break

			except Exception as ie:
				print("Error in crawling web page.")

	except Exception as ie:
		print("Error in crawling web page.")

	return url_list


print_lock = threading.Lock()

def threaded(c):
	HEADERSIZE = 10
	while True:
		try:
			url = c.recv(4096)
			if not url:
				print('Bye')
				print_lock.release()
				break
			my_url=url.decode('utf-8')
			print('the website you are crawling is: ')
			print(my_url)
			url_list = WebCrawl(my_url)
			print('crawled links #. is : ')
			print(len(url_list))
			msg=pickle.dumps(url_list)
			msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
			c.send(msg)
			print('data sent!')
			print(url_list)
		except:
			url_list.clear()
			url_list.append(["No message sent.", "Error sending data."])
			msg=picke.dumps(url_list)
			c.send(msg)
			print("Error in sending data.")
	c.close()

def Main():
	host = ""
	port = 12347
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
