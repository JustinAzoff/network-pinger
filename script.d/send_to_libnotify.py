#!/usr/bin/env python
import json
import subprocess
import os
import sys

d =  os.getenv("ALERTS")
alerts = json.loads(d)

hosts = ' '.join(alerts)
num_hosts = len(alerts)

status =  sys.argv[1]

msg="Hosts are %s - %d - %s" % (status, num_hosts, hosts)
subprocess.call(["notify-send", "Alerts", msg])
