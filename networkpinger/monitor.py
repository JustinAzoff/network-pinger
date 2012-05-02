#!/usr/bin/env python
from networkpinger import client
import ping_wrapper

import sys
import time
import os
from subprocess import Popen
import json
import threading

RUNNING=True

SUDO=True

def run_scripts(status, hosts):
    ALERTS = json.dumps(list(hosts))
    script_dir = "./script.d"
    for f in os.listdir(script_dir):
        fn = os.path.join(script_dir, f)
        if os.access(fn, os.X_OK):
            os.putenv("ALERTS", ALERTS)
            p = Popen([fn, status])#, env={"ALERTS": ALERTS})
            os.waitpid(p.pid, 0)[1]

def log(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def monitor_up(c=None):
    pinger = ping_wrapper.get_backend(use_sudo=SUDO)
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

    for ip in down:
        c.set_down(ip)

    if down:
        log('upmon up:%d down:%d' % (len(ips) - len(down), len(down)))
        run_scripts("down", down)
    return len(down)

def monitor_down(c=None):
    pinger = ping_wrapper.get_backend(use_sudo=SUDO)
    if not c:
        c = client.Client('localhost:8888')
    ips = c.get_down_addrs()
    if not ips:
        return
    up, down = pinger.ping_many_updown(ips)
    for ip in up:
        c.set_up(ip)
    if up:
        log('downmon up:%d down:%d' % (len(up), len(down)))
        run_scripts("up", up)
    return len(up)

def maybe_sleep(seconds):
    """Sleep for `seconds` while keeping track if we should be exiting or not"""
    global RUNNING
    for x in range(seconds*10):
        if not RUNNING:
            return
        time.sleep(.1)

def down_loop():
    global RUNNING
    c = client.Client('localhost:8888')
    time.sleep(0.5)
    print "starting down loop"
    while RUNNING:
        up = monitor_down(c)
        if not up:
            maybe_sleep(2)

def up_loop():
    global RUNNING
    c = client.Client('localhost:8888')
    print "starting up loop"
    while RUNNING:
        down = monitor_up(c)
        if not down:
            maybe_sleep(10)

def main():
    global RUNNING
    u = threading.Thread(target=up_loop,name="up-monitor")
    d = threading.Thread(target=down_loop,name="down-monitor")
    try :
        u.start()
        d.start()
        #exit if either of the threads crashes.
        while u.isAlive() and d.isAlive():
            u.join(1)
            d.join(1)
    except KeyboardInterrupt:
        pass
    print "Exiting.."
    RUNNING=False
    sys.exit(1)

if __name__ == "__main__":
    main()
