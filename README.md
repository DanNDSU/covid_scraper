# python_sockets
A client-server setup for python - will expand to multiple servers eventually
Currently includes a separate web scraper that we'll need to integrate into the server.

# To run the client-server:
In one terminal, cd to the folder and run python socket.py
Then, in another terminal, cd to the folder and run python client.py

Currently, this takes in a string of input in the client, then reverses the string in the server.
Note: the server will not shut down on its own. You'll have to Ctrl + D (in bash terminal) or just close terminal (Windows).

# To run the web scraper:
First, you'll need to install requests and beautiful soup.

I'd recommend doing this by installing Pipenv (as this is currently set up).
To do this, install Pipenv (by running $ pip install pipenv), then run $ pipenv install
To start up a Pipenv environment, run $ pipenv shell
You'll know if your environment is running if "(python_sockets)" appears on the left side of the terminal
To exit your running environment, type exit into the terminal


If you don't want to do pipenv, run:

$ pip install requests
$ pip install beautifulsoup4

Don't forget the "4" at the end of "beautifulsoup"!
