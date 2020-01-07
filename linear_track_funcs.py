import serial
import serial.tools.list_ports
import os,sys
import time
 #%% functions
def countdown(seconds):
    i=0
    while True:
        sys.stdout.write("%.1is in total %ss"%(i,seconds))
        sys.stdout.write("\r")
        time.sleep(1)
        i += 1
        if i >= seconds:
            #sys.stdout.write("%s countdown finished"%seconds)
            break

def check_ports(serial_ports):
    ports = [i.device for i in serial.tools.list_ports.comports()]
    if len(ports) == 0:
        print("There is no ports avilable")
        sys.exit()
    else:
        for i in serial_ports:          
            if i in ports:
                print(f'{i} is available')
            else:
                print(f'{i} is unavailable, please choose from{ports}')
                sys.exit()
#check_ports(r'/dev/ttyUSB0')

#def RandomContextOrder(context_nu=2,trials=30,blocks=3):
def RandomContextOrder():
    ContextOrder_average = [
	[1,2,1,2,1,2,2,1,2,1],
	[2,2,2,2,1,1,1,1,2,1],
	[1,2,2,1,1,2,2,2,1,1],
	[2,1,1,2,2,1,2,1,2,1],
	[1,2,2,1,1,2,1,2,1,2],
	[1,2,1,2,1,2,2,1,2,1]]
    ContextOrder_most_1 =[ 
        [1,1,1,2,1,2,1,1,2,1],
        [1,2,1,2,1,1,1,1,2,1],
        [1,2,1,1,1,2,1,2,1,1],
        [1,1,1,2,1,1,2,1,2,1],
        [1,2,1,2,1,1,1,2,1,1],
        [2,1,1,2,1,2,1,1,2,1]]
    ContextOrder_most_2 = [
        [2,2,2,1,2,1,2,2,1,2],
        [2,1,2,1,2,2,2,2,1,2],
        [2,1,2,2,2,1,2,1,2,2],
        [2,2,2,1,2,2,1,2,1,2],
        [2,1,2,1,2,2,2,1,2,2],
        [1,2,2,1,2,1,2,2,1,2]]
    ContextOrder_all_1 = [
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1]]
    ContextOrder_all_2= [
        [2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2]]
    return ContextOrder_average
    #np.random.seed(12) # 取值12，
    #return np.random.randint(1,context_nu+1,(blocks,trials))
#p.sum(np.where(RandomContextOrder(2,30,3)==1,1,0),axis=1)

