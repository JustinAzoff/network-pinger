from networkpinger.tests import *
import simplejson

class TestAlertsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='alerts', action='down'))
        # Test response...

        assert 'Nothing is down' in response

    def test_with_alert(self):
        response = self.app.get(url(controller='alerts', action='down'))
        assert '1.2.3.4' not in response

        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()

        response = self.app.get(url(controller='alerts', action='down'))
        assert '1.2.3.4' in response

        a.up = True

        response = self.app.get(url(controller='alerts', action='down'))
        assert '1.2.3.4' not in response

    def test_alert_note(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        a.add_note("testing")

        response = self.app.get(url(controller='alerts', action='down'))
        assert 'testing' in response

        a.add_note("blah blah")

        response = self.app.get(url(controller='alerts', action='down'))
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

    def test_add_note_no_short(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        response = self.app.get(url(controller='alerts', action='notes',id=a.id))

        form = response.form
        form['long'] ='whatever'
        res = form.submit()
        assert res.status != 302

    def test_add_note(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        response = self.app.get(url(controller='alerts', action='notes',id=a.id))

        form = response.form
        form['short']='testing'
        form['long'] ='whatever'
        res = form.submit().follow()
        res = self.app.get(url(controller='alerts', action='down'))
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


    def test_alerts_json(self):
        h = model.Host.add("1.2.3.4",'foo')
        response = simplejson.loads(self.app.get(url(controller='alerts', action='down_json')).body)

        assert response['down'] == []

    def test_alerts_json_with_alert(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()
        response = simplejson.loads(self.app.get(url(controller='alerts', action='down_json')).body)
        ja = response['down'][0]

        assert ja['id'] == a.id
        assert ja['addr'] == a.addr

    def test_set_down(self):
        h = model.Host.add("1.2.3.4",'foo')

        response = self.app.get(url(controller='alerts', action='set_down',addr='1.2.3.4'))

        response = self.app.get(url(controller='alerts', action='down'))
        assert '1.2.3.4' in response

    def test_set_up(self):
        h = model.Host.add("1.2.3.4",'foo')
        a = h.add_alert()

        response = self.app.get(url(controller='alerts', action='set_up',addr='1.2.3.4'))

        response = self.app.get(url(controller='alerts', action='down'))
        assert '1.2.3.4' not in response
