#!/usr/bin/env python
import sys
import stomp
import simplejson
def send(up=None,down=None):
    queue = '/topic/alert_msgs'
    conn = stomp.Stomp('localhost',61613)
    data = {'up': up, 'down': down, 'who':'backend'}
    msg = simplejson.dumps(data)

    conn.connect()
    conn.send(dict(body=msg, destination=queue))
    conn.disconnect()


if __name__ == "__main__":
    import sys, time
    send(sys.argv[1], sys.argv[2])
