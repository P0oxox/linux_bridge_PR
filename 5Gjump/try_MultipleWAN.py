import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping

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
    if_info = sys.argv[1]
    str_2_dic = json.loads(if_info)

    output_json1 = {"mode":str_2_dic["mode"],"ping_target":str_2_dic["ping_target"]}
    output_json2 = {}
    if str_2_dic["mode"]=="fo":    
        output_json2["fo"] = {"failback": str_2_dic["failback"],"main_iface":str_2_dic["main_iface"],"sec_iface":str_2_dic["sec_iface"],"backup_iface":str_2_dic["backup_iface"],"detection_mode":str_2_dic["detection_mode"] }
        output_json2["fo"]["latency"] = {"threshold":str_2_dic["latency"]["threshold"],"detection_period":str_2_dic["latency"]["detection_period"]}       
    output_json3 = {}
    if str_2_dic["mode"]=="single":  
        output_json3["single"] = {"main_iface": str_2_dic["main_wan"]}
    
    output_json1.update(output_json2)
    output_json1.update(output_json3)
    return output_json1


def info():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    a = json.load(jsonFile)
    if a['mode'] == "fo": 
        result = {}
        result["mode"]="fo"
        if "enp" in a["fo"]["main_iface"]:
            info = subprocess.getoutput("ifconfig "+ a["fo"]["main_iface"])
            line_list = info.split('\n')   
            name = line_list[0].split()[0]
            ip = line_list[1].split()[1]
            mac_address = line_list[3].split()[1]
            netmask = line_list[1].split()[3]
            rx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["main_iface"]+"/statistics/rx_bytes")
            tx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["main_iface"]+"/statistics/tx_bytes")
            time.sleep(1)
            rx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["main_iface"]+"/statistics/rx_bytes")
            tx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["main_iface"]+"/statistics/tx_bytes")
            rx_mbps = (int(rx_end)-int(rx_start))*(0.000008)
            tx_mbps = (int(tx_end)-int(tx_start))*(0.000008)
            # second = ping("8.8.8.8", interface = a["fo"]["main_iface"])
            # if second is None :
            #     status = "Fail"
            # else:
            #     status = "Active"
            result["main_iface"] = {"name":name,"ip":ip,"mac_address":mac_address,"netmask":netmask,"traffic":{"tx":tx_mbps,"rx": rx_mbps}}  # 'status' : status     
        else:
            result["main_iface"] = {"name":"none"}
        #===========================================================
        if "enp" in a["fo"]["sec_iface"]:
            info = subprocess.getoutput("ifconfig "+ a["fo"]["sec_iface"])
            line_list = info.split('\n')   
            name = line_list[0].split()[0]
            ip = line_list[1].split()[1]
            mac_address = line_list[3].split()[1]
            netmask = line_list[1].split()[3]
            rx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["sec_iface"]+"/statistics/rx_bytes")
            tx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["sec_iface"]+"/statistics/tx_bytes")
            time.sleep(1)
            rx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["sec_iface"]+"/statistics/rx_bytes")
            tx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["sec_iface"]+"/statistics/tx_bytes")
            rx_mbps = (int(rx_end)-int(rx_start))*(0.000008)
            tx_mbps = (int(tx_end)-int(tx_start))*(0.000008)
            second = ping("8.8.8.8", interface = a["fo"]["sec_iface"])
            # if second is None :
            #     status = "Fail"
            # else:
            #     status = "Idle"
            result["sec_iface"] = {"name":name,"ip":ip,"mac_address":mac_address,"netmask":netmask,"traffic":{"tx":tx_mbps,"rx": rx_mbps}}    #   ,'status' : status
        else:
            result["sec_iface"] = {"name":"none"}
        #=======================================================
        if "enp" in a["fo"]["backup_iface"]:
            info = subprocess.getoutput("ifconfig "+ a["fo"]["backup_iface"])
            line_list = info.split('\n')   
            name = line_list[0].split()[0]
            ip = line_list[1].split()[1]
            mac_address = line_list[3].split()[1]
            netmask = line_list[1].split()[3]
            rx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["backup_iface"]+"/statistics/rx_bytes")
            tx_start = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["backup_iface"]+"/statistics/tx_bytes")
            time.sleep(1)
            rx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["backup_iface"]+"/statistics/rx_bytes")
            tx_end = subprocess.getoutput("cat /sys/class/net/"+a["fo"]["backup_iface"]+"/statistics/tx_bytes")
            rx_mbps = (int(rx_end)-int(rx_start))*(0.000008)
            tx_mbps = (int(tx_end)-int(tx_start))*(0.000008)
            # second = ping("8.8.8.8", interface = a["fo"]["backup_iface"])
            # if second is None :
            #     status = "Fail"
            # else:
            #     status = "Idle"
            result["backup_iface"] = {"name":name,"ip":ip,"mac_address":mac_address,"netmask":netmask,"traffic":{"tx":tx_mbps,"rx": rx_mbps}}       #,'status' : status
        else:
            result["backup_iface"] = {"name":"none"}

    elif a['mode'] == "single":
        result["mode"] = "single"
    else:
        print('wrong')
    return result

