#!/usr/bin/env python
from networkpinger import client
import ping_wrapper

import sys
import time
import os
from subprocess import Popen
import simplejson

def run_scripts(status, hosts):
    ALERTS = simplejson.dumps(list(hosts))
    script_dir = "./script.d"
    for f in os.listdir(script_dir):
        fn = os.path.join(script_dir, f)
        if os.access(fn, os.X_OK):
            os.putenv("ALERTS", ALERTS)
            p = Popen([fn, status])#, env={"ALERTS": ALERTS})
            sts = os.waitpid(p.pid, 0)[1]

def log(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def monitor_up(c=None):
    pinger = ping_wrapper.get_backend(use_sudo=True)
    if not c:
        c = client.Client('localhost:8888')
    ips = c.get_up_addrs()
    if not ips:
        return
    #give devices 2 changes to be up
    down = ips
    _, down = pinger.ping_many_updown(down)
    if down:
        _, down = pinger.ping_many_updown(down)
    if len(down):
        log('upmon up:%d down:%d' % (len(ips) - len(down), len(down)))
        run_scripts("down", down)

    for ip in down:
        c.set_down(ip)

def monitor_down(c=None):
    pinger = ping_wrapper.get_backend(use_sudo=True)
    if not c:
        c = client.Client('localhost:8888')
    ips = c.get_down_addrs()
    if not ips:
        return
    up, down = pinger.ping_many_updown(ips)
    if len(up):
        log('downmon up:%d down:%d' % (len(up), len(down)))
        run_scripts("up", up)
    for ip in up:
        c.set_up(ip)


def down_loop():
    c = client.Client('localhost:8888')
    while 1:
        monitor_down(c)
        time.sleep(2)

def up_loop():
    c = client.Client('localhost:8888')
    while 1:
        monitor_up(c)
        time.sleep(10)

def main():
    if sys.argv[1]=='up':
        up_loop()
    elif sys.argv[1]=='down':
        down_loop()
