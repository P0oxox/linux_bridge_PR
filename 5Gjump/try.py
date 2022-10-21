import os
import sys
import time
import json
from json import load
import sys
import logging
import subprocess 
from ping3 import ping, verbose_ping

def kill():
    nat = subprocess.getoutput("iptables -t nat -v -L POSTROUTING -n --line-number")
    # print(type(nat))
    while True:
        if "enp0s10" in nat:
            os.system('iptables -t nat -D POSTROUTING -s 192.168.0.0/24 -o enp0s10 -j MASQUERADE')
        break


if __name__ == '__main__':
    kill()

   
