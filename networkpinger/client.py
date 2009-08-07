from networkpinger.config import read_config
import httplib2
from urllib import urlencode
import os

import simplejson

class Client:
    def __init__(self, client_ini_path):
        cfg = read_config(client_ini_path)
        self.h = cfg['host']

        h = httplib2.Http(os.path.expanduser("~/.httplib2_cache"))
        h.add_credentials(cfg['username'], cfg['password'])
        self.http = h
    
    def do(self, page, **kwargs):
        url = "%s/%s" % (self.h, page)
        data = None
        if kwargs:
            data = urlencode(kwargs)
            resp, content = self.http.request(url, 'POST', data)
        else:
            resp, content = self.http.request(url)
        return content

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

    def add_host(self, addr, name):
        return self.do("add_host", addr=addr, name=name)
