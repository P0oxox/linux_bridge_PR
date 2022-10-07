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
    en_to_eth["enp0s3"] = "Mobile Network"
    en_to_eth["enp0s8"] = "Wi-Fi"
    en_to_eth["enp0s9"] = "NR"
    en_to_eth["enp0s10"] = "LTE"  #隨便亂取的
    # eth_to_en["Mobile Network"] = "enp0s3"
    # eth_to_en["Wi-Fi"] = "enp0s8"
    # eth_to_en["NR"] = "enp0s9"
    # eth_to_en["LTE"] = "enp0s10" 
    return en_to_eth,eth_to_en
    
def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

def str_to_json(json_str_file):
    json_fomat = json.loads(json_str_file)
    return json_fomat

               
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


if __name__ == '__main__':
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, filename='/var/log/failover.log', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    input_json = str_to_json(sys.argv[1])
    ##
    # 全域變數???
    all_WANs = find_WANs.find_interface()
    ip_WANs = find_WANs.if_has_IP(all_WANs)
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


# python3 try_white.py '{"function":"supported"}'