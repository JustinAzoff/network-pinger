import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for
from pylons.decorators import jsonify

from networkpinger.lib.base import BaseController, render, validate

log = logging.getLogger(__name__)

from networkpinger import model

from networkpinger.model import forms

from webhelpers.feedgenerator import Atom1Feed

from pylons import cache
from pylons.decorators.cache import beaker_cache

from repoze.what.predicates import has_permission
from repoze.what.plugins.pylonshq import ActionProtector

mycache = cache.get_cache('alerts', type='memory', expiretime=10)
def get_down():
    f = model.Alert.query_down().all
    return mycache.get_value(key='down', createfunc=f)

def get_up():
    f = model.Alert.query_recent_up
    return mycache.get_value(key='up', createfunc=f)

class AlertsController(BaseController):

    @beaker_cache(expire=600, type="memory")
    @ActionProtector(has_permission('see-alerts'))
    def index(self):
        return render('/alerts/index.mako')

    @ActionProtector(has_permission('see-alerts'))
    def down(self):
        c.down = get_down()
        return render('/alerts/down.mako')
    @ActionProtector(has_permission('see-alerts'))
    def up(self):
        c.up = get_up()
        return render('/alerts/up.mako')

    @ActionProtector(has_permission('see-alerts'))
    def addr(self, id):
        addr = id
        h = model.Host.get_by_addr(addr)
        c.host = h
        c.alerts = h.alerts.all()
        return render('/alerts/addr.mako')

    @ActionProtector(has_permission('see-alerts'))
    def notes(self, id):
        c.alert = model.Session.query(model.Alert).get(id)
        return render('/alerts/notes.mako')

    @jsonify
    @ActionProtector(has_permission('see-alerts'))
    def up_json(self):
        up = get_up()
        return {'up': [c.to_dict() for c in up]}

    @jsonify
    @ActionProtector(has_permission('see-alerts'))
    def down_json(self):
        down = get_down()
        return {'down': [c.to_dict() for c in down]}

    @jsonify
    @ActionProtector(has_permission('edit-alerts'))
    def set_down(self):
        addr = request.params.get("addr")
        h = model.Host.get_by_addr(addr)
        a = h.add_alert()
        mycache.remove_value("down")
        return {'alert': a.to_dict()}

    @jsonify
    @ActionProtector(has_permission('edit-alerts'))
    def set_up(self):
        addr = request.params.get("addr")
        a = model.Alert.query_down().filter_by(addr=addr).first()
        if not a:
            return {'alert': None}

        a.up = True
        model.Session.commit()
        mycache.remove_value("down")
        mycache.remove_value("up")
        return {'alert': a.to_dict()}

    @jsonify
    @ActionProtector(has_permission('edit-alerts'))
    def update(self, id):
        a = model.Session.query(model.Alert).get(id)
        if 'ok' in request.params:
            ok = request.params.get("ok")
            ok = (ok == 'true')
            a.ok = ok
        if 'reason' in request.params:
            reason = request.params.get("reason")
            a.reason = reason
        if 'note_short' in request.params:
            note_short = request.params.get("note_short")
            note_long = request.params.get("note_long")
            a.add_note(note_short, note_long)

        model.Session.commit()
        self._clear_caches()

        return {'alert': a.to_dict()}

    @jsonify
    @ActionProtector(has_permission('see-alerts'))
    def up_addrs_json(self):
        return {'addrs': [a for a in model.Host.get_up_addresses()]}
    @jsonify
    @ActionProtector(has_permission('see-alerts'))
    def down_addrs_json(self):
        return {'addrs': [a.addr for a in get_down()]}

    @validate(schema=forms.AddNote(),form='notes', on_get=True)
    @ActionProtector(has_permission('edit-alerts'))
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

        redirect_to(action="index")

    @ActionProtector(has_permission('see-alerts'))
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

    def _clear_caches(self):
        mycache.remove_value("down")
        mycache.remove_value("up")
        return "ok"
