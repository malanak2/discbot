import datetime
import shutil
import os
from os.path import exists
import time

log = ["ok", "not"]

if exists('./logs/latestlog.txt'):
    timestamp = int(time())
    curdattime = datetime.fromtimestamp(timestamp)
    fileName = './logs/' + str(curdattime) + ".txt"
    leng = len(fileName)
    stra = []
    for x in fileName:
        stra.append(x)
    for x in range(0, leng):
        if stra[x] == ":":
            stra[x] = "  "
    finFileName = ''.join(stra)
    os.rename('./logs/latestlog.txt', finFileName)
open("./logs/latestlog.txt", 'x')
with open("./logs/latestlog.txt", 'w') as f:
    for line in log:
        f.write(f"{line}\n")