#!/usr/bin/env python
import sys
import stomp
import simplejson
def send(msg):
    queue = '/topic/alert_msgs'
    conn = stomp.Connection()
    conn.start()
    conn.connect()

    data = {'body': msg, 'who':'test'}
    msg = simplejson.dumps(data)

    conn.send(msg, destination=queue)
    #conn.disconnect()

if __name__ == "__main__":
    import sys, time
    send(sys.argv[1], sys.argv[2])
