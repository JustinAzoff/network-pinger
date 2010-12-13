#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

import os

from networkpinger import model
from networkpinger.model.configure import configure
configure(os.path.abspath(os.path.join(os.path.dirname(__file__), "../development.ini")))

from webhelpers.date import time_ago_in_words, distance_of_time_in_words


def get_down():
    f = model.Alert.query_down().all
    return f()

def get_up():
    f = model.Alert.query_recent_up
    return f()

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

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/alerts", AlertsHandler),
            (r"/alerts/down", AlertsDownHandler),
            (r"/alerts/up",   AlertsUpHandler),
        ]
        settings = dict(
            page_title=u"Alerts",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        #self.db = tornado.database.Connection(
        #    host=options.mysql_host, database=options.mysql_database,
        #    user=options.mysql_user, password=options.mysql_password)

define("port", default=8888, help="run on the given port", type=int)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
