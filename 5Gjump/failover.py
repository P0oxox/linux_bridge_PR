import os
import time
import socket
from ping3 import ping, verbose_ping
import json
import sys
import logging

def iface_name():
    en_to_eth = {}
    eth_to_en = {}
    en_to_eth["enp0s3"] = "eth1"
    en_to_eth["enp0s8"] = "eth2"
    en_to_eth["enp0s9"] = "eth3"
    en_to_eth["enp0s10"] = "eth4"
    eth_to_en["eth1"] = "enp0s3"
    eth_to_en["eth2"] = "enp0s8"
    eth_to_en["eth3"] = "enp0s9"
    eth_to_en["eth4"] = "enp0s10"
    return en_to_eth,eth_to_en
    
def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

def str_to_json(json_str_file):
    json_fomat = json.loads(json_str_file)
    return json_fomat

# find_interface()  先找全部的 WAN                    
# if_has_IP()       再篩選出有 IP 的                   
class find_WANs:
    def find_interface():
        interface_list = socket.if_nameindex()
        i_list = []
        for i in interface_list:
            i_list.append(i[1])  #這是所有的 interface，包括 br0 跟 lo
        WANs = []
        for i in i_list:
            if 'en' in i:
                WANs.append(i)  # 這是只有 enp0sxxx 的 interface
        return WANs

    def if_has_IP(WANs):
        all_WANs = []
        has_IP_WANs = []
        for i in range(len(WANs)):
            all_WANs.append(os.system('ip -4 addr show {0} | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\'  >/dev/null 2>&1'.format(WANs[i],'1','2','{3}' )))
            if (all_WANs[i] == 256) : 
                logging.info("{} has no ip.".format(WANs[i]))       #這行是啥  
            else:
                has_IP_WANs.append(WANs[i])
        logging.info('這些是有 ip 的 WAN ' + str(has_IP_WANs))
        return has_IP_WANs


# choose_3_WANs() 選3個可用的 WAN  
class choose_WANs:
    def choose_3_WANs(WANs): 
        choose_WANs = {"main iface":[],"sec iface":[],"backup iface":[]}
        print("Choose 3 WANs: ")
        print("Now all available WANs are: ", WANs )

        main_iface = input("Please choose main iface: ")     
        if main_iface in WANs:
            choose_WANs["main iface"].append(main_iface)
            # choose_WANs.append(main_iface)
        else:
            print("it's not available WAN. ")
            choose_WANs["main iface"].append(None)
            return choose_WANs
        sec_iface = input("Please choose sec iface: ") 
        if sec_iface in WANs and sec_iface not in main_iface:
            # choose_WANs.append(sec_iface)
            choose_WANs["sec iface"].append(sec_iface)
        else:
            print("it's not available WAN. ")
            choose_WANs["main iface"].append()
            return choose_WANs
        backup_iface = input("Please choose backup iface: ") 
        if backup_iface in WANs and backup_iface not in main_iface and backup_iface not in sec_iface:
            # choose_WANs.append(backup_iface)
            choose_WANs["backup iface"].append(backup_iface)
        else:
            print("it's not available WAN. ")
            choose_WANs["main iface"].append()
            return choose_WANs
        return choose_WANs


# WANs_order()     排優先級          
# class order_WANs:
    # def WANs_order(WANs): 
#         if len(WANs)==4:
#             for i in WANs:
#                 if i=="main_iface":
#                     print(WANs["main_iface"] + " is main iface.")
#                     # os.system('ifmetric {} 2'.format(WANs["main_iface"]))
#                     # os.system('ifmetric {} 8'.format(WANs["sec_iface"]))
#                     # os.system('ifmetric {} 9'.format(WANs["backup_iface"]))
#                     # os.system('ifmetric {} 10'.format(WANs["forth_iface"]))
#                     nmcli connection modify WANs["main_iface"] ipv4.route-metric 1
#                     nmcli connection up WANs["main_iface"]

#                 elif i=="sec_iface":
#                     print(WANs[i] + " is sec iface.")

#                 elif i=="backup_iface":
#                     print(WANs[i] + " is backup iface.")

#                 elif i=="forth_iface":
#                     print(WANs[i] + " is forth iface.")
#                 else:
#                     print("Something Wrong.")
#         if len(WANs)==3:
#             for i in WANs:
#                 if i=="main_iface":
#                     print(WANs["main_iface"] + " is main iface.")
#                     os.system('ifmetric {} 1'.format(WANs["main_iface"]))
#                     os.system('ifmetric {} 5'.format(WANs["sec_iface"]))
#                     os.system('ifmetric {} 7'.format(WANs["backup_iface"]))
#                 elif i=="sec_iface":
#                     print(WANs[i] + " is sec iface.")

#                 elif i=="backup_iface":
#                     print(WANs[i] + " is backup iface.")
#                 else:
#                     print("Something Wrong.")






if __name__ == '__main__':
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, filename='/var/log/failover.log', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    input_json = str_to_json(sys.argv[1])
    ##
    # 全域變數???
    all_WANs = find_WANs.find_interface()
    ip_WANs = find_WANs.if_has_IP(all_WANs)
    choose3_WANs = choose_WANs.choose_3_WANs(ip_WANs)
    ##

    if input_json['function'] == 'supported':
        output_json = {}  
        try:
            output_json["ifaces"] = []
            
            en_to_eth,eth_to_en = iface_name()
            for iface in ip_WANs:
                output_json["ifaces"].append({"text":en_to_eth[iface],"value":iface})
            output_json['status'] = True
        except:
            error_msg = "nono"
            output_json['status'] = False
            output_json['err_message'] = error_msg
        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()


    if input_json['function'] == 'current_config': #讀取目前設定值 
        output_json = {}  
        try:
            output_json['mode'] = "fo"
            output_json['ping_target'] = "8.8.8.8"
            output_json["fo"] = []
            
            # for iface in choose3_WANs:
            output_json["fo"].append({"failback":"true"})
            output_json["fo"].append({"main iface":choose3_WANs["main iface"]})
            output_json["fo"].append({"sec iface":choose3_WANs["sec iface"]})
            output_json["fo"].append({"backup iface":choose3_WANs["backup iface"]})
            output_json['single'] = {"main_iface":choose3_WANs["main iface"]}
            output_json['status'] = True

        except:
            error_msg = "nono"
            output_json['status'] = False
            output_json['err_message'] = error_msg
        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()        


    else:
        all_WANs = find_WANs.find_interface()
        ip_WANs = find_WANs.if_has_IP(all_WANs)
        host = '8.8.8.8'

        # setting_iface = choose_WANs.setting(ip_WANs)

    
