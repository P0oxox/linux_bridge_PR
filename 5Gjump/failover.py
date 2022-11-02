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
current_config_jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
a = json.load(current_config_jsonFile)


jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/info.json','r')
info_json = json.load(jsonFile)


no_use = []
for i in ifaces:
    if i != a["fo"]["main_iface"] and i != a["fo"]["sec_iface"] and i != a["fo"]["backup_iface"]:
        no_use.append(i)


def choose_status():
    threshold = a["fo"]['latency']["threshold"]
    detection_period = a["fo"]['latency']["detection_period"]
    # print(a['fo']["failback"])

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
            # wan_status = {"main_iface":"Active", "sec_iface": "Fail", "backup_iface":"Fail"}
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
            # wan_status = {"main_iface":"Fail", "sec_iface": "Active", "backup_iface":"Fail"}
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
            wan_status = {"main_iface":"Fail", "sec_iface": "Fail", "backup_iface":"Fail"}
            print("eight")     
            
        return info_json

        time.sleep(int(detection_period))



if __name__ == '__main__':
    # input_json = str_to_json(sys.argv[1])  
    # if input_json['failback'] == 'true':
    info_status = choose_status()
    with open("info.json", "w") as f:
        f.write(json.dumps(info_status))
    



