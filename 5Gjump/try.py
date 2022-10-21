import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping

class info():
    def find_WAN():
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
        a = json.load(jsonFile)
        if a['mode'] == "fo": 
            iface = [a["fo"]["main_iface"], a["fo"]["sec_iface"], a["fo"]["backup_iface"]]
            ifa = []
            for i in iface:
                if 'en' in i:
                    ifa.append(i)
        return ifa
    def info():
        if a['mode'] == "fo": 
            info = []
            info.append(subprocess.getoutput("ifconfig "+ ifa[-1]))
def pinf8888():
    host = "google.com"
    interface = "enp0s3"
    second = ping(host,interface=interface) 
    if second is None :
        status = "Fail"
        print("Fail")
    else:
        status = "true"
        print("true")
        print(status)

    # result = {}
    # for i in range(len(info)):
    #     print(i)
        # line_list = info[i].split('\n')   
        # # mode = "fo"
        # name = line_list[0].split()[0]
        # ip = line_list[1].split()[1]
        # mac_address = line_list[3].split()[1]
        # netmask = line_list[1].split()[3]
        # rx_start = subprocess.getoutput("cat /sys/class/net/"+i+"/statistics/rx_bytes")
        # tx_start = subprocess.getoutput("cat /sys/class/net/"+i+"/statistics/tx_bytes")
        # time.sleep(1)
        # rx_end = subprocess.getoutput("cat /sys/class/net/"+i+"/statistics/rx_bytes")
        # tx_end = subprocess.getoutput("cat /sys/class/net/"+i+"/statistics/tx_bytes")
        # rx_mbps = (int(rx_end)-int(rx_start))*(0.000008)
        # tx_mbps = (int(tx_end)-int(tx_start))*(0.000008)
        # result["i"] = {"name":name,"ip":ip,"mac_address":mac_address,"netmask":netmask,"traffic":{"tx":tx_mbps,"rx": rx_mbps},'status' : "Active"}




 

if __name__ == '__main__':

    pinf8888()
    # second = ping("enp0s3",'google.com')
    # print('it took {} second'.format(second))

   
