#!/usr/bin/python
# <variable> = required
# [variable] = optional
# Usage ./canbus-stress-test.py <timeout> <device>

import sys
import subprocess
import time


def canstats():
    cmd = 'cat /proc/net/can/stats'
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "ERROR!"
        print e
        exit(1)


def cansequence(device):
    cmd = 'cansequence -e -p > /dev/null &'
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "ERROR!"
        print e
        exit(1)


def canbus_dump(device):
    cmd = 'candump can0 > ~/tmp/log.txt &'
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "ERROR!"
        print e
        exit(1)


def umount_device(device):
    cmd = 'umount -f %s' % device
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "ERROR!"
        print e
        exit(1)


def mount_device(device):
    cmds = ['mkdir -p ~/tmp', 'mkfs -F -t ext4 %s' % device, 'mount %s ~/tmp/' % device]
    try:
        for cmd in cmds:
            subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "ERROR!"
        print e
        exit(1)


def main(timeout, device):
    run = True
    stop = time.time() + float(timeout)
    mount_device(device)
    canbus_dump(device)
    cansequence(device)
    while run:
        if stop <= time.time():
            run = False
            print "Test finished!"
        else:
            canstats()
            time.sleep(60)
    exit(0)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])