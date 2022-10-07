'''
要改很多地方
'''

import os
import time
from ping3 import ping, verbose_ping
from datetime import datetime

path_to_file = "/home/pp/5gJUMP/ping3.log"
host = "8.8.8.8"
interface = ["enp0s3","enp0s8","enp0s9","enp0s10"]
can_use_WANs = []
while True:
    with open(path_to_file, "a") as f:
        for i in range(4):
            second = ping(host, interface = interface[i]) 
            if second is None:
                f.write(interface[i] +' failed!\n')
            else:
                # print('ping-{}, took: {}s, use: {}'.format(host,second,interface))
                f.write(interface[i] +' can use.\n')

    
        f.write("The current timestamp is: " + str(datetime.now()))
        f.write("\n")
        f.close()
    time.sleep(3)



    # def if_ping_8888(host, interface=None):   
    #     can_use_WANs = []
    #     for i in range(len(interface)):
    #         second = ping(host, interface = interface[i]) 
    #         if second is None:
    #             print(interface ,' failed!') 
    #         else:
    #             # print('ping-{}, took: {}s, use: {}'.format(host,second,interface))
    #             can_use_WANs.append(interface[i])
    #     return can_use_WANs