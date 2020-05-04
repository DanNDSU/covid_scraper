import socket
import pickle
#from urllib.parse import urlparse
#import requests

def GetOutput(c_host, c_port, seed_url, c_name):
	# local host IP '127.0.0.1'
	host = c_host
	# Define the port on which you want to connect
	port = c_port
	to_return = []
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host,port))
		HEADERSIZE = 10
		while True:
			url= seed_url
			s.send(url.encode('utf-8'))

			full_msg=b''
			new_msg=True
			while True:
				try:
					msg=s.recv(32768)
					if new_msg:
						#print("new msg len:", msg[:HEADERSIZE])
						msglen = int(msg[:HEADERSIZE])
						new_msg = False
						#print(f"full message length: {msglen}")
						full_msg += msg
						if len(full_msg) - HEADERSIZE == msglen:
							to_return = pickle.loads(full_msg[HEADERSIZE:])
						else:
							to_return.append(["Scrape unsuccessful.", "Something went wrong."])
					break
				except:
					to_return.append(["Scrape unsuccessful.", "Try again later."])
					break
			break
		s.close()

	except:
		to_return.append(["Scrape unsuccessful.", "Try again later."])

	to_return_new = []

	for item in to_return:
		to_return_new.append([item, c_name])

	return to_return_new
