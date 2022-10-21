import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping
from datetime import datetime

ifaces = ['enp0s3','enp0s8','enp0s9','enp0s10']
jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
a = json.load(jsonFile)
no_use = []
for i in ifaces:
    if i != a["fo"]["main_iface"] and i != a["fo"]["sec_iface"] and i != a["fo"]["backup_iface"]:
        no_use.append(i)


def choose_status():
    threshold = a["fo"]['latency']["threshold"]
    detection_period = a["fo"]['latency']["detection_period"]

    while True:
        if "enp" in a["fo"]["main_iface"]:
            ping_main = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        else:
            ping_main = None
        if "enp" in a["fo"]["sec_iface"]:
            ping_sec = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        else:
            ping_sec = None
        if "enp" in a["fo"]["backup_iface"]:
            ping_backup = ping("8.8.8.8", interface = a["fo"]["backup_iface"],timeout = int(threshold))
        else:
            ping_backup = None

        if ping_main and ping_sec and ping_backup :
            wan_status = {"main_iface":"Active", "sec_iface": "Idle", "backup_iface":"Idle"}
            print("one")
        if ping_main is None and ping_sec and ping_backup :
            wan_status = {"main_iface":"Fail", "sec_iface": "Active", "backup_iface":"Idle"}
            print("two")
        if ping_main and ping_sec is None and ping_backup :
            wan_status = {"main_iface":"Active", "sec_iface": "Fail", "backup_iface":"Idle"}
            os.system('ifmetric {0} 1'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))

            # os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))
            
            print("three")



        if ping_main and ping_sec and ping_backup is None :
            wan_status = {"main_iface":"Active", "sec_iface": "Idle", "backup_iface":"Fail"}
            print("four")
        if ping_main is None and ping_sec is None and ping_backup :
            wan_status = {"main_iface":"Fail", "sec_iface": "Fail", "backup_iface":"Active"}
            print("five")
        if ping_main and ping_sec is None and ping_backup is None:
            wan_status = {"main_iface":"Active", "sec_iface": "Fail", "backup_iface":"Fail"}
            print("six")
        if ping_main is None and ping_sec and ping_backup is None :
            wan_status = {"main_iface":"Fail", "sec_iface": "Active", "backup_iface":"Fail"}
            print("seven")
        if ping_main is None and ping_sec is None and ping_backup is None :
            wan_status = {"main_iface":"Fail", "sec_iface": "Fail", "backup_iface":"Fail"}
            print("eight")       


        



        time.sleep(int(detection_period))




if __name__ == '__main__':
    choose_status()
    



