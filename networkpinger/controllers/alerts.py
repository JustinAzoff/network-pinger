import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from networkpinger.lib.base import BaseController, render

log = logging.getLogger(__name__)

from networkpinger import model

class AlertsController(BaseController):

    def index(self):
        c.down = model.Alert.query_down()
        return render('/alerts.mako')
