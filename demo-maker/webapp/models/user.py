# models.user
# -*- coding: UTF-8 -*-

from libs import store
import hashlib
from datetime import datetime
from MySQLdb import IntegrityError

def pwd_hash(email, password):
    if not password:
        return ""
    m = hashlib.md5(email.lower())
    m.update(password)
    return m.hexdigest()[:15]

def create_session(email):
    m = hashlib.md5(email.lower())
    m.update(str(datetime.now()))
    return m.hexdigest()[:15]


class User(object):

    FLAG_NORMAL = 'N'
    FLAG_BANNED = 'B'
    FLAG_ADMIN = 'A'

    def __init__(self, id, email, name, passhash, session, rtime, flag):
        self.id = str(id)
        self.email = email
        self.passhash = passhash
        self.session = session
        self.name = name
        self.rtime = rtime
        self.flag = flag

    @classmethod
    def get(cls, id):
        r = store.execute("select id, email, name, passwd, session, rtime, flag from demo_user"
                " where id=%s", id)
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def get_by_email(cls, email):
        r = store.execute("select id, email, name, passwd, session, rtime, flag from demo_user"
                " where email=%s", email)
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def count(cls):
        r = store.execute("select count(id) from demo_user")
        return r and r[0][0]

    def update_session(self, session):
        store.execute("update demo_user set `session`=%s where id=%s", (session, self.id))
        store.commit()
        self.session = session

    def expire_session(self):
        store.execute("update demo_user set `session`='' where id=%s", self.id)
        store.commit()
        self.session = None

    @classmethod
    def login(cls, email, password):
        passhash = pwd_hash(email, password)
        u = cls.get_by_email(email)
        if passhash == u.passhash:
            session = create_session(email)
            u.update_session(session)
            return u

    @classmethod
    def register(cls, email, password):
        passhash = pwd_hash(email, password)
        try:
            name = email.split('@')[0]
            store.execute("insert into demo_user(email, passwd, name) "
                    " values(%s, %s, %s)", (email, passhash, name))
            store.commit()
            id = store.get_cursor(table="demo_user").lastrowid
            u = cls.get(id)
            session = create_session(email)
            u.update_session(session)
            return u
        except IntegrityError:
            store.rollback()
