import ConfigParser
def read_config(fn):
    c = ConfigParser.ConfigParser()
    c.read(fn)
    return dict(c.items("pinger"))
