from networkpinger.tests import *

class TestAlertsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='alerts', action='index'))
        # Test response...

        assert 'Nothing is down' in response

    def test_with_alert(self):
        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' not in response

        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()

        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' in response

        a.up = True

        response = self.app.get(url(controller='alerts', action='index'))
        assert '1.2.3.4' not in response

    def test_alert_note(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        a.add_note("testing")

        response = self.app.get(url(controller='alerts', action='index'))
        assert 'testing' in response

        a.add_note("blah blah")

        response = self.app.get(url(controller='alerts', action='index'))
        assert 'testing' not in response
        assert 'blah blah' in response

    def test_alert_notes(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        a.add_note("testing")
        a.add_note("blah blah")

        response = self.app.get(url(controller='alerts', action='notes',id=a.id))
        assert 'testing' in response
        assert 'blah blah' in response

    def test_add_alert_no_short(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        response = self.app.get(url(controller='alerts', action='notes',id=a.id))

        form = response.form
        form['long'] ='whatever'
        res = form.submit()
        assert res.status != 302

    def test_add_alert(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        response = self.app.get(url(controller='alerts', action='notes',id=a.id))

        form = response.form
        form['short']='testing'
        form['long'] ='whatever'
        res = form.submit().follow()
        assert 'testing' in res

        response = self.app.get(url(controller='alerts', action='notes',id=a.id))
        assert 'whatever' in response

    def test_alerts_by_addr(self):
        h = model.Host.add("1.2.3.4",'foo')
        response = self.app.get(url(controller='alerts', action='addr',id=h.addr))

        assert 'No alert history' in response

        a = h.add_alert()
        response = self.app.get(url(controller='alerts', action='addr',id=h.addr))
        assert 'No alert history' not in response
