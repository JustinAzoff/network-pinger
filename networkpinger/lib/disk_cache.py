import logging
log = logging.getLogger(__name__)

from decorator import decorator
from pylons import request
from pylons import cache

import os

def disk_cache(basedir):
    def render_to_disk(func, *args, **kwargs):
        def create_func():
            try:
                f = open(fn)
                s = f.read()
                f.close()
                log.info("not writing to %s, returning existing content" % fn)
                return s
            except:
                pass
            log.info("writing to %s" % fn)
            d = os.path.dirname(fn)
            if not os.path.isdir(d):
                os.makedirs(d)
            s = func(*args, **kwargs)
            tfn = fn + '.tmp'
            f=open(tfn,'w')
            f.write(s)
            f.close()
            os.rename(tfn,fn)
            return s

        path = request.path[1:]
        qs = request.query_string
        fn = os.path.normpath(os.path.join(basedir, path + '.html'))
        if not fn.startswith(basedir):
            return ''
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
