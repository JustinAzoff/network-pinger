import urllib, urllib2
import simplejson

class Client:
    def __init__(self, host):
        self.h = host
        #authinfo = urllib2.HTTPBasicAuthHandler()
        #authinfo.add_password("Cisco Controller", host, user, password)
        #opener = urllib2.build_opener(authinfo)
        #urllib2.install_opener(opener)
    
    def do(self, page, **kwargs):
        url = "http://%s/%s" % (self.h, page)
        data = None
        if kwargs:
            data = urllib.urlencode(kwargs)
        return urllib2.urlopen(url, data).read()

    def do_json(self, page, **kwargs):
        return simplejson.loads(self.do(page, **kwargs))

    def get_up_addrs(self):
        return self.do_json("alerts/up_addrs_json")['addrs']
    def get_down_addrs(self):
        return self.do_json("alerts/down_addrs_json")['addrs']

    def set_down(self, addr):
        return self.do_json("alerts/set_down", addr=addr)['alert']

    def set_up(self, addr):
        return self.do_json("alerts/set_up", addr=addr)['alert']

    def get_down(self):
        return self.do_json("alerts/down_json")['down']

    def get_up(self):
        return self.do_json("alerts/up_json")['up']

    def set_ok(self, alert_id):
        return self.do_json("alerts/set_ok", id=alert_id,ok=True)
    
    def set_bad(self, alert_id):
        return self.do_json("alerts/set_ok", id=alert_id)

    def set_reason(self, alert_id, reason):
        return self.do_json("alerts/set_reason", id=alert_id, reason=reason)
