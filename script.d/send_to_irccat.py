#!/usr/bin/env python
import simplejson

import sys
import os
from irccat import client

d =  os.getenv("ALERTS")
alerts = simplejson.loads(d)

hosts = ' '.join(alerts)
num_hosts = len(alerts)

status =  sys.argv[1]

msg="#alerts Hosts are %s - %d - %s" % (status, num_hosts, hosts)

client.irccat(msg, host='localhost', port=5000)
