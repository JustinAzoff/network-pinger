"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import config, url
from routes.util import URLGenerator
from webtest import TestApp

import pylons.test


# Invoke websetup with the current config file
SetupCommand('setup-app').run([config['__file__']])

environ = {}

from networkpinger import model
class TestModel(TestCase):
    """
    We want the database to be created from scratch before each test and dropped after
    each test (thus making them unit tests).
    """
    def setUp(self):
        #model.resync()
        model.meta.metadata.create_all(bind=model.meta.engine)
    def tearDown(self):
        model.meta.Session.remove()
        model.meta.metadata.drop_all(bind=model.meta.engine)

class TestController(TestModel):

    def __init__(self, *args, **kwargs):
        if pylons.test.pylonsapp:
            wsgiapp = pylons.test.pylonsapp
        else:
            wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)

__all__ = ['environ', 'url', 'TestController','model']
