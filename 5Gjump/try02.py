import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping
ifaces = ['enp0s3','enp0s8','enp0s9','enp0s10']


ifmetric_show = subprocess.getoutput("route -n")
line_list = ifmetric_show.split('\n')
print(line_list[2])
if "enp0s10" in line_list[2]:
    print(1)
else:
    print(0)
# print(ifmetric_show[3][0:10])

# print(ifmetric_show[2].split()[2])