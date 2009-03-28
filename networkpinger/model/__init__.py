"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from networkpinger.model import meta
Session = meta.Session

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine

import ConfigParser
def configure(filename='development.ini'):
    c = ConfigParser.ConfigParser({'here':'./'})
    c.read(filename)
    uri = c.get("app:main","sqlalchemy.url")
    init_model(sa.create_engine(uri))

Base = declarative_base(metadata=meta.metadata)

class Note(Base):
    __tablename__ = 'notes'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    added       = sa.Column(sa.types.DateTime,      nullable=False,default=datetime.datetime.now)
    short       = sa.Column(sa.types.String(80),    nullable=False)
    long        = sa.Column(sa.types.Text,          nullable=True)

    alert_id    = sa.Column(sa.types.Integer,       sa.ForeignKey('alerts.id'))

class Alert(Base):
    __tablename__ = 'alerts'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    addr        = sa.Column(sa.types.String(255),   nullable=False)
    name        = sa.Column(sa.types.String(255),   nullable=False)
    time        = sa.Column(sa.types.DateTime,      nullable=False,default=datetime.datetime.now)
    uptime      = sa.Column(sa.types.DateTime,      nullable=True, default=None)
    ok          = sa.Column(sa.types.Boolean,       nullable=False, default=False)
    reason      = sa.Column(sa.types.String(80),    nullable=True)
    cur_note    = sa.Column(sa.types.String(80),    default=None)

    host_id     = sa.Column(sa.types.Integer,       sa.ForeignKey('hosts.id'))

    notes       = orm.relation('Note', backref='alert', lazy='dynamic',order_by=sa.desc(Note.added))


    def __init__(self, addr, name):
        self.addr = addr
        self.name = name

    def __repr__(self):
       return "<Alert('%s', '%s')>" % (self.addr, self.name)

    def _set_up(self, val):
        if val == True and not self.uptime:
            self.uptime = datetime.datetime.now()
        else:
            self.uptime = None
        Session.add(self)

    def _get_up(self):
        return bool(self.uptime)
    up = property(_get_up, _set_up)

    @classmethod
    def query_down(self):
        return Session.query(Alert).filter(Alert.uptime==None).order_by(sa.desc(Alert.time))

    @classmethod
    def query_recent_up(self):
        now = datetime.datetime.now()
        before = now - datetime.timedelta(hours=24)
        recent = Session.query(Alert).filter(Alert.time > before).filter(Alert.uptime!=None).order_by(sa.desc(Alert.uptime))
        
        seen_alerts = {}
        ret = []
        for a in recent:
            r = seen_alerts.get(a.addr)
            if r:
                r.count += 1
            else:
                seen_alerts[a.addr] = a
                a.count = 0
                ret.append(a)
        return ret

    def add_note(self, short, long=None):
        n = Note()
        n.short = short
        n.long = long
        self.notes.append(n)
        self.cur_note = n.short
        Session.add(n)
        Session.add(self)
        Session.commit()
        return n

sa.Index('addr_uptime', Alert.addr, Alert.uptime, unique=True)

class Host(Base):
    __tablename__ = 'hosts'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    addr        = sa.Column(sa.types.String(255),   nullable=False)
    name        = sa.Column(sa.types.String(255),   nullable=False)
    active      = sa.Column(sa.types.Boolean,       nullable=False, default=True)

    alerts      = orm.relation('Alert', backref='host', lazy='dynamic',order_by=sa.desc(Alert.time))

    def __init__(self, addr, name, active=True):
        self.addr = addr
        self.name = name
        self.active = active

    def __repr__(self):
       return "<Host('%s', '%s')>" % (self.addr, self.name)

    @classmethod
    def get_by_addr(self, addr):
        return Session.query(Host).filter(Host.addr==addr).first()

    @classmethod
    def add(self, addr, name):
        h = Host.get_by_addr(addr)
        if not h:
            h = Host(addr, name)
            Session.add(h)
            Session.commit()
        return h

    @classmethod
    def get_all_addresses(cls):
        q = Session.query(Host).filter(Host.active==True).all()
        return [h.addr for h in q]

    @classmethod
    def get_down_addresses(cls):
        return [a.addr for a in Alert.query_down()]

    @classmethod
    def get_up_addresses(cls):
        ips = set(Host.get_all_addresses())
        ips -= set(Host.get_down_addresses())
        return list(ips)

    def add_alert(self):
        a = Alert.query_down().filter(Alert.addr==self.addr).first()
        if not a:
            a = Alert(self.addr, self.name)
            self.alerts.append(a)
            Session.add(a)
            Session.commit()
        return a
