#!/usr/bin/env python
import sys
import stomp
import simplejson
def send(msg):
    queue = '/topic/alert_msgs'
    conn = stomp.Stomp('localhost',61613)
    data = {'body': msg, 'who':'test'}
    msg = simplejson.dumps(data)

    conn.connect()
    conn.send(dict(body=msg, destination=queue))
    conn.disconnect()

def wakeup():
    send("")

if __name__ == "__main__":
    import sys, time
    send(sys.argv[1], sys.argv[2])
