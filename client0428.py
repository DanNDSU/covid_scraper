import socket
import pickle
#from urllib.parse import urlparse
#import requests

def loadresources():
	links = []
	with open('resources.txt') as f:
		for line in f:
			inner_list = [elt.strip() for elt in line.split(',')]
			#only grab the item before the ','
			links.append(inner_list)
	return links


def Main():
	# local host IP '127.0.0.1'
	host = '127.0.0.1'
	# Define the port on which you want to connect
	port = 12345
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	HEADERSIZE = 100
	while True:
		urls=loadresources()
		print('Available web urls are: ')
		for i in range(len(urls)):
			print(urls[i])
		idx = int(input("Enter index of url you want to crawl with idx[0,1,2,3,..]: "))
		url=urls[idx][1]
		s.send(url.encode('utf-8'))
		print('crawling.....')

		full_msg=b''
		new_msg=True
		while True:
			msg=s.recv(40960)
			if new_msg:
				print("new msg len:", msg[:HEADERSIZE])
				msglen = int(msg[:HEADERSIZE])
				new_msg = False
			print(f"full message length: {msglen}")

			full_msg += msg
			if len(full_msg) - HEADERSIZE == msglen:
				print("all the crawled url resources: ")
				final_dic = pickle.loads(full_msg[HEADERSIZE:])
				print('Total # is: ', len(final_dic))
				for item in final_dic:
					print(item)

				break

		# ask the client whether he wants to continue
		ans = input('\nDo you want to continue(y/n) :')
		if ans == 'y':
			continue
		else:
			break
	s.close()

if __name__ == '__main__':
	Main()
