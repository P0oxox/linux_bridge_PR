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
def choose_status(): 
    ping_main = 1
    ping_sec = 1
    ping_backup = 1
    if "enp" in a["fo"]["main_iface"]:
        ping_main1 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main2 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main3 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        ping_main4 = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = int(threshold))
        if ping_main1 or ping_main2 or ping_main3 or ping_main4 == float:
            ping_main = 1
    else:
        ping_main = None   

    if "enp" in a["fo"]["sec_iface"]:
        ping_sec1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_sec4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_sec1 or ping_sec2 or ping_sec3 or ping_sec4 == float:
            ping_sec = 1
    else:
        ping_sec = None

    ping_backup = 1
    if "enp" in a["fo"]["backup_iface"]:
        ping_backup1 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup2 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup3 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        ping_backup4 = ping("8.8.8.8", interface = a["fo"]["sec_iface"],timeout = int(threshold))
        if ping_backup1 or ping_backup2 or ping_backup3 or ping_backup4 == float:
            ping_backup = 1
    else:
        ping_backup = None

 #ping_main, ping_sec, ping_backup
    if ping_main and ping_sec and ping_backup :
        info_json["main_iface"]["status"] = "Active"
        info_json["sec_iface"]["status"] = "Idle"
        info_json["backup_iface"]["status"] = "Idle"
        print("one")

        if a['fo']["failback"] == True:
            print("one failover")
            os.system('ifmetric {0} 1'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            if a["fo"]["main_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))



    if ping_main is None and ping_sec and ping_backup :
        if "en" in a["fo"]["main_iface"]:
            info_json["main_iface"]["status"] = "Fail"
        info_json["sec_iface"]["status"] = "Active"
        info_json["backup_iface"]["status"] = "Idle"
        print("two")
        if a['fo']["failback"] == True:
            print("two failback")
            os.system('ifmetric {0} 3'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 1'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            if a["fo"]["sec_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
          



    if ping_main and ping_sec is None and ping_backup :
        info_json["main_iface"]["status"] = "Active"
        if "en" in a["fo"]["sec_iface"]:
            info_json["sec_iface"]["status"] = "Fail"
        info_json["backup_iface"]["status"] = "Idle"
        print("three")
        if a['fo']["failback"] == True:            
            os.system('ifmetric {0} 1'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            if a["fo"]["main_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))
           



    if ping_main and ping_sec and ping_backup is None :
        print("four")
        info_json["main_iface"]["status"] = "Active"
        info_json["sec_iface"]["status"] = "Idle"
        if "en" in a["fo"]["backup_iface"]:
            info_json["backup_iface"]["status"] = "Fail"

        if a['fo']["failback"] == True:
            print("four failback")
            os.system('ifmetric {0} 1'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            # print(nat_show)
            if a["fo"]["main_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))




    if ping_main is None and ping_sec is None and ping_backup :
        if "en" in a["fo"]["main_iface"]:
            info_json["main_iface"]["status"] = "Fail"
        if "en" in a["fo"]["sec_iface"]:
            info_json["sec_iface"]["status"] = "Fail"
        info_json["backup_iface"]["status"] = "Active"
        print("five")
        if a['fo']["failback"] == True:  
            os.system('ifmetric {0} 2'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 1'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            if a["fo"]["backup_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))





    if ping_main and ping_sec is None and ping_backup is None:
        info_json["main_iface"]["status"] = "Active"
        if "en" in a["fo"]["sec_iface"]:
            info_json["sec_iface"]["status"] = "Fail"
        if "en" in a["fo"]["backup_iface"]:
            info_json["backup_iface"]["status"] = "Fail"
        print("six")
        if a['fo']["failback"] == True: 
            os.system('ifmetric {0} 1'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 3'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
            if a["fo"]["main_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))




    if ping_main is None and ping_sec and ping_backup is None :
        if "en" in a["fo"]["main_iface"]:
            info_json["main_iface"]["status"] = "Fail"

        info_json["sec_iface"]["status"] = "Active"
        if "en" in a["fo"]["backup_iface"]:
            info_json["backup_iface"]["status"] = "Fail"
        print("seven")
        if a['fo']["failback"] == True:             
            os.system('ifmetric {0} 3'.format(a["fo"]["main_iface"]))
            os.system('ifmetric {0} 1'.format(a["fo"]["sec_iface"]))
            os.system('ifmetric {0} 2'.format(a["fo"]["backup_iface"]))
            for i in range(len(no_use)):
                os.system('ifmetric {0} {1}'.format(no_use[i],i+10))
            
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["main_iface"]))
            os.system('iptables -t nat -D POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["backup_iface"]))
            nat_show = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")

            if a["fo"]["sec_iface"] not in nat_show:
                os.system('iptables -t nat -A POSTROUTING -s {0} -o {1} -j MASQUERADE'.format('192.168.0.0/24',a["fo"]["sec_iface"]))


    if ping_main is None and ping_sec is None and ping_backup is None :
        print("eight")     
          
    return info_json
            


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


        # ping_main1 = ping_main()
        # ping_sec1 = ping_sec()
        # ping_backup1 = ping_backup()
        info_status = choose_status()#ping_main1, ping_sec1, ping_backup1
        print(info_status)

        with open(path_to_file, "w") as f:
            f.write(json.dumps(info_status))

        time.sleep(int(detection_period))

