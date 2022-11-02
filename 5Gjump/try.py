import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping
def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

def str_to_json(json_str_file):
    json_fomat = json.loads(json_str_file)
    return json_fomat


def setting():
    if_info = sys.argv[1]
    str_2_dic = json.loads(if_info)

    # print(str_2_dic['mode'])

    output_json1 = {"mode":str_2_dic["mode"],"ping_target":str_2_dic["ping_target"]}
    print('前面 output_json1')
    print(output_json1)
    output_json2 = {}
    if str_2_dic["mode"]=="fo":    
        output_json2["fo"] = {"failback": str_2_dic["failback"],"main_iface":str_2_dic["main_iface"],"sec_iface":str_2_dic["sec_iface"],"backup_iface":str_2_dic["backup_iface"],"detection_mode":str_2_dic["detection_mode"] }
        output_json2["fo"]["latency"] = {"threshold":str_2_dic["latency"]["threshold"],"detection_period":str_2_dic["latency"]["detection_period"]}   
     
    # print('output_json2')
    # print(output_json2)   
    output_json3 = {}
    if str_2_dic["mode"]=="single":  
        output_json3["single"] = {"main_iface": str_2_dic["main_wan"]}
    # print('output_json3')
    # print(output_json3)      
    output_json1.update(output_json2)
    output_json1.update(output_json3)
    print('後面 output_json1')
    print(output_json1)
    return output_json1


if __name__ == '__main__':
    # if input_json['function'] == 'setting': 
    setting()
    jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/current_config.json','r')
    b = json.load(jsonFile)
    output_json = {}
    output_setting = {}
    # try:
    output_json = setting()
        # output_json1 = {"mode":str_2_dic["mode"],"ping_target":str_2_dic["ping_target"]}
    b['mode'] = output_json['mode']
    b['ping_target'] = output_json['ping_target']

    if output_json["mode"] == 'fo':
        b['fo']["main_iface"] = output_json['fo']['main_iface']
        b['fo']["sec_iface"] = output_json['fo']['sec_iface']
        b['fo']["backup_iface"] = output_json['fo']['backup_iface']
        b['fo']["detection_mode"] = output_json['fo']['detection_mode']
        b['fo']["latency"]['threshold'] = output_json['fo']['latency']['threshold']
        b['fo']["latency"]['detection_period'] = output_json['fo']['latency']['detection_period'] 
    if output_json["mode"] == 'single':
        b['single']["main_iface"] = output_json['single']['main_iface']

    output_setting['status'] = True
    # except:
    #     error_msg = "Setting is wrong"
    #     output_setting['status'] = False
    #     output_setting['err_message'] = error_msg
    sys.stdout.write(json_to_str(output_setting))
    sys.stdout.flush()

    with open("current_config.json", "w") as f:
        f.write(json.dumps(b))
    with open("setting.json", "w") as f:
        f.write(json.dumps(output_setting))
















# def kill():
#     nat = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
#     # print(type(nat))
#     while True:
#         if "enp0s10" in nat:
#             os.system('iptables -t nat -D POSTROUTING -s 192.168.0.0/24 -o enp0s10 -j MASQUERADE')
#         break


# if __name__ == '__main__':
#     kill()

   
