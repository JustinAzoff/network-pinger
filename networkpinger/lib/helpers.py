"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html.tags import *
from webhelpers.date import *
#from webhelpers.date import time_ago_in_words

import datetime
def time_ago_in_words(from_time):
    now = datetime.datetime.now()
    d = (now - from_time).seconds

    r = ""

    minute = 60
    hour   = 60 * minute
    day    = 24 * hour
    year   = 365 * day

    did_years = False
    did_days = False
    did_hours = False

    if(d > year):
        r+= d/year + " years"
        d %= year
        did_years = True

    if(d > day):
        r+= " %d days" % (d/day)
        d %= day
        did_days = true

    if(d > hour):
        r+= " %d hours" % (d/hour)
        d %= hour
        did_hours = True

    if(did_years):
        return r

    if(d > minute):
        r+= " %d minutes" % (d/minute)
        d %= minute
    
    if (did_hours):
        return r

    r+= " %d seconds" % d
    return r