def current_config():
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    output_json1 = json.load(jsonFile)
    # print(output_json1)
    # output_json2 = output_json['status'] = True
    # output_json1.update(output_json2)
    output_json1['status'] = True
    return output_json1

if __name__ == '__main__':

    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, filename='/var/log/failover.log', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    input_json = str_to_json(sys.argv[1])  

    #======================'supported'==========================#
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
        with open("supported.json", "w") as f:
            f.write(json.dumps(output_json))

    #======================="setting"============================#
    if input_json['function'] == 'setting': 
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
        b = json.load(jsonFile)
        output_json = {}
        output_setting = {}
        try:
            output_json = setting()
            b['mode'] = output_json['mode']
            b['ping_target'] = output_json['ping_target']
            if output_json["mode"] == 'fo':
                b['fo']["failback"] = output_json['fo']['failback']
                b['fo']["main_iface"] = output_json['fo']['main_iface']
                b['fo']["sec_iface"] = output_json['fo']['sec_iface']
                b['fo']["backup_iface"] = output_json['fo']['backup_iface']
                b['fo']["detection_mode"] = output_json['fo']['detection_mode']
                b['fo']["latency"]['threshold'] = output_json['fo']['latency']['threshold']
                b['fo']["latency"]['detection_period'] = output_json['fo']['latency']['detection_period'] 
            if output_json["mode"] == 'single':
                b['single']["main_iface"] = output_json['single']['main_iface']

            output_setting['status'] = True
        except:
            error_msg = "Setting is wrong"
            output_setting['status'] = False
            output_setting['err_message'] = error_msg
        sys.stdout.write(json_to_str(output_setting))
        sys.stdout.flush()
        with open("current_config.json", "w") as f:
            f.write(json.dumps(b))
        with open("setting.json", "w") as f:
            f.write(json.dumps(output_setting))
    #====================='info'================================#
    if input_json['function'] == 'info':
        # jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
        # b = json.load(jsonFile)
        while True:
            output_json = {}  
            try: 
                output_json = info()
                # output_json['status'] = True
            except:
                error_msg = "info is wrong"
                output_json['status'] = False
                output_json['err_message'] = error_msg
                break
            sys.stdout.write(json_to_str(output_json))
            sys.stdout.write("\n")
            sys.stdout.flush()
            with open("info.json", "w") as f:
                f.write(json.dumps(output_json))

    #======================'current_config'============================#
    if input_json['function'] == 'current_config': 
        output_json = {}
        try:
            output_json = current_config()
        except:
            error_msg = "current_config is wrong"
            output_json['status'] = False
            output_json['err_message'] = error_msg
        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()
        with open("current_config.json", "w") as f:
            f.write(json.dumps(output_json))





 

