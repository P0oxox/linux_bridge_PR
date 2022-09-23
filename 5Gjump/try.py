import os
import time
import socket
from ping3 import ping, verbose_ping


# 1. 先找全部的 WAN                    find_interface()
# 2. 篩選出跟 NetworkManager 有連接的   (不會寫)
# 3. 再篩選出有 IP 的                   if_has_IP()
# 4. 最後再用 ping3 檢查是否可通外網     if_ping_8888()
class find_WANs:
    def find_interface():
        interface_list = socket.if_nameindex()
        i_list = []
        for i in interface_list:
            i_list.append(i[1])  #這是所有的 interface，包括 br0 跟 lo
        WANs = []
        for i in i_list:
            if 'enp' in i:
                WANs.append(i)  # 這是只有 enp0sxxx 的 interface
        return WANs

    def if_has_IP(WANs):   
        all_WANs = []
        has_IP_WANs = []
        for i in range(len(WANs)):
            all_WANs.append(os.system('ip -4 addr show {0} | grep -oP \'(?<=inet\s)\d+(\.\d+){3}\' '.format(WANs[i],'1','2','{3}')))
            if (all_WANs[i] == 256) : 
                print("{} has no ip.".format(WANs[i]))
            else:
                # print("{} has ip.".format(WANs[i]))
                has_IP_WANs.append(WANs[i])
        print('這些是有 ip 的 WAN', has_IP_WANs)
        return has_IP_WANs
    
    # 剩下的 interface 用 ping3 來檢查是否可用
    def if_ping_8888(host, interface=None):   
        can_use_WANs = []
        for i in range(len(interface)):
            second = ping(host, interface = interface[i]) 
            if second is None:
                print(interface ,' failed!') 
            else:
                # print('ping-{}, took: {}s, use: {}'.format(host,second,interface))
                can_use_WANs.append(interface[i])
        return can_use_WANs

# 1. 選3個可用的 WAN  choose_3_WANs()
# 2. 排優先級         WANs_order()
class choose_WANs:
    # def choose_3_WANs(WANs): # main_iface、sec_iface、backup_iface
    #     for i in range(len(WANs)):
    #         return WANs[0:3]
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

    def WANs_order(WANs): 
        if len(WANs)==4:
            for i in WANs:
                if i=="main_iface":
                    print(WANs["main_iface"] + " is main iface.")
                    os.system('ifmetric {} 2'.format(WANs["main_iface"]))
                    os.system('ifmetric {} 8'.format(WANs["sec_iface"]))
                    os.system('ifmetric {} 9'.format(WANs["backup_iface"]))
                    os.system('ifmetric {} 10'.format(WANs["forth_iface"]))

                elif i=="sec_iface":
                    print(WANs[i] + " is sec iface.")

                elif i=="backup_iface":
                    print(WANs[i] + " is backup iface.")

                elif i=="forth_iface":
                    print(WANs[i] + " is forth iface.")
                else:
                    print("Something Wrong.")
        if len(WANs)==3:
            for i in WANs:
                if i=="main_iface":
                    print(WANs["main_iface"] + " is main iface.")
                    os.system('ifmetric {} 1'.format(WANs["main_iface"]))
                    os.system('ifmetric {} 5'.format(WANs["sec_iface"]))
                    os.system('ifmetric {} 7'.format(WANs["backup_iface"]))
                elif i=="sec_iface":
                    print(WANs[i] + " is sec iface.")

                elif i=="backup_iface":
                    print(WANs[i] + " is backup iface.")
                else:
                    print("Something Wrong.")





    
    # 好像4張網卡都要給優先級
    # 分4個 mode -> Active、Idle、Fail、Fourth



if __name__ == '__main__':
    all_WANs = find_WANs.find_interface()
    ip_WANs = find_WANs.if_has_IP(all_WANs)
    host = '8.8.8.8'
    can_use_WANs = find_WANs.if_ping_8888(host, ip_WANs)
    # three_can_use_WANs = choose_WANs.choose_3_WANs(can_use_WANs)
    setting_iface = choose_WANs.setting(can_use_WANs)
    print(setting_iface)
    choose_WANs.WANs_order(setting_iface)










