from multiprocessing import Queue, Process
import Queue as QueueException
import sys
from urlgrabber import urlopen
from MyHTMLParser import MyHTMLParser
import os

r = 1
n = 100
w = 15

if( len(sys.argv) > 1 ):
    r = int(sys.argv[1])

if( len(sys.argv) > 2 ):
    n = int(sys.argv[2])

if( len(sys.argv) > 3 ):
    w = int(sys.argv[3])

ITEM_URL  = 0
ITEM_QUIT = 1

class Item(object):
    def __init__(self, item_type, data):
        self.item_type = item_type
        self.data = data

def f(idx, q,r):
    path = "data%s"%(idx)
    os.makedirs(path)
    while True:
        item = q.get()
        if( item.item_type == ITEM_QUIT ):
            break;

        count = 0
        localQueue = Queue()
        current = item.data
        while True:
            print current
            fo = urlopen(current)
            data = fo.read()
            name = "%s/%s"%(path,count)
            fw = open( name, "w" )
            count = count + 1
            fw.write(data)
            fw.close()
            fo.close()
            p = MyHTMLParser()
            try:
                p.feed(data)
            except:
                pass

            for href in p.hrefs:
                print item.data, ": ", href

            try:
                current = localQueue.get_nowait()
            except:
                break;

def processItem(item):
    pass

def idleProcess():
    pass

url = [
        "http://www.naver.com",
        "http://www.daum.net",
        "http://www.google.com",
        "http://www.yahoo.com"
      ]

if __name__=='__main__':
    print r, n, w
    q = []
    p = []
    retQueue = Queue()

    for i in xrange(r):
        q.append(Queue())
        p.append(Process(target=f, args=(i, q[i],retQueue)))
        item = Item(ITEM_URL, url[i])
        q[i].put(item)
        p[i].start()

    while True:
        try:
            item = retQueue.get(False)
            processItem(item)
        except QueueException.Empty:
            idleProcess()

    for i in xrange(r):
        p[i].join()
