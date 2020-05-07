# mega_client.py is mostly taken from this stack-overflow thread:
#https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
# it is the answer by "Arik" of April 28 2016, about halfway down the page

# this is our "mega-scraper" which uses threading and a thread Queue
# to enable a multi-threaded scrape of multiple servers

from queue import Queue
import threading

# we are basically running this function at the same time, on multiple servers
from .client import GetOutput

# had to call it MegaScrape
def MegaScrape(scrapers):
    message = []
    que = Queue()
    threads = []

    for scraper in scrapers:
        # Call the Client GetOutput method and put it into the threads list
        # trust in the lambda! - note the list of parameters going to GetOutput,
        # each scraper in scrapers runs its own thread, que just sits there collecting it all
        t = threading.Thread(target= lambda q, arg1 : q.put(GetOutput(arg1[0],arg1[1],arg1[2], arg1[3])),
                             args=(que, [scraper.ip_address, scraper.port, scraper.seed, scraper.name]))

        # this starts each threaded function
        t.start()
        threads.append(t)

    # this halts the functions
    for thread in threads:
        thread.join()

    # this uses our message[] to gather the return values from the queue
    while not que.empty():
        message += que.get()

    # we added a sort function just to mix up the display a bit
    message.sort()

    return message
