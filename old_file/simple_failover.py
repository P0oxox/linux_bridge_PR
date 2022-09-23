import os
import time
from ping3 import ping, verbose_ping
from datetime import datetime

def ping_enp0s8(host, interface=None):   
    while True:
        second = ping(host, interface=interface) 
        if second is None:
            print('ping enp0s8 failed!')
            os.system('bash return_to_enp0s3.sh')
            break
        else:
            print('ping-{}, took: {}s, use: {}'.format(host,second,interface))
        time.sleep(1)

def ping_enp0s3(host, interface=None):   
    while True:
        second = ping(host, interface=interface) 
        if second is None:
            print('ping enp0s3 failed!')
            os.system('bash turn_to_enp0s8.sh')
            break
        else:
            print('ping-{}, took: {}s, use: {}'.format(host,second,interface))
        time.sleep(1)

if __name__ == '__main__':
    host = '8.8.8.8'
    interface_enp0s8 = 'enp0s8'
    interface_enp0s3 = 'enp0s3'
    while(True):
        if(ping( host, interface = interface_enp0s8) ):
            print('=============')
            print('using enp0s8')
            print('=============')
            ping_enp0s8(host,interface_enp0s8)  
        elif(ping( host, interface = interface_enp0s3) ):
            print('=============')
            print('using enp0s3')
            print('=============')
            ping_enp0s3(host,interface_enp0s3) 
        else:
            print('=============')
            print('both Interface couldn\'t use')
            print('=============')

        time.sleep(0.2)



def disconnected():
    time.sleep(5)
    print('要搗蛋囉')
    os.system('bash disconnected_enp0s8.sh')

