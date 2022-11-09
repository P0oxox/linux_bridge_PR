import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping




ping_main1 = ping("8.8.8.8", interface = "enp0s8") #,timeout = 2
ping_main2 = ping("8.8.8.8", interface = "enp0s8")#,timeout = 2
ping_main3 = ping("8.8.8.8", interface = "enp0s8")#,timeout = 2
ping_main4 = ping("8.8.8.8", interface = "enp0s8")#,timeout = 2
# ping_test = verbose_ping("8.8.8.8", interface = "enp0s8")

if __name__ == '__main__':
    # if "enp" in a["fo"]["main_iface"]:
    #     ping_main1 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
    #     ping_main2 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
    #     ping_main3 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
    #     ping_main4 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
    ping_main = None
    if ping_main1 or ping_main2 or ping_main3 or ping_main4 == float:
        ping_main = 1
    else:
        ping_main = None
    # else:
    #     ping_main = None
        
    # if "enp" in a["fo"]["sec_iface"]:
    #     ping_sec = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
    # else:
    #     ping_sec = None
    # if "enp" in a["fo"]["backup_iface"]:
    #     ping_backup = ping("8.8.8.8", interface = a["fo"]["backup_iface"],timeout = int(threshold))
    # else:
    #     ping_backup = None


    print(ping_main1, type(ping_main1))
    print(ping_main2, type(ping_main2))
    print(ping_main3, type(ping_main3))
    print(ping_main4, type(ping_main4))
    print(ping_main1 or ping_main2 or ping_main3 or ping_main4)
    print(ping_main)

    # a = 0.004090309143066406
    # b = None
    # c = False
    # print(a, type(a))
    # print(b, type(b))
    # print(c, type(c))
    # print(a or b)
    # print(a or c)
    # print(a or b or c)