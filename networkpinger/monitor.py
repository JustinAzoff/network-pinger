#!/usr/bin/env python
from networkpinger import client
import ping_wrapper

import sys
import time
import os
from subprocess import Popen
import simplejson
import threading

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
    #give devices 2 chances to be up
    down = ips
    _, down = pinger.ping_many_updown(down)
    if down:
        time.sleep(3)
        _, down = pinger.ping_many_updown(down)
    if len(down):
        log('upmon up:%d down:%d' % (len(ips) - len(down), len(down)))
        run_scripts("down", down)

    for ip in down:
        c.set_down(ip)
    return len(down)

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
    return len(up)


def down_loop():
    c = client.Client('localhost:8888')
    print "starting down loop"
    while True:
        up = monitor_down(c)
        if not up:
            time.sleep(2)

def up_loop():
    c = client.Client('localhost:8888')
    print "starting up loop"
    while True:
        down = monitor_up(c)
        if not down:
            time.sleep(10)

def main():
    u = threading.Thread(target=up_loop)
    d = threading.Thread(target=down_loop)
    u.start()
    d.start()
    try :
        while u.isAlive() and d.isAlive():
            u.join(1)
            d.join(1)
    except KeyboardInterrupt:
        sys.exit(1)
    sys.exit(1)

if __name__ == "__main__":
    main()
