from networkpinger.tests import *

class TestModels(TestController):

    # The setUp and tearDown methods get inherited from TestController

    def test_Alert(self):
        print
        a = model.Alert('1.2.3.4','Host Foo')
        model.meta.Session.add(a)
        model.meta.Session.flush()

        down = model.Alert.query_down().all()
        assert len(down)==1

        a2 = down[0]
        assert a == a2

        print a.up, a.uptime
        assert a.up is False
        assert a.uptime is None

        a.up = True

        print a.up, a.uptime
        assert a.up is True
        assert a.uptime is not None

        down = model.Alert.query_down().all()
        assert len(down)==0

    def test_Dup_Alerts(self):
        print
        a = model.Alert('1.2.3.4','Host Foo')
        model.meta.Session.add(a)
        model.meta.Session.flush()

        a2 = model.Alert('1.2.3.4','Host Foo')
        model.meta.Session.add(a)
        model.meta.Session.flush()

    def test_Host(self):
        print
        h = model.Host('1.2.3.4','Host Foo')
        model.meta.Session.add(h)

        len(h.alerts.all())==0
        a = h.add_alert()

        len(h.alerts.all())==1

        a2 = h.add_alert()
        len(h.alerts.all())==1
        assert a is a2

        h2 = model.meta.Session.query(model.Host).filter(model.Host.addr=='1.2.3.4').first()
        assert h is h2

    def test_add_host(self):
        print
        assert model.Host.get_by_addr("1.2.3.4") is None
        h = model.Host.add("1.2.3.4","foo")
        assert h.addr == '1.2.3.4'

        h2 = model.Host.add("1.2.3.4","foo")
        assert h is h2

