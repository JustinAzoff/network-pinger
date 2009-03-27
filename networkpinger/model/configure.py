from paste.deploy import appconfig
from pylons import config

from networkpinger.config.environment import load_environment

def configure(filename='development.ini'):
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
