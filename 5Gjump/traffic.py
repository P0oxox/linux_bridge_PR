import os
import time
import json
from json import load
import sys
import logging
import subprocess 
import time

# dirpath = r"/sys/class/net"
# print("列出當前資料夾所有檔案和資料夾:\n",os.listdir(dirpath))
# result = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirpath, f))]
# print("In列出當前資料夾所有檔案:\n",result)

# start=time.time()
# enp0s10_rx_start = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/rx_bytes")
# enp0s10_rx_end = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/rx_bytes")
# end=time.time()
# total=end-start
# time.sleep(1-total)
# print("enp0s10 rx: "+str(int(enp0s10_rx_end)-int(enp0s10_rx_start))+"  bytes")

enp0s3_rx_start = subprocess.getoutput("cat /sys/class/net/enp0s3/statistics/rx_bytes")
enp0s3_tx_start = subprocess.getoutput("cat /sys/class/net/enp0s3/statistics/tx_bytes")
enp0s8_rx_start = subprocess.getoutput("cat /sys/class/net/enp0s8/statistics/rx_bytes")
enp0s8_tx_start = subprocess.getoutput("cat /sys/class/net/enp0s8/statistics/tx_bytes")
enp0s9_rx_start = subprocess.getoutput("cat /sys/class/net/enp0s9/statistics/rx_bytes")
enp0s9_tx_start = subprocess.getoutput("cat /sys/class/net/enp0s9/statistics/tx_bytes")
enp0s10_rx_start = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/rx_bytes")
enp0s10_tx_start = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/tx_bytes")
time.sleep(1)
enp0s3_rx_end = subprocess.getoutput("cat /sys/class/net/enp0s3/statistics/rx_bytes")
enp0s3_tx_end = subprocess.getoutput("cat /sys/class/net/enp0s3/statistics/tx_bytes")
enp0s8_rx_end = subprocess.getoutput("cat /sys/class/net/enp0s8/statistics/rx_bytes")
enp0s8_tx_end = subprocess.getoutput("cat /sys/class/net/enp0s8/statistics/tx_bytes")
enp0s9_rx_end = subprocess.getoutput("cat /sys/class/net/enp0s9/statistics/rx_bytes")
enp0s9_tx_end = subprocess.getoutput("cat /sys/class/net/enp0s9/statistics/tx_bytes")
enp0s10_rx_end = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/rx_bytes")
enp0s10_tx_end = subprocess.getoutput("cat /sys/class/net/enp0s10/statistics/tx_bytes")
print("enp0s3 rx: "+str(int(enp0s3_rx_end)-int(enp0s3_rx_start))+"  bytes")
print("enp0s3 tx: "+str(int(enp0s3_tx_end)-int(enp0s3_tx_start))+"  bytes")
print("enp0s8 rx: "+str(int(enp0s10_rx_end)-int(enp0s10_rx_start))+"  bytes")
print("enp0s8 tx: "+str(int(enp0s10_tx_end)-int(enp0s10_tx_start))+"  bytes")
print("enp0s9 rx: "+str(int(enp0s9_rx_end)-int(enp0s9_rx_start))+"  bytes")
print("enp0s9 tx: "+str(int(enp0s9_tx_end)-int(enp0s9_tx_start))+"  bytes")
print("enp0s10 rx: "+str(int(enp0s10_rx_end)-int(enp0s10_rx_start))+"  bytes")
print("enp0s10 tx: "+str(int(enp0s10_tx_end)-int(enp0s10_tx_start))+"  bytes")
