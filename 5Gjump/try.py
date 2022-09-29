import os
import time
import socket

iface = ["enp0s3","enp0s8","enp0s9","enp0s10"]
class find_WANs:
#     def find_interface():
#         interface_list = socket.if_nameindex()
#         i_list = []
#         for i in interface_list:
#             i_list.append(i[1])  #這是所有的 interface，包括 br0 跟 lo
#         WANs = []
#         for i in i_list:
#             if 'enp' in i:
#                 WANs.append(i)  # 這是只有 enp0sxxx 的 interface
#         return WANs

    def if_has_IP(WANs):   
        all_WANs = []
        has_IP_WANs = []
        for i in range(len(WANs)):
            all_WANs.append(os.system('ip -4 addr show {0} | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\'  >/dev/null 2>&1'.format(WANs[i],'1','2','{3}' )))
            if (all_WANs[i] == 256) : 
                print("{} has no ip.".format(WANs[i]))
            else:
                # print("{} has ip.".format(WANs[i]))  
                has_IP_WANs.append(WANs[i])
        print('這些是有 ip 的 WAN', has_IP_WANs)
        return has_IP_WANs




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

# class order_WANs:       

# class Active:
#     def __init__(self):
#         # self.ifmetric = ifmetric  
#         # self.NAT_rule = NAT_rule  
#     def ifmetric(self):
#         os.system('ifmetric {} 2'.format(WANs["main iface"]))
#         os.system('ifmetric {} 4'.format(WANs["sec iface"]))
#         os.system('ifmetric {} 6'.format(WANs["backup iface"]))
#     # def NAT_rule(self):



# mazda = Cars("blue", 4)
# mazda.drive()





if __name__ == '__main__':
    # all_WANs = find_WANs.find_interface()
    ip_WANs = find_WANs.if_has_IP(iface)
    host = '8.8.8.8'
    # can_use_WANs = find_WANs.if_ping_8888(host, ip_WANs)
    # three_can_use_WANs = choose_WANs.choose_3_WANs(can_use_WANs)
    # setting_iface = choose_WANs.setting(can_use_WANs)
    # print(setting_iface)
    # choose_WANs.WANs_order(setting_iface)


    # choose_3_WANs = choose_WANs.choose_3_WANs(ip_WANs)
    choose_3_WANs = {'main iface': ['enp0s3'], 'sec iface': ['enp0s8'], 'backup iface': ['enp0s10']}

    print(choose_3_WANs['main iface'])











