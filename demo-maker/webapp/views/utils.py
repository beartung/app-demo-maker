#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import SITE_COOKIE, DOMAIN
import re
from webapp.models.user import User
from datetime import datetime, timedelta

_P3P_POLICY = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

def format_rfc822_date(dt, localtime=True, cookie_format=False):
    if localtime:
        dt = dt - timedelta(hours=8)
    fmt = "%s, %02d %s %04d %02d:%02d:%02d GMT"
    if cookie_format:
        fmt = "%s, %02d-%s-%04d %02d:%02d:%02d GMT"

    # dt.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    return fmt % (
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
            dt.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month-1],
            dt.year, dt.hour, dt.minute, dt.second)

def format_cookie_date(dt, localtime=True):
    return format_rfc822_date(dt, localtime=True, cookie_format=True)

EMAILRE = re.compile(r'^[_\.0-9a-zA-Z+-]+@([0-9a-zA-Z]+[0-9a-zA-Z-]*\.)+[a-zA-Z]{2,4}$')
def is_validate_email(email):
    if not email:
        return False
    if len(email) >= 6:
        return EMAILRE.match(email) != None
    return False

def expire_session(req):
    if req.user:
        req.user.expire_session()
        req.response.expire_cookie(SITE_COOKIE, path='/', domain=DOMAIN)

def check_session(req):
    cookie = req.get_cookie(SITE_COOKIE)
    print "check session", cookie
    if cookie:
        email, user_id, session = cookie.split(':')
        user = User.get(user_id)
        if user and user.session == session:
            req.user = user
            req.email = email

    print "session user", req.user

def set_session(req, user):
    req.user = user
    if user:
        print "set session", user.session
        d = {'domain':DOMAIN, 'httponly':'True'}
        dt = datetime.now() + timedelta(days=60)
        d['expires'] = format_cookie_date(dt, True)

        print "cookie", d
        req.response.set_cookie(SITE_COOKIE, '%s:%s:%s' % (user.email, user.id, user.session), path='/', **d)
        #req.response.set_header('P3P', _P3P_POLICY)
