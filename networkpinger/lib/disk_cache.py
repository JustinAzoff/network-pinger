import logging
log = logging.getLogger(__name__)

from decorator import decorator
from pylons import request
from pylons import cache

import os

def disk_cache(basedir):
    def render_to_disk(func, *args, **kwargs):
        def create_func():
            d = os.path.dirname(fn)
            if not os.path.isdir(d):
                os.makedirs(d)
            f=open(fn,'w')
            s = func(*args, **kwargs)
            f.write(s)
            f.close()
            return s

        path = request.path[1:]
        qs = request.query_string
        fn = os.path.join(basedir, path + '.html')
        if not fn.startswith(basedir):
            return ''
        log.info("writing to %s" % fn)
        mycache = cache.get_cache('disk_cache', type='memory',expiretime=0)
        return mycache.get_value(key=fn, createfunc=create_func)
    return decorator(render_to_disk)

def rm_cached(basedir, files):
    for f in files:
        fn = os.path.join(basedir, f + '.html')
        try :
            log.debug("deleting %s" % fn)
            os.unlink(fn)
        except:
            pass
