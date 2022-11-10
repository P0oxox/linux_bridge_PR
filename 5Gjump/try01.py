import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping
ifaces = ['enp0s3','enp0s8','enp0s9','enp0s10']
def ping_main(): 
    if "enp" in a["fo"]["main_iface"]:
        ping_main1 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main2 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main3 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main4 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        if ping_main1 or ping_main2 or ping_main3 or ping_main4 == float:
            ping_main = 1
        else:
            ping_main = None
    else:
        ping_main = None   
    return ping_main    

def ping_sec():
    if "enp" in a["fo"]["sec_iface"]:
        # ping_sec = 1
        ping_sec1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_sec1 or ping_sec2 or ping_sec3 or ping_sec4 == float:
            ping_sec = 1
        else:
            ping_sec = None
    else:
        ping_sec = None
    return ping_sec

def ping_backup():
    if "enp" in a["fo"]["backup_iface"]:
        # ping_backup = 1
        ping_backup1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_backup1 or ping_backup2 or ping_backup3 or ping_backup4 == float:
            ping_backup = 1
        else:
            ping_backup = None
    else:
        ping_backup = None
    return ping_backup

if __name__ == '__main__':

    while True:
        info_json = {"main_iface":{"status":'Idle'},"sec_iface":{"status":'Idle'},"backup_iface":{"status":'Idle'}}
        current_config_jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
        a = json.load(current_config_jsonFile)

        no_use = []
        for i in ifaces:
            if i != a["fo"]["main_iface"] and i != a["fo"]["sec_iface"] and i != a["fo"]["backup_iface"]:
                no_use.append(i)
        threshold = a["fo"]['latency']["threshold"]
        detection_period = a["fo"]['latency']["detection_period"]

        ping_main1 = ping_main()
        ping_sec1 = ping_sec()
        ping_backup1 = ping_backup()
        print("ping_main")
        print(ping_main1)
        print("ping_sec")
        print(ping_sec)
        print("ping_backup1")
        print(ping_backup1)


        time.sleep(int(detection_period))
