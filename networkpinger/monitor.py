#!/usr/bin/env python
from networkpinger import client
from networkpinger.lib import nmapping

import sys
import time

def log(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def monitor_up(c=None):
    if not c:
        c = client.Client('localhost:8000')
    ips = c.get_up_addrs()
    if not ips:
        return
    up, down = nmapping.pingmanyupdown(ips,use_sudo=True)
    if len(down):
        log('upmon up:%d down:%d' % (len(up), len(down)))

    for ip in down:
        c.set_down(ip)

def monitor_down(c=None):
    if not c:
        c = client.Client('localhost:8000')
    ips = c.get_down_addrs()
    if not ips:
        return
    up, down = nmapping.pingmanyupdown(ips,use_sudo=True)
    if len(up):
        log('downmon up:%d down:%d' % (len(up), len(down)))
    for ip in up:
        c.set_up(ip)


def down_loop():
    c = client.Client('localhost:8000')
    while 1:
        monitor_down(c)
        time.sleep(2)

def up_loop():
    c = client.Client('localhost:8000')
    while 1:
        monitor_up(c)
        time.sleep(10)

def main():
    if sys.argv[1]=='up':
        up_loop()
    elif sys.argv[1]=='down':
        down_loop()
