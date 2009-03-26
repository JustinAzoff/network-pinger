from networkpinger.tests import *

class TestAlertsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='alerts', action='index'))
        # Test response...

        assert 'Nothing is down' in response

    def test_with_alert(self):
        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' not in response

        h = model.Host("1.2.3.4",'foo')
        a = h.add_alert()

        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' in response

        a.up = True

        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' not in response
