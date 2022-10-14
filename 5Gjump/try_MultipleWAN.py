import os
import time
import json
from json import load
import sys
import logging
import subprocess 

def iface_name():
    en_to_eth = {}
    eth_to_en = {}
    en_to_eth["enp0s3"] = "Mobile Network"
    en_to_eth["enp0s8"] = "Wi-Fi"
    en_to_eth["enp0s9"] = "NR"
    en_to_eth["enp0s10"] = "LTE"  
    return en_to_eth,eth_to_en
    
def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

def str_to_json(json_str_file):
    json_fomat = json.loads(json_str_file)
    return json_fomat

class supported():
    # read Json file to find all WAN
    def find_WAN():
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/iface.json','r')
        a = json.load(jsonFile)
        all_wan = []
        for i in range(len(a["inter_face"])):
            all_wan.append(a["inter_face"][i]['value'])
        return all_wan
    # check the wan whether has IP
    def if_has_IP(WANs):
        all_WANs = []
        has_IP_WANs = []
        for i in range(len(WANs)):
            all_WANs.append(os.system('ip -4 addr show {0} | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\'  >/dev/null 2>&1'.format(WANs[i],'1','2','{3}' )))
            if (all_WANs[i] != 256) : 
                has_IP_WANs.append(WANs[i])
        return has_IP_WANs


# 1. 讀json看是 fo 還是 single mode
# 2. 產生 current_config.json
# 3. 產生 current_config.json
def setting():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/setting_fo.json','r')
    a = json.load(jsonFile)
    if a['mode'] == "fo": 
        # os.system() 啟動systemd 
        
        print('Now is fo mode, start systemd. <還沒寫好> ')
    elif a['mode'] == "single":
        
        print('Now is single mode, stop systemd. <還沒寫好> ')
    else:
        print('wrong')

def info():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)
    if a['mode'] == "fo": 
        if_info = subprocess.getoutput("ifconfig "+ a["main_iface"])
        result = {}
        result["mode"] = "fo"
        line_list = if_info.split('\n')
        # name = line_list[0].split()[0]
        # ip = line_list[1].split()[1]
        # mac address = line_list[3].split()[1]
        # netmask = line_list[1].split()[3]

        # result["main_iface"].append({"name":name})
        # result["main_iface"].append({"ip":line_list[1].split()[1]})
        # result["main_iface"].append({"mac_address":line_list[3].split()[1]})
        # result["main_iface"].append({"netmask":line_list[1].split()[3]})
        # result["main_iface"].append({"traffic":"to do"})

        
        result["name"] = line_list[0].split()[0]
        result["ip"] = line_list[1].split()[1]
        result["mac_address"] = line_list[3].split()[1]
        result["netmask"] = line_list[1].split()[3]

    elif a['mode'] == "single":
        result["mode"] = "single"
    else:
        print('wrong')
    return result
    
    



def current_config():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)
    output_json = {}

if __name__ == '__main__':

    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, filename='/var/log/failover.log', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    input_json = str_to_json(sys.argv[1])  

    ###
    all_wan = supported.find_WAN()  # read Json file to find all WAN
    ip_wan = supported.if_has_IP(all_wan)  # find who has ip in all WAN
    # setting() # fo mode or single mode


    ###

    if input_json['function'] == 'supported':
        output_json = {}  
        try:
            output_json["ifaces"] = []
            
            en_to_eth,eth_to_en = iface_name()
            for iface in ip_wan:
                output_json["ifaces"].append({"text":en_to_eth[iface],"value":iface})
            output_json['status'] = True
            

        except:
            error_msg = "nono, something is wrong"
            output_json['status'] = False
            output_json['err_message'] = error_msg


        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()
        with open("supported_iface.json", "w") as f:
            f.write(json.dumps(output_json))

#===========================================================#
    if input_json['function'] == 'setting':
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/setting_fo.json','r')
        a = json.load(jsonFile)
        output_json = {}
        output_setting = {}
        try:
            if a['mode'] == "fo" :
                output_json["function"] = 'setting'
                output_json["mode"] = a['mode']
                output_json["ping_target"] = a['ping_target']

                # output_json["fo"] = []
                output_json["failback" ]=True
                output_json["main_iface" ]=a['main_iface']
                output_json["sec_iface" ]=a['sec_iface']
                output_json["backup_iface"]=a['backup_iface']
                output_json["detection_mode"] = a['detection_mode']
                output_json["latency"] = a['latency']
                output_setting['status'] = True
            elif a['mode'] == "single":
                output_json["function"] = 'setting'
                output_json["main_wan" ]=a['main_iface']
                output_json["ping_target"] = a['ping_target']
                output_json["mode"] = a['mode']
                output_setting['status'] = True
            else: #a['mode'] == "single"
                output_setting['status'] = False
                output_setting['err_message'] = error_msg
        except:
            error_msg = "Something is wrong"
            output_setting['status'] = False
            output_setting['err_message'] = error_msg


        # sys.stdout.write(json_to_str(output_json))
        sys.stdout.write(json_to_str(output_setting))
        sys.stdout.flush()
        with open("current_config.json", "w") as f:
            f.write(json.dumps(output_json))
        with open("setting.json", "w") as f:
            f.write(json.dumps(output_setting))
#===========================================================#
    if input_json['function'] == 'info':
        i = info()
        print("i=",i["mac_address"],"..")
        output_json = {}  
        try: 
            output_json["mode"] = i["mode"]
            output_json["main_iface"] = []
            output_json["main_iface"].append({"name":i["name"],"ip":i["ip"],"mac_address":i["mac_address"],"netmask":i["netmask"],'status' : "Active"})
            # output_json["main_iface"].append({}) 
            # output_json["main_iface"].append({})
            # output_json["main_iface"].append({]})
            output_json["main_iface"].append({"traffic":"to do"})


            

        except:
            error_msg = "nono, something wrong"
            output_json['status'] = False
            output_json['err_message'] = error_msg


        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()
        with open("info.json", "w") as f:
            f.write(json.dumps(output_json))







 

