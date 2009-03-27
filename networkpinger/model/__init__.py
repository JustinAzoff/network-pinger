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


Base = declarative_base(metadata=meta.metadata)

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

    notes       = orm.relation('Note', backref='alert', lazy='dynamic')


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
        return Session.query(Alert).filter(Alert.uptime==None)

sa.Index('addr_uptime', Alert.addr, Alert.uptime, unique=True)

class Host(Base):
    __tablename__ = 'hosts'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    addr        = sa.Column(sa.types.String(255),   nullable=False)
    name        = sa.Column(sa.types.String(255),   nullable=False)
    monitor     = sa.Column(sa.types.Boolean,       nullable=False, default=True)

    alerts      = orm.relation('Alert', backref='host', lazy='dynamic')

    def __init__(self, addr, name, monitor=True):
        self.addr = addr
        self.name = name
        self.monitor = monitor

    def __repr__(self):
       return "<Host('%s', '%s')>" % (self.addr, self.name)

    def add_alert(self):
        a = Alert.query_down().filter(Alert.addr==self.addr).first()
        if not a:
            a = Alert(self.addr, self.name)
            self.alerts.append(a)
            Session.add(a)
            Session.commit()
        return a

class Note(Base):
    __tablename__ = 'notes'

    id          = sa.Column(sa.types.Integer,       primary_key=True)
    added       = sa.Column(sa.types.DateTime,      nullable=False,default=datetime.datetime.now)
    short       = sa.Column(sa.types.String(80),    nullable=False)
    long        = sa.Column(sa.types.Text,          nullable=True)

    alert_id    = sa.Column(sa.types.Integer,       sa.ForeignKey('alerts.id'))
