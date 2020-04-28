from queue import Queue
import threading
from .client import GetOutput

def MegaScrape(scrapers):
    message = []
    que = Queue()
    threads = []

    for scraper in scrapers:
        #Call the Client GetOutput method and put it into threads.
        t = threading.Thread(target= lambda q, arg1 : q.put(GetOutput(arg1[0],arg1[1],arg1[2], arg1[3])),
                             args=(que, [scraper.ip_address, scraper.port, scraper.seed, scraper.name]))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    while not que.empty():
        message += que.get()

    message.sort()

    return message
