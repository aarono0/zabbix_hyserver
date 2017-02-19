#!/bin/sh

Disk_io_discovery() {
    disk_name=`iostat | grep -v ^$ |grep -v ^[Linux\|Device\|avg\|' '] |awk '{print $1}'`
    COUNT=`echo "$disk_name" |wc -l`
    INDEX=0
    echo {'"data"':[
        echo "$disk_name" | while read LINE;
            do
                    echo -n '{"{#DISKNAME}":"'$LINE'"}'
                    INDEX=`expr $INDEX + 1`
                    if [ $INDEX -lt $COUNT ]; then
                        echo ","
                    fi
            done
        echo ]}
}

Disk_io_status() {
    if [ $mode = "read" ]
    then
        iostat -x -k 1 1  |grep $disk |awk '{print $6}'
    elif [ $mode = 'write' ]
    then
        iostat -x -k 1 1  |grep $disk |awk '{print $7}'
    fi
}

if [ $# -ne 2 ]
then
    Disk_io_discovery
else
    mode=$1
    disk=$2
    Disk_io_status
fi
