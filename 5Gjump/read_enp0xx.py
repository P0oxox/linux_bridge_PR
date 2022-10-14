import subprocess 

'''
把 ifconfig 拆成 ifconfig enp0s3、ifconfig enp0s8、ifconfig enp0s9......
'''
# def parse_ifconfig_data(data):
#     parsed_data = []
#     new_line = ''
#     data = [i for i in data.split('\n') if i]

#     for line in data:
#         if not line.startswith(' '):
#             parsed_data.append(new_line)
#             new_line = line + '\n'
#         else:
#             new_line += line + '\n'
#     parsed_data.append(new_line)
#     return   parsed_data[1:]
'''
取 ifconfig enp0s3 的資料
'''
def parse_one_interface(one_data):
    result = {}
    line_list = if_info.split('\n')
    result["device_name"] = line_list[0].split()[0]
    result["inet_addr"] = line_list[1].split()[1]
    result["netmask"] = line_list[1].split()[3]
    result["mac address"] = line_list[3].split()[1]
    # result["inet_addr"] = line_list[1].split()[1].split(':')[1]
    # result["MTU"] = line_list[3].split()[-2].split(':')[-1]
    return result

if  __name__ == "__main__":
    ifaces = ['enp0s3', 'enp0s8', 'enp0s9', 'enp0s10']
    if_info = subprocess.getoutput("ifconfig "+ ifaces[0])
    print(parse_one_interface(if_info))
    



###
# 參考：
# https://blog.csdn.net/hjxzb/article/details/79890749
###

