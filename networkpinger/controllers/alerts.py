import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for
from pylons.decorators import jsonify

from networkpinger.lib.base import BaseController, render, validate

log = logging.getLogger(__name__)

from networkpinger import model

from networkpinger.model import forms
from networkpinger.lib.send import wakeup

from webhelpers.feedgenerator import Atom1Feed

from pylons import cache
mycache = cache.get_cache('alerts', type='memory')
def get_down():
    f = model.Alert.query_down().all
    return mycache.get_value(key='down', createfunc=f)

def get_up():
    f = model.Alert.query_recent_up
    return mycache.get_value(key='up', createfunc=f)

class AlertsController(BaseController):

    def index(self):
        return render('/alerts/index.mako')

    def down(self):
        c.down = get_down()
        return render('/alerts/down.mako')
    def up(self):
        c.up = get_up()
        return render('/alerts/up.mako')

    def addr(self, id):
        addr = id
        h = model.Host.get_by_addr(addr)
        c.host = h
        c.alerts = h.alerts.all()
        return render('/alerts/addr.mako')

    def notes(self, id):
        a = model.Session.query(model.Alert).filter_by(id=id).one()
        c.alert = a
        return render('/alerts/notes.mako')

    @jsonify
    def up_json(self):
        up = get_up()
        return {'up': [c.to_dict() for c in up]}

    @jsonify
    def down_json(self):
        down = get_down()
        return {'down': [c.to_dict() for c in down]}

    @jsonify
    def set_down(self):
        addr = request.params.get("addr")
        h = model.Host.get_by_addr(addr)
        a = h.add_alert()
        mycache.remove_value("down")
        wakeup()
        return {'alert': a.to_dict()}

    @jsonify
    def set_up(self):
        addr = request.params.get("addr")
        a = model.Alert.query_down().filter_by(addr=addr).first()
        if not a:
            return {'alert': None}

        a.up = True
        model.Session.commit()
        mycache.remove_value("down")
        mycache.remove_value("up")
        wakeup()
        return {'alert': a.to_dict()}

    @jsonify
    def up_addrs_json(self):
        return {'addrs': [a for a in model.Host.get_up_addresses()]}
    @jsonify
    def down_addrs_json(self):
        return {'addrs': [a.addr for a in get_down()]}

    @validate(schema=forms.AddNote(),form='notes', on_get=True)
    def addnote(self, id):
        a = model.Session.query(model.Alert).filter_by(id=id).one()
        short = self.form_result.get("short")
        long = self.form_result.get("long")
        a.add_note(short, long)
        model.Session.commit()

        if a.uptime:
            mycache.remove_value("up")
        else:
            mycache.remove_value("down")

        wakeup()
        redirect_to(action="index")


    def feed(self):
        alerts = model.Session.query(model.Alert)
        alerts = alerts.order_by(model.sa.desc(model.Alert.time)).limit(100)
        f = Atom1Feed(
            title = "Alerts",
            link=url_for(),
            description="Alerts",
        )
        for a in alerts:
            f.add_item(
                title="%s - %s" %(a.addr, a.name),
                link=url_for(controller="alerts",action="notes",id=a.id),
                description="Down at %s\nUp at %s" % (a.time,a.uptime),
                pubdate = a.time,
            )
        response.content_type = 'application/atom+xml'
        return f.writeString('utf-8')

    def clear_caches(self):
        mycache.remove_value("down")
        mycache.remove_value("up")
        wakeup()
        return "ok"
