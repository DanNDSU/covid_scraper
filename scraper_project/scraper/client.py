# Runs a single client instance method to get output from the server.
# Base code is from https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

import socket
import pickle

def GetOutput(c_host, c_port, seed_url, c_name):
	# gets the IP address information from the django scraper object
	host = c_host
	# gets the port number from the django scraper object
	port = c_port

	# Our preliminary return list (see the end of the function)
	to_return = []

	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host,port))
		HEADERSIZE = 10

		while True:

			#sends the seed url from the scraper object to the server
			url= seed_url
			s.send(url.encode('utf-8'))

			full_msg=b''
			new_msg=True
			while True:
				try:
					# gets the report sent by the server
					# we have a large buffer size because each scrape uses it only once
					msg=s.recv(32768)

					if new_msg:
						msglen = int(msg[:HEADERSIZE])
						new_msg = False
						full_msg += msg

						# unpacks the message with pickle.loads
						if len(full_msg) - HEADERSIZE == msglen:
							to_return = pickle.loads(full_msg[HEADERSIZE:])

						# creates a "fail" return result
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

	# we added this to collect data in the loop below.
	to_return_new = []

	# appends both the returned website info
	# along with the name of the scraper object
	# also removes any duplicates
	for item in to_return:
		scrape = [item, c_name]
		if scrape not in to_return_new:
			to_return_new.append(scrape)

	return to_return_new
