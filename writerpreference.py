import threading
import time

wmutex = threading.Semaphore()
rmutex = threading.Semaphore()
readTry = threading.Semaphore()
lock = threading.Semaphore()
readcount = 0
val = 0
writecount = 0
thread_read = []
thread_read_over = []
thread_write = []
thread_write_over = []
def read(i):
    #for j in range(0,6):
    global readcount
    global val
    global thread_read
    global thread_read_over
    
    for j in thread_read:
        if j.name != threading.currentThread().name and j.name not in thread_read_over :
            print(j.name, "in waiting queue")
    readTry.acquire()
    rmutex.acquire()
    print(threading.currentThread().name,"Breaks the Wait Barrier") 
    readcount  = readcount + 1
    if readcount==1:
        print("Writers have to wait")
        lock.acquire()
    rmutex.release()
    readTry.release()
    ##    Critical Section Starts
    
    thread_read_over.append(threading.currentThread().name)

    print(threading.currentThread().name,"in the reading critical section")
    print(threading.currentThread().name,"reading the val=",val)
    
    time.sleep(1)
    print(threading.currentThread().name,"exits")
    ## Critical Section Ends
    
    rmutex.acquire()
    readcount = readcount - 1
    if readcount ==0:
        lock.release()
        print("Now writers can write")
    rmutex.release()    
        
def write(i):
    #for j in range(0,6):
    global val
    global writecount
    global thread_write
    global thread_write_over
    wmutex.acquire()
    print(threading.currentThread().name,"Breaks the Wait Barrier") 
    writecount = writecount + 1
    if writecount == 1:
        readTry.acquire()
        print("Readers have to wait")
    wmutex.release()
    
    lock.acquire()
    #Critical Section Starts    
    val = val + 1
    for j in thread_write:
        if j.name != threading.currentThread().name and j.name not in thread_write_over :
            print(j.name, "in waiting queue")
    thread_write_over.append(threading.currentThread().name)
    print(threading.currentThread().name,"in the writing critical section")
    print(threading.currentThread().name,"writing the value",val)
    
    
    time.sleep(1)
    print(threading.currentThread().name,"exits")
    #Critical Section Ends
    print("Writing threads completed till now",thread_write_over)
    lock.release()
    
    wmutex.acquire()
    writecount = writecount - 1
    if writecount == 0:
        print("Releasing the Lock, now readers can read")
        readTry.release()
    wmutex.release()               

print("Enter no. of Writers")
n_writers = int(input())
print("Enter no. of Readers")
n_readers = int(input())
l = max(n_writers,n_readers)
# To start running both the threads of reader and writer concurrently.
if n_writers >= n_readers:
    for i in range(0,n_readers):
        
        #print("I love to Read",i+1)
        tr= threading.Thread(target= read , name = "Reader" + str(i+1), args = (i+1,))
        thread_read.append(tr)
        #print("I love to write",i+1)
         
        tw= threading.Thread(target= write, name="Writer" + str(i+1) , args = (i+1,))
        thread_write.append(tw)
        
        tw.start()
        tr.start() 
    i = i+1    
    for j in range(0,n_writers-n_readers):
        #print("I love to write",i+1)
        tw= threading.Thread(target= write, name="Writer" + str(i+1), args = (i+1,))  
        thread_write.append(tw)
        tw.start()
        i = i+1 
       
if n_writers < n_readers:
    for i in range(0,n_writers):
        
        #print("i love to Read",i+1)
        tr= threading.Thread(target= read ,name = "Reader" + str(i+1), args = (i+1,))
        thread_read.append(tr)
        #print("I love to write",i+1)
        tw= threading.Thread(target= write,name="Writer" + str(i+1) , args = (i+1,))
        thread_write.append(tw)
        tw.start()
        tr.start() 
    i = i+1    
    for j in range(0,n_readers-n_writers):
        
        tr= threading.Thread(target= read,name="Reader" + str(i+1), args = (i+1,))  
        thread_read.append(tr)
        tr.start()
        i = i+1 
tr.join()
tw.join()            



          

             
            