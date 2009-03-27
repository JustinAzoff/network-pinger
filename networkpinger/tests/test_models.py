from networkpinger.tests import *

class TestModels(TestController):

    # The setUp and tearDown methods get inherited from TestController

    def test_Alert(self):
        print
        a = model.Alert('1.2.3.4','Host Foo')
        model.Session.add(a)
        model.Session.flush()

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
        model.Session.add(a)
        model.Session.flush()

        #FIXME: should fail
        a2 = model.Alert('1.2.3.4','Host Foo')
        model.Session.add(a)
        model.Session.flush()

    def test_add_Host(self):
        print
        h = model.Host.add('1.2.3.4','Host Foo')

        len(h.alerts.all())==0
        a = h.add_alert()

        len(h.alerts.all())==1

        a2 = h.add_alert()
        len(h.alerts.all())==1
        assert a is a2

        h2 = model.Session.query(model.Host).filter(model.Host.addr=='1.2.3.4').first()
        assert h is h2

    def test_add_host(self):
        print
        h =  model.Host.get_by_addr("1.2.3.4")
        assert h is None
        h = model.Host.add("1.2.3.4","foo")
        assert h.addr == '1.2.3.4'

        h2 = model.Host.add("1.2.3.4","foo")
        assert h is h2


    def test_add_alert(self):
        h = model.Host.add("1.2.3.4","foo")
        a = h.add_alert()
        assert a.cur_note is None
        assert a.notes.count()==0

        a.add_note("testing")
        assert a.cur_note == "testing"
        assert a.notes.count()==1

        a.add_note("testing2")
        assert a.cur_note == "testing2"
        assert a.notes.count()==2

    def test_host_get_all_addresses(self):
        assert '1.2.3.4' not in model.Host.get_all_addresses()
        
        h = model.Host.add("1.2.3.4","foo")
        assert '1.2.3.4' in model.Host.get_all_addresses()

        h.active = False
        assert '1.2.3.4' not in model.Host.get_all_addresses()

        h.active = True
        assert '1.2.3.4' in model.Host.get_all_addresses()

        
    def test_host_get_up_addresses(self):
        h = model.Host.add("1.2.3.4","foo")
        assert '1.2.3.4' in model.Host.get_up_addresses()

        a = h.add_alert()
        assert '1.2.3.4' not in model.Host.get_up_addresses()

        a.up = True
        assert '1.2.3.4' in model.Host.get_up_addresses()

    def test_host_get_down_addresses(self):
        h = model.Host.add("1.2.3.4","foo")
        assert '1.2.3.4' not in model.Host.get_down_addresses()

        a = h.add_alert()

        assert '1.2.3.4' in model.Host.get_down_addresses()

        a.up = True
        assert '1.2.3.4' not in model.Host.get_down_addresses()
