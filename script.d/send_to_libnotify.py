#!/usr/bin/env python
import simplejson
import os
import sys

import pygtk
pygtk.require('2.0')
import pynotify

if not pynotify.init("Network Pinger"):
    sys.exit(1)


d =  os.getenv("ALERTS")
alerts = simplejson.loads(d)

hosts = ' '.join(alerts)
num_hosts = len(alerts)

status =  sys.argv[1]

msg="Hosts are %s - %d - %s" % (status, num_hosts, hosts)
n = pynotify.Notification(msg)
n.update("Alerts", msg)
n.set_hint("x", 1050)
n.set_hint("y", 880)
n.show()
