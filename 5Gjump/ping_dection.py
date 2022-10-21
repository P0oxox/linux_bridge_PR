import os
import time
from ping3 import ping, verbose_ping
from datetime import datetime

path_to_file = "/home/pp/linux_bridge_PR/5Gjump/ping3.log"
host = "8.8.8.8"
interface = ["enp0s3","enp0s8","enp0s9","enp0s10"]

def dectect():
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

def wan_initialize():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)
    print(a["fo"]['latency']["threshold"])
    if a['mode'] == "fo": 
        wan_status = {"main_iface":"Active", "sec_iface": "Idle", "backup_iface":"Idle"}  #從這邊丟回info?????
        second = ping("8.8.8.8", interface = a["fo"]["main_iface"],timeout = a["fo"]['latency']["threshold"])
            if second is None :
                wan_status = {"main_iface":"Fail", "sec_iface": "Active", "backup_iface":"Idle"}
            else:
                wan_status = {"main_iface":"Active", "sec_iface": "Idle", "backup_iface":"Idle"}




if __name__ == '__main__':
    dectect()



