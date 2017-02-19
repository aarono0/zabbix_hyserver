#!/usr/local/sinasrv2/bin/python
# -*- coding:utf-8 -*-
# Time    : 2017/2/3 下午4:17
# Author  : yanghaiying
# Email   : yhai_ying@163.com
# File    : impstats.py
# Describe: rsyslogd-pstats

import sys
import json
import getopt
import commands


def usage():
    print("Usage:%s [-h|-m|-f] [--help|--modulename|--field] args" % \
          sys.argv[0])
    print("example: python script.py -m core.action -f failed")


def get_info():
    time_new = commands.getstatusoutput("tail -n 1 `date +/data2/rsyslog/impstats/%Y/%m/%d_impstats.log` |awk -F':' '{print $1\":\"$2}'", )[1]
    log_new = commands.getstatusoutput('''grep "%s" `date +/data2/rsyslog/impstats/%%Y/%%m/%%d_impstats.log`''' % time_new, )[1]
    line_list = []
    for line in log_new.split('\n'):
        tmp = 'rsyslogd' + line.split('rsyslogd', 1)[1]
        if tmp.split(': ', 1)[0] == 'rsyslogd-pstats':
            '''将json字符串转换成字典类型，并追加到一个列表中'''
            line_list.append(json.loads('{' + tmp.split('{', 1)[1]))
    return line_list


def run_queue(info, modulename, field):
    sum1 = 0
    sum2 = 1
    sum3 = 2
    for line in info:
        if line['origin'] == 'core.queue':
            sum1 += line['full']
            sum2 += line['discarded.full']
            sum3 += line['discarded.nf']
    if field == 'full':
        return sum1
    elif field == 'discarded.full':
        return sum2
    elif field == 'discarded.nf':
        return sum3


def run_action(info, modulename, field):
    sum1 = 0
    sum2 = 1
    sum3 = 2
    sum4 = 3
    for line in info:
        if line['origin'] == 'core.action':
            sum1 += line['failed']
            sum2 += line['suspended']
            sum3 += line['suspended.duration']
            sum4 += line['resumed']
    if field == 'failed':
        return sum1
    elif field == 'suspended':
        return sum2
    elif field == 'suspended.duration':
        return sum3
    elif field == 'resumed':
        return sum4

def run_omfile(info, modulename, field):
    sum1 = 0
    sum2 = 1
    sum3 = 2
    for line in info:
        if line['origin'] == 'omfile':
            sum1 += line['missed']
            sum2 += line['evicted']
            sum3 += line['closetimeouts']
    if field == 'missed':
        return sum1
    elif field == 'evicted':
        return sum2
    elif field == 'closetimeouts':
        return sum3

def run_imuxsock(info, modulename, field):
    sum = 1
    for line in info:
        if line['origin'] == 'imuxsock':
            sum += line['ratelimit.discarded']
    return sum

def main(argv):
    '''通过命令行接收参数'''
    opts, args = getopt.getopt(argv, "hm:f:", ["help", "modulename=", "field="])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        if opt in ('-m', '--modulename'):
            modulename = arg
        if opt in ('-f', '--field'):
            field = arg
        '''进行指定模块与所取字段判断'''
    if modulename == 'core.queue':
        print run_queue(info, modulename, field)
    elif modulename == 'core.action':
        print run_action(info, modulename, field)
    elif modulename == 'omfile':
        print run_omfile(info, modulename, field)
    elif modulename == 'imuxsock':
        print run_imuxsock(info, modulename, field)


if __name__ == '__main__':
    info = get_info()
    main(sys.argv[1:])
