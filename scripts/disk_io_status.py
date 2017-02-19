#!/usr/local/sinasrv2/bin/python
# -*- coding:utf-8 -*-
# Time    : 2017/2/16 下午4:17
# Author  : yanghaiying
# Email   : yhai_ying@163.com
# File    : disk_io_status.py
# Describe: disk devices io monitor

import os
import sys
import json
import subprocess

def disk_discovery():
    command="iostat | grep -v ^$ |grep -v ^[Linux\|Device\|avg\|' '] |awk '{print $1}'"
    popen = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    tmp = popen.stdout.read()
    list_disk= []
    for i in tmp.split('\n'):
        if i:
            list_disk.append({"{#DISKNAME}": i})
    print json.dumps({'data': list_disk}, sort_keys=True, indent=7,separators=(',',':'))

def disk_status(mode,disk):
    if mode == "read":
        os.system("iostat -x -k 1 1  |grep %s |awk '{print $6}'" % disk)
    elif mode == "write":
        os.system("iostat -x -k 1 1  |grep %s |awk '{print $7}'" % disk)

def main():
    if len(sys.argv) == 1:
        disk_discovery()
    elif len(sys.argv) == 3:
        mode = sys.argv[1]
        disk = sys.argv[2]
        disk_status(mode,disk)

if __name__ == '__main__':
    main()
