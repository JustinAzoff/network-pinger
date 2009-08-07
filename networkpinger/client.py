from networkpinger.config import read_config
import urllib, urllib2
import simplejson

class Client:
    def __init__(self, client_ini_path):
        cfg = read_config(client_ini_path)
        self.h = cfg['host']
        authinfo = urllib2.HTTPBasicAuthHandler()
        authinfo.add_password("Alerts", self.h, cfg['username'], cfg['password'])
        opener = urllib2.build_opener(authinfo)
        urllib2.install_opener(opener)
    
    def do(self, page, **kwargs):
        url = "%s/%s" % (self.h, page)
        data = None
        if kwargs:
            data = urllib.urlencode(kwargs)
        return urllib2.urlopen(url, data).read()

    def do_json(self, page, **kwargs):
        return simplejson.loads(self.do(page, **kwargs))

    def get_up_addrs(self):
        return self.do_json("up_addrs_json")['addrs']
    def get_down_addrs(self):
        return self.do_json("down_addrs_json")['addrs']

    def set_down(self, addr):
        return self.do_json("set_down", addr=addr)['alert']

    def set_up(self, addr):
        return self.do_json("set_up", addr=addr)['alert']

    def get_down(self):
        return self.do_json("down_json")['down']

    def get_up(self):
        return self.do_json("up_json")['up']

    def update(self, alert_id, **kwargs):
        return self.do_json("update/%d" % alert_id, **kwargs)
    
    def set_ok(self, alert_id):
        return self.update(alert_id, ok='true')
    def set_bad(self, alert_id):
        return self.update(alert_id, ok='false')
    def set_reason(self, alert_id, reason):
        return self.update(alert_id, reason=reason)

    def set_note(self, alert_id, short, long):
        return self.update(alert_id, note_short=short, note_long=long)
