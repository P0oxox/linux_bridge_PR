import os
import time
import json
from json import load
import sys
import logging
import subprocess 

def json_to_str(json_file):
    json_string_format = json.dumps(
        json_file, ensure_ascii=False).encode('utf8')
    return json_string_format.decode()

class supported():
    # read Json file to find all WAN
    def find_WAN():
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/iface.json','r')
        a = json.load(jsonFile)
        all_wan = []
        for i in range(len(a["inter_face"])):
            all_wan.append(a["inter_face"][i]['value'])
        return all_wan

    def if_has_IP(WANs):
        all_WANs = []
        has_IP_WANs = []
        for i in range(len(WANs)):
            all_WANs.append(os.system('ip -4 addr show {0} | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\'  >/dev/null 2>&1'.format(WANs[i],'1','2','{3}' )))
            if (all_WANs[i] != 256) : 
                has_IP_WANs.append(WANs[i])
        return has_IP_WANs

# 1. 讀json看是 fo 還是 single mode
# 2. 產生 current_config.json(?)
class setting():
    def apply():
        jsonFile = open('/home/pp/linux_bridge_PR/5Gjump/setting_single.json','r')
        a = json.load(jsonFile)
        output_json = {}
        if a['mode'] == "fo": #啟動systemd 
            output_json["mode"] = a['mode']
            output_json["ping_target"] = a['ping_target']

            output_json["fo"] = []
            output_json["fo"].append({"failback": True})
            output_json["fo"].append({"main_iface": a['main_iface']})
            output_json["fo"].append({"sec_iface": a['sec_iface']})
            output_json["fo"].append({"backup_iface": a['backup_iface']})
            output_json["detection_mode"] = a['detection_mode']
            output_json["latency"] = a['latency']
            output_json['status'] = True

        elif a['mode'] == "single":
            output_json["single"] = []
            output_json["single"].append({"main_iface": a['main_wan']})
            output_json['status'] = True

        else:
            error_msg = "nono, something is wrong"
            output_json['status'] = False
            output_json['err_message'] = error_msg
        
        sys.stdout.write(json_to_str(output_json))
        sys.stdout.flush()
        with open("current_config.json", "w") as f:
            json.dump(json_to_str(output_json), f)     #要怎麼不覆蓋原來的檔案




if __name__ == '__main__':
    # {"function":"supported"}
    all_wan = supported.find_WAN()  # read Json file to find all WAN
    ip_wan = supported.if_has_IP(all_wan)  # find who has ip in all WAN

    setting.apply()




 




    # print(a)