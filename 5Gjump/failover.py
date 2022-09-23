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
    en_to_eth["ens4"] = "eth1"
    eth_to_en["eth1"] = "ens4"
    return en_to_eth,eth_to_en
    
def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

def str_to_json(json_str_file):
    json_fomat = json.loads(json_str_file)
    return json_fomat

# 1. 先找全部的 WAN                    find_interface()
# 2. 篩選出跟 NetworkManager 有連接的   (不會寫)
# 3. 再篩選出有 IP 的                   if_has_IP()
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
                logging.info("{} has no ip.".format(WANs[i]))
                
            else:
                has_IP_WANs.append(WANs[i])
        logging.info('這些是有 ip 的 WAN ' + str(has_IP_WANs))
        return has_IP_WANs


# 1. 選3個可用的 WAN  choose_3_WANs()
# 2. 排優先級         WANs_order()
class choose_WANs:
    def choose_3_WANs(WANs): 
        main_iface = input("Please choose main iface: ") 
        sec_iface = input("Please choose sec iface: ") 
        backup_iface = input("Please choose backup iface: ") 
        choose_3_WANs = []
        choose_3_WANs.append(main_iface)
        choose_3_WANs.append(sec_iface)
        choose_3_WANs.append(backup_iface)
        return choose_3_WANs

    def setting(WANs):
        if len(WANs) == 4:
            setting_iface = dict(main_iface=WANs[0] ,sec_iface=WANs[1],backup_iface= WANs[2],forth_iface= WANs[3])
        elif len(WANs) == 3:
            setting_iface = dict(main_iface=WANs[0] ,sec_iface=WANs[1],backup_iface= WANs[2])
        elif len(WANs) == 2:
            setting_iface = dict(main_iface=WANs[0] ,sec_iface=WANs[1])
        elif len(WANs) == 1:
            setting_iface = dict(main_iface=WANs[0])
        elif len(WANs) == 0:
            print("No any WAN can use.")
        else:
            print("Something Wrong.")
        return setting_iface

    

# class order_WANs:
#     def WANs_order(WANs): 
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
    if input_json['function'] == 'supported':
        output_json = {}
        try:
            output_json["ifaces"] = []
            all_WANs = find_WANs.find_interface()
            ip_WANs = find_WANs.if_has_IP(all_WANs)
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

    else:
        all_WANs = find_WANs.find_interface()
        ip_WANs = find_WANs.if_has_IP(all_WANs)
        host = '8.8.8.8'
        can_use_WANs = find_WANs.if_ping_8888(host, ip_WANs)
        # three_can_use_WANs = choose_WANs.choose_3_WANs(can_use_WANs)
        setting_iface = choose_WANs.setting(can_use_WANs)
