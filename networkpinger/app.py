#!/usr/bin/env python
import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode

from tornado.options import define, options

from tornad_io import SocketIOHandler
from tornad_io import SocketIOServer

from webhelpers.date import time_ago_in_words, distance_of_time_in_words

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

import logging
logger = logging.getLogger()

cache_opts = {
    'cache.type': 'memory'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
mycache = cache.get_cache('alerts', type='memory', expiretime=10)


from networkpinger import model

def get_down():
    f = model.Alert.query_down().all
    return mycache.get_value(key='down', createfunc=f)

def get_up():
    f = model.Alert.query_recent_up
    return mycache.get_value(key='up', createfunc=f)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class AlertsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("alerts/index.html")

class AlertsDownHandler(tornado.web.RequestHandler):
    def get(self):
        down = get_down()
        self.render("alerts/down.html", down=down, time_ago_in_words=time_ago_in_words)

class AlertsUpHandler(tornado.web.RequestHandler):
    def get(self):
        up = get_up()
        self.render("alerts/up.html", up=up, distance_of_time_in_words=distance_of_time_in_words)

class AlertsDownJsonHandler(tornado.web.RequestHandler):
    def get(self):
        down = get_down()
        self.finish(json_encode({'down': [c.to_dict() for c in down]}))

class AlertsUpJsonHandler(tornado.web.RequestHandler):
    def get(self):
        up = get_up()
        self.finish(json_encode({'up': [c.to_dict() for c in up]}))

class AlertsSetDownHandler(tornado.web.RequestHandler):
    def post(self):
        addr = self.get_argument("addr")
        h = model.Host.get_by_addr(addr)
        a = h.add_alert()
        logger.info("pinger addr=%s state=down" % addr)
        msg = json_encode({'down': a.to_dict()})
        self.finish(msg)

        mycache.remove_value("down")
        broadcast(msg)

class AlertsSetUpHandler(tornado.web.RequestHandler):
    def post(self):
        addr = self.get_argument("addr")
        a = model.Alert.query_down().filter_by(addr=addr).first()
        if not a:
            return self.finish(json_encode({'alert': None}))
        a.up = True
        model.Session.commit()
        logger.info("pinger addr=%s state=up" % addr)
        msg = json_encode({'up': a.to_dict()})
        self.finish(msg)

        mycache.remove_value("down")
        mycache.remove_value("up")
        broadcast(msg)

class AlertsUpAddrsJson(tornado.web.RequestHandler):
    def get(self):
        self.finish(json_encode({'addrs': [a for a in model.Host.get_up_addresses()]}))

class AlertsDownAddrsJson(tornado.web.RequestHandler):
    def get(self):
        self.finish(json_encode({'addrs': [a.addr for a in get_down()]}))

participants = set()

def broadcast(msg):
    for p in participants:
        p.send(msg)

class Realtimehandler(SocketIOHandler):
    """Socket.IO handler"""

    def on_open(self, *args, **kwargs):
        self.send("Welcome!")
        participants.add(self)
        logger.info("new participant")

    #def on_message(self, message):
    #    for p in participants:
    #        p.send(message)

    def on_close(self):
        participants.remove(self)

realtimeRoute = Realtimehandler.routes("socket.io/*")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/alerts", AlertsHandler),
            (r"/alerts/down", AlertsDownHandler),
            (r"/alerts/up",   AlertsUpHandler),

            (r"/alerts/down.json", AlertsDownJsonHandler),
            (r"/alerts/up.json", AlertsUpJsonHandler),

            (r"/alerts/set_up", AlertsSetUpHandler),
            (r"/alerts/set_down", AlertsSetDownHandler),

            (r"/alerts/up_addrs.json", AlertsUpAddrsJson),
            (r"/alerts/down_addrs.json", AlertsDownAddrsJson),

            realtimeRoute,
        ]
        settings = dict(
            page_title=u"Alerts",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            #xsrf_cookies=True,
            #cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            enabled_protocols = ['websocket', 'xhr-multipart', 'xhr-polling'],
            socket_io_port = 8888,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        #self.db = tornado.database.Connection(
        #    host=options.mysql_host, database=options.mysql_database,
        #    user=options.mysql_user, password=options.mysql_password)

define("port", default=8888, help="run on the given port", type=int)
define("config", default="devel.ini", help="Config file")
define("setup", default=False, help="perform application setup", type=bool)

def main():
    tornado.options.parse_command_line()

    model.configure(os.path.abspath(options.config))

    if options.setup:
        from networkpinger import websetup
        websetup.setup_app()
        sys.exit(0)
    
    application = Application()
    socketio_server = SocketIOServer(application)


if __name__ == "__main__":
    main()
