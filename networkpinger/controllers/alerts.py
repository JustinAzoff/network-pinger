import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from networkpinger.lib.base import BaseController, render, validate

log = logging.getLogger(__name__)

from networkpinger import model

from networkpinger.model import forms

class AlertsController(BaseController):

    def index(self):
        c.down = model.Alert.query_down().all()
        return render('/alerts/index.mako')
    def notes(self, id):
        a = model.Session.query(model.Alert).filter_by(id=id).one()
        c.alert = a
        return render('/alerts/notes.mako')

    @validate(schema=forms.AddNote(),form='notes', on_get=True)
    def addnote(self, id):
        a = model.Session.query(model.Alert).filter_by(id=id).one()
        short = self.form_result.get("short")
        long = self.form_result.get("long")
        a.add_note(short, long)
        model.Session.commit()
        redirect_to(action="index")
