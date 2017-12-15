#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : yanghaiying
# Email   : yhai_ying@163.com
# File    : uwsgi_status_mon.py
# Describe: uwsgi status monitor

import os
import sys
import json
import time
import getopt
import commands

class monitor_uwsgi:
    def __init__(self):
        self.uwsgi = "/usr/local/sinasrv5/bin/uwsgi"
        self.sockdir = "/var/run/uwsgi"
        self.uwsgiconf="/usr/local/sinasrv5/etc/uwsgi.d"

    def usages(self):
        print "usages: python uwsgi_status_mon.py -p [pool name] -s [status name] -m [module name]"

    def get_mon_info(self,dpool):
        command='%s --connect-and-read %s/%s 2>&1' % (self.uwsgi,self.sockdir,dpool)
        get_info = commands.getstatusoutput(command)
        if get_info[0] == 0:
            return get_info[1]

    def memory_mon(self,info,status):
        sum1 = 0
        for i in info['workers']:
            sum1 += i[status]
        print sum1 / 1024 / 1024

    def process_use(self,info,status):
        sum1 = 0
        sum2 = 0
        for i in info['workers']:
        print sum1

    def avg_rt_time(self,info,status):
        sum1 = 0
        sum2 = 0
        for i in info['workers']:
            sum1 += i[status]
            sum2 += 1
        print sum1/sum2

    def cores_rw(self,info,status):
        sum1 = 0
        for i in info['workers']:
            tmp = i['cores']
            for j in tmp:
                sum1 += j[status]
        print sum1

    def apps_exception(self,info,status):
        sum1 = 0
        for i in info['workers']:
            tmp = i['apps']
            for j in tmp:
                sum1 += j[status]
        print sum1

    def all_requests(self,info,status):
        sum1 = 0
        for i in info['workers']:
            sum1 += i[status]
        print sum1


    def status_info(self,info,module,status):
        if module == 'memory':
            self.memory_mon(info,status)
        elif module == 'process':
            self.process_use(info,status)
        elif module == 'time':
            self.avg_rt_time(info,status)
        elif module == 'error':
            self.cores_rw(info,status)
        elif module == 'process_requsts':
            self.all_requests(info,status)
        elif module == 'process_num':
            self.process_num(info,status)

    def branch_pool(self,dpool_sock,module,status):
        getinfo = self.get_mon_info(dpool_sock)
        info = json.loads(getinfo)
        self.status_info(info,module,status)

    def pool_sock(self):
        list1 = os.listdir(self.uwsgiconf)
        list2 = []
        for i in list1:
            j = i.split('.conf')[0]
            list2.append(j.split('-')[1])
        return list2

    def analysis_parameter(self,Pool,module,status):
        dpool_sock = 'hyserver.com.cn-' + Pool + '-m.sock'
        self.branch_pool(dpool_sock,module,status)


def main():
    if len(sys.argv) == 1:
        list1 = monitor_uwsgi().pool_sock()
        uwsgi_pool = []
        for i in list1:
            if i:
                uwsgi_pool.append({"{#USWGINAME}": i})
        print json.dumps({'data': uwsgi_pool}, sort_keys=True, indent=7,separators=(',',':'))

    else:
        opts, args = getopt.getopt(sys.argv[1:], "hp:s:m:", ["help", "poolname=", "statusname=", "module="])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                monitor_uwsgi().usages()
                sys.exit()
            if opt in ('-p', '--poolname'):
                Pool = arg
            if opt in ('-s', '--statusname'):
                status = arg
            if opt in ('-m', '--module'):
                module = arg

        monitor_uwsgi().analysis_parameter(Pool,module,status)


if __name__ == '__main__':
    main()
