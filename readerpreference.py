import threading
import time
#barrier  = threading.Barrier(1)
sema_write = threading.Semaphore()
sema_read = threading.Semaphore()
readcount = 0
val = 0
reader_value = 0
writer_value = 0
thread_read = []
thread_read_over = []
thread_write = []
thread_write_over = []
def read(i):
    #for k in range(0,6):
    
    global readcount
    global val
    global reader_value
    global thread_read
    global thread_read_over
        
    
       
    sema_read.acquire()
    
    
      
    
    readcount  = readcount + 1
    if readcount==1:
        sema_write.acquire()
        print("Now writers have to wait")
    sema_read.release()
    #CS Stars
    thread_read_over.append(threading.currentThread().name)

    print(threading.currentThread().name,"in the reading critical section")
    print(threading.currentThread().name,"reading the val=",val)
    print("ReadCount is",readcount)

    
    time.sleep(1)
    #CS Ends
    sema_read.acquire()
   
    readcount = readcount - 1
    if readcount ==0:
        sema_write.release()
        print("Now writers can write")
       
       
    sema_read.release()    
        
def write(i):
    #for j in range(0,6):
        
    global val
    global thread_write
    global thread_write_over
    
    for j in thread_write:
        if j.name != threading.currentThread().name and j.name not in thread_write_over :
            print(j.name, "in waiting queue")
    
    sema_write.acquire()
    print(threading.currentThread().name,"Breaks the Wait Barrier") 
    #CS Starts
    val = val + 1
    thread_write_over.append(threading.currentThread().name)
    print(threading.currentThread().name,"in the writing critical section")
    print(threading.currentThread().name,"writing the value",val)
    time.sleep(1)
    #CS Ends
    print("Writing threads completed till now",thread_write_over)
    sema_write.release()            
    




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

  
    
                       



          

             
            