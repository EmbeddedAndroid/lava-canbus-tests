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
        output = subprocess.check_output(cmd, shell=True)
        print (time.strftime("%H:%M:%S"))
        print output
    except subprocess.CalledProcessError as e:
        print "Test error!"
        print e
        exit(1)


def umount_device(device):
    cmd = 'umount -f %s' % device
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "Test error!"
        print e
        exit(1)


def mount_device(device):
    cmds = ['mkdir -p ~/tmp', 'mkfs -F -t ext4 %s' % device, 'mount %s ~/tmp/' % device]
    try:
        for cmd in cmds:
            subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print "Test error!"
        print e
        exit(1)


def main(timeout, device):
    run = True
    stop = time.time() + float(timeout)
    mount_device(device)
    commands = ['candump can0 > ~/tmp/log.txt', 'cansequence -e -p > /dev/null']
    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
    while run:
        if stop <= time.time():
            run = False
            for p in processes:
                p.kill()
            umount_device(device)
            print "Test finished!"
        else:
            time.sleep(60)
            canstats()
    exit(0)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])