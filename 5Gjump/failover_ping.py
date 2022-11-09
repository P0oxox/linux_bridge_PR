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

# ifaces = ['enp0s3','enp0s8','enp0s9','enp0s10']

def choose_status():
    if "enp" in a["fo"]["main_iface"]:
        ping_main1 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main2 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main3 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main4 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        if ping_main1 and ping_main2 and ping_main3 and ping_main4 != float:
            ping_main = None
        else:
            ping_main = 1
        
    if "enp" in a["fo"]["sec_iface"]:
        ping_sec1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_sec1 and ping_sec2 and ping_sec3 and ping_sec4 != float:
            ping_sec = None
        else:
            ping_sec = 1

    if "enp" in a["fo"]["backup_iface"]:
        ping_backup1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_backup1 and ping_backup2 and ping_backup3 and ping_backup4 != float:
            ping_backup = None
        else:
            ping_backup = 1
    

            

path_to_file = "/home/pp/linux_bridge_PR/5Gjump/failover"
if __name__ == '__main__':

    while True:
        info_json = {"main_iface":{"status":''},"sec_iface":{"status":''},"backup_iface":{"status":''}}
        current_config_jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
        a = json.load(current_config_jsonFile)

        no_use = []
        for i in ifaces:
            if i != a["fo"]["main_iface"] and i != a["fo"]["sec_iface"] and i != a["fo"]["backup_iface"]:
                no_use.append(i)
        threshold = a["fo"]['latency']["threshold"]
        detection_period = a["fo"]['latency']["detection_period"]

        info_status = choose_status()
        print(info_status)

        with open(path_to_file, "w") as f:
            f.write(json.dumps(info_status))

        time.sleep(int(detection_period))

