import threading
import time

qlock = threading.Semaphore()
rmutex = threading.Semaphore()
lock = threading.Semaphore()

readcount = 0
val = 0
thread_read = []
thread_read_over = []
thread_write = []
thread_write_over = []
def read(i):
    #for j in range(0,6):
    global readcount
    global val
    for j in thread_read:
        if j.name != threading.currentThread().name and j.name not in thread_read_over :
            print(j.name, "in waiting queue")
    qlock.acquire()
    rmutex.acquire()
    print(threading.currentThread().name,"Breaks the Wait Barrier")
    if readcount==0:
        lock.acquire()
        print("Writers have to wait")
        
    readcount  = readcount + 1 
    qlock.release()   
    rmutex.release()
    
    ##    Critical Section Starts
    thread_read_over.append(threading.currentThread().name)

    print(threading.currentThread().name,"in the reading critical section")
    print(threading.currentThread().name,"reading the val=",val)
    
    time.sleep(1)
    print(threading.currentThread().name,"exits")
    ## Critical Section Ends
    print("Reading threads completed till now",thread_read_over)
    rmutex.acquire()
    readcount = readcount - 1
    if readcount ==0:
        lock.release()
        print("Now writers can write")
    rmutex.release()    
        
def write(i):
    #for j in range(0,6):
    global val

    global thread_write
    global thread_write_over    
    qlock.acquire()
    print(threading.currentThread().name,"Breaks the Wait Barrier") 
    lock.acquire()
    qlock.release()
    
    #Critical Section Starts    
    for j in thread_write:
        if j.name != threading.currentThread().name and j.name not in thread_write_over :
            print(j.name, "in waiting queue")
    thread_write_over.append(threading.currentThread().name)
    val = val + 1
    print(threading.currentThread().name,"in the writing critical section")
    print(threading.currentThread().name,"writing the value",val)
    
    
    time.sleep(1)
    print(threading.currentThread().name,"exits")
    #Critical Section Ends
    print("Writing threads completed till now",thread_write_over)    
    lock.release()
    
                  

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

             
            