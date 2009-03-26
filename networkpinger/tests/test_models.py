from networkpinger.tests import *

class TestModels(TestController):

    # The setUp and tearDown methods get inherited from TestController

    def test_Alert(self):
        print
        a = model.Alert('1.2.3.4','Host Foo')
        model.meta.Session.add(a)
        model.meta.Session.flush()

        a2 = model.Alert.query_down().all()[0]
        assert a == a2

        print a.up, a.uptime
        assert a.up is False
        assert a.uptime is None

        a.up = True

        print a.up, a.uptime
        assert a.up is True
        assert a.uptime is not None

