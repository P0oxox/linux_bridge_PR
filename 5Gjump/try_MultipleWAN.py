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


def setting():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/setting_fo.json','r')   #setting_single
    a = json.load(jsonFile)
    output_json = {}
    if a['mode'] == "fo" :
        output_json["function"] = 'setting'
        output_json["mode"] = a['mode']
        output_json["ping_target"] = a['ping_target']
        output_json["failback"]=True
        output_json["main_iface" ]=a['main_iface']
        output_json["sec_iface" ]=a['sec_iface']
        output_json["backup_iface"]=a['backup_iface']
        output_json["detection_mode"] = a['detection_mode']
        output_json["latency"] = a['latency']
    if a['mode'] == "single":
        output_json["function"] = 'setting'
        output_json["main_iface" ]=a['main_wan']
        output_json["ping_target"] = a['ping_target']
        output_json["mode"] = a['mode']
    return output_json

def info():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)

    if a['mode'] == "fo": 
        if_info = subprocess.getoutput("ifconfig "+ a["main_iface"])
        result = {}
        line_list = if_info.split('\n')   
        mode = "fo"
        name = line_list[0].split()[0]
        ip = line_list[1].split()[1]
        mac_address = line_list[3].split()[1]
        netmask = line_list[1].split()[3]

        rx_start = subprocess.getoutput("cat /sys/class/net/"+a["main_iface"]+"/statistics/rx_bytes")
        tx_start = subprocess.getoutput("cat /sys/class/net/"+a["main_iface"]+"/statistics/tx_bytes")
        time.sleep(1)
        rx_end = subprocess.getoutput("cat /sys/class/net/"+a["main_iface"]+"/statistics/rx_bytes")
        tx_end = subprocess.getoutput("cat /sys/class/net/"+a["main_iface"]+"/statistics/tx_bytes")
        rx_byte = int(rx_end)-int(rx_start)
        tx_byte = int(tx_end)-int(tx_start)
        result["main_iface"] = []
        result["main_iface"].append({"name":name,"ip":ip,"mac_address":mac_address,"netmask":netmask,"traffic":{"tx":tx_byte,"rx": rx_byte},'status' : "Active"})

    if a['mode'] == "single":  #不太確定single mode時，info要吐什麼json
        result = {}
        result["mode"] = "single"
        if_info = subprocess.getoutput("ifconfig "+ a["main_iface"])
        line_list = if_info.split('\n') 
        result["name"] = line_list[0].split()[0]
        time.sleep(1)
    return result

    

def current_config():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)
    
    if a["mode"] == 'fo':
        output_json = {}
        output_json["mode"] = a['mode']
        output_json["ping_target"] = a['ping_target']
        output_json["fo"]=[]
        output_json["fo"].append({"failback":"true","main_iface":a['main_iface'],"sec_iface":a['sec_iface'],"backup_iface":a['backup_iface'],"detection_mode":a["detection_mode"],"latency":a['latency']})
        # output_json["status"] = True
        output_json['single'] = 0
    if a["mode"] == 'single':
        output_json = {}
        output_json["mode"] = a['mode']
        output_json["ping_target"] = a['ping_target']
        output_json["single"] = []
        output_json["single"].append({"main_iface":a['main_iface']})
        # output_json["status"] = True
        output_json["fo"]=0


    return output_json



if __name__ == '__main__':

    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, filename='/var/log/failover.log', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    input_json = str_to_json(sys.argv[1])  

#===========================================================#
    if input_json['function'] == 'supported':
        output_json = {}  
        try:
            all_wan = supported.find_WAN()  # read Json file to find all WAN
            ip_wan = supported.if_has_IP(all_wan)  # find who has ip in all WAN
            output_json["ifaces"] = []
            
            en_to_eth,eth_to_en = iface_name()
            for iface in ip_wan:
                output_json["ifaces"].append({"text":en_to_eth[iface],"value":iface})
            output_json['status'] = True
            
        except:
            error_msg = "supported is wrong"
            output_json['status'] = False
            output_json['err_message'] = error_msg


        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()
        with open("supported_iface.json", "w") as f:
            f.write(json.dumps(output_json))

#===========================================================#
    if input_json['function'] == 'setting': 
        output_json = {}
        output_setting = {}
        try:
            output_json = setting()
            output_setting['status'] = True
        except:
            error_msg = "Setting is wrong"
            output_setting['status'] = False
            output_setting['err_message'] = error_msg
        sys.stdout.write(json_to_str(output_setting))
        sys.stdout.flush()
        with open("current_config.json", "w") as f:
            f.write(json.dumps(output_json))
        with open("setting.json", "w") as f:
            f.write(json.dumps(output_setting))
#===========================================================#
    if input_json['function'] == 'info':
        while True:
            output_json = {}  
            try: 
                output_json = info()
                output_json['status'] = True
            except:
                error_msg = "info is wrong"
                output_json['status'] = False
                output_json['err_message'] = error_msg
                break
            sys.stdout.write(json_to_str(output_json))
            sys.stdout.flush()
            with open("info.json", "w") as f:
                f.write(json.dumps(output_json))

#===========================================================#
    if input_json['function'] == 'current_config': 
        jsonFile_b = open('/home/pp/linux_bridge_PR/5Gjump/current_function.json','r')
        b = json.load(jsonFile_b)
        a = {}
        try:
            a = current_config()
            b['mode'] = a['mode']
            if a['fo'] != 0:
                b['fo']["main_iface"] = a['fo'][0]['main_iface']
                b['fo']["sec_iface"] = a['fo'][0]['sec_iface']
                b['fo']["backup_iface"] = a['fo'][0]['backup_iface']
                b['fo']["detection_mode"] = a['fo'][0]['detection_mode']
                b['fo']["latency"]['threshold'] = a['fo'][0]['latency']['threshold']
                b['fo']["latency"]['detection_period'] = a['fo'][0]['latency']['detection_period'] 
            if a['single'] != 0:
                b['single']["main_iface"] = a['single'][0]['main_iface']
            b['status'] = True
        except:
            error_msg = "current_config is wrong"
            b['status'] = False
            b['err_message'] = error_msg
        sys.stdout.write(json_to_str(b))
        sys.stdout.flush()

        with open("current_function_01.json", "w") as f:
            f.write(json.dumps(b))






 

