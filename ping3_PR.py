import os
import time
from ping3 import ping, verbose_ping
from datetime import datetime

def ping_some_ip(host,src_addr=None):
    second = ping(host,src_addr=src_addr)
    return second

if __name__ == '__main__':
    host = '8.8.8.8'
    src_addr_enp0s3 = '10.0.2.15'
    src_addr_enp0s8 = '172.30.1.148'
    while True:
        print('ping @ {}'.format(datetime.now()))
        result = ping_some_ip(host,src_addr_enp0s8)
        if result is None:
            print(result)
            print('ping 失敗！')
        else:
            print('ping-{}成功，耗时{}s'.format(host,result))
        time.sleep(5)
