#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs import store, filestore
from MySQLdb import IntegrityError
from wand.image import Image
from datetime import datetime
from config import SITE
import time
import traceback

class Rect(object):

    def __init__(self, id, x, y, width, height):
        self.id = str(id)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @classmethod
    def get(cls, id):
        r = store.execute("select id, x, y, width, height from demo_rect"
                " where id=%s", id)
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def new(cls, x, y, w, h):
        store.execute("insert into demo_rect(x, y, width, height)"
            " values(%s, %s, %s, %s)", (x, y, w, h))
        store.commit()
        id = store.get_cursor(table="demo_rect").lastrowid
        return id

    def save(self):
        store.execute("update demo_rect set x=%s, y=%s, width=%s, height=%s"
            " where id=%s", (self.x, self.y, self.width, self.height, self.id))
        store.commit()

class Screen(object):

    FLAG_NORMAL = 'N'
    FLAG_DELETED = 'D'

    def __init__(self, id, name, os, width, height, icon_width, icon_height, virtual_keys):
        self.id = str(id)
        self.name = name
        self.os = os
        self.width = width
        self.height = height
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.virtual_keys = virtual_keys == 'Y'

    @property
    def is_android(self):
        return self.os == 'android'

    @classmethod
    def get(cls, id):
        if id == '0':
            return DEFAULT_SCREEN

        r = store.execute("select id, name, os, width, height, icon_width, icon_height,"
                " virtual_keys from demo_screen where id=%s and flag=%s", (id, cls.FLAG_NORMAL))
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def gets(cls):
        rs = store.execute("select id, name, os, width, height, icon_width, icon_height,"
                " virtual_keys from demo_screen where flag=%s", cls.FLAG_NORMAL)
        return [cls(*r) for r in rs]

    def remove(self):
        store.execute("update demo_screen set flag=%s where id=%s", (self.FLAG_DELETED, self.id))
        store.commit()

    @classmethod
    def new(cls, name, os, width, height, icon_width, icon_height, virtual_keys):
        try:
            virtual_keys = virtual_keys and 'Y' or 'N'
            store.execute("insert into demo_screen(name, os, width, height, icon_width,"
                    " icon_height, virtual_keys) values(%s,%s,%s,%s,%s,%s,%s)", (name, os, width,
                        height, icon_width, icon_height, virtual_keys))
            store.commit()
            id = store.get_cursor(table="demo_screen").lastrowid
            return id
        except IntegrityError:
            store.rollback()

    def update(self, name, os, width, height, icon_width, icon_height, virtual_keys):
        try:
            virtual_keys = virtual_keys and 'Y' or 'N'
            store.execute("update demo_screen set name=%s, os=%s, width=%s, height=%s,"
                        " icon_width=%s, icon_height=%s, virtual_keys=%s where id=%s", (name, os, width,
                        height, icon_width, icon_height, virtual_keys, self.id))
            store.commit()
        except IntegrityError:
            store.rollback()

    def rect(self):
        return Rect(0, 0, self.width, self.height)

    @property
    def json_dict(self):
        d = {
            'id': self.id,
            'name': self.name,
            'os': self.os,
            'width': self.width,
            'height': self.height,
            'virtual_keys': self.virtual_keys
        }
        return d


NEXUS4_SCREEN = Screen('0', 'nexus4', 'android', 720, 1144, 96, 96, 'Y')
#+----+----------+---------+-------+--------+------------+-------------+------+--------------+
#| id | name     | os      | width | height | icon_width | icon_height | flag | virtual_keys |
#+----+----------+---------+-------+--------+------------+-------------+------+--------------+
#|  1 | note2    | android |   720 |   1232 |         96 |          96 | N    | N            |
#|  2 | iPhone4S | iOS     |   640 |    920 |         74 |          74 | N    | N            |
#+----+----------+---------+-------+--------+------------+-------------+------+--------------+
DEFAULT_SCREEN = NEXUS4_SCREEN

class App(object):

    FLAG_NORMAL = 'N'
    FLAG_DELETED = 'D'

    def __init__(self, id, user_id, name, screen_id, icon_ver, zoomout, rtime, flag):
        self.id = str(id)
        self.name = name
        self.user_id = str(user_id)
        self.screen_id = str(screen_id)
        self.icon_ver = icon_ver
        self.zoomout = zoomout
        self.rtime = rtime
        self.flag = flag

    def can_admin(self, user):
        return user and user.id == self.user_id

    @property
    def screen(self):
        return Screen.get(self.screen_id)

    @property
    def zoomed_width(self):
        return self.screen.width/self.zoomout

    @property
    def zoomed_height(self):
        return self.screen.height/self.zoomout

    @classmethod
    def new(cls, user_id, name, icon_filename, screen_id=DEFAULT_SCREEN.id, zoomout=2):
        try:
            icon_ver = 1
            store.execute("insert into demo_app(user_id, name, screen_id, icon_ver, zoomout)"
                    " values(%s,%s,%s,%s,%s)", (user_id, name, screen_id, icon_ver, zoomout))
            store.commit()
            id = store.get_cursor(table="demo_app").lastrowid

            screen = Screen.get(screen_id)
            data = open(icon_filename).read()
            with Image(blob=data) as img:
                img.resize(screen.icon_width, screen.icon_height, "catrom")
                filestore.save_image(img, "app-icon-%s-%s.jpg" % (id, icon_ver))
                img.resize(screen.icon_width/zoomout, screen.icon_height/zoomout, "catrom")
                filestore.save_image(img, "app-icon-%s-%s.jpg" % (id, icon_ver), "s")
            return id
        except IntegrityError:
            #traceback.print_exc()
            store.rollback()

    def remove(self):
        store.execute("update demo_app set flag=%s where id=%s", (self.FLAG_DELETED, self.id))
        store.commit()

    def update(self, name, icon_filename='', zoomout=2):
        try:
            now = datetime.now()
            if name and name != self.name:
                store.execute("update demo_app set name=%s, rtime=%s"
                        " where id=%s", (name, now, self.id))
                store.commit()
                self.name = name

            if icon_filename:
                icon_ver = self.icon_ver + 1
                data = open(icon_filename).read()
                screen = self.screen
                with Image(blob=data) as img:
                    img.resize(screen.icon_width, screen.icon_height, "catrom")
                    filestore.save_image(img, "app-icon-%s-%s.jpg" % (self.id, icon_ver))
                    img.resize(screen.icon_width/zoomout, screen.icon_height/zoomout, "catrom")
                    filestore.save_image(img, "app-icon-%s-%s.jpg" % (self.id, icon_ver), "s")

                store.execute("update demo_app set icon_ver=%s, rtime=%s"
                        " where id=%s", (icon_ver, now, self.id))
                store.commit()
                self.icon_ver = icon_ver

        except IntegrityError:
            #traceback.print_exc()
            store.rollback()

    @property
    def path(self):
        return "/app/%s/" % self.id

    @property
    def api(self):
        return "%s/app/%s/?output=json" % (SITE, self.id)

    @property
    def icon(self):
        return "/per/img/s/app-icon-%s-%s.jpg" % (self.id, self.icon_ver)

    @property
    def pages(self):
        from webapp.models.page import Page
        return Page.gets_by_app(self.id)

    @classmethod
    def get(cls, id):
        r = store.execute("select id, user_id, name, screen_id, icon_ver, zoomout,"
                " rtime, flag from demo_app where id=%s and flag=%s", (id, cls.FLAG_NORMAL))
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def gets_by_user(cls, user_id):
        rs = store.execute("select id, user_id, name, screen_id, icon_ver, zoomout,"
                " rtime, flag from demo_app where user_id=%s and flag=%s", (user_id, cls.FLAG_NORMAL))
        return len(rs), [cls(*r) for r in rs]

    @property
    def json_dict(self):
        d = {
                'id':self.id,
                'api': self.api,
                'name':self.name,
                'icon': '%s%s' % (SITE, self.icon),
                'icon_width': self.screen.icon_width,
                'icon_height': self.screen.icon_height,
                'url': '%s%s' % (SITE, self.path),
                'time': time.mktime(self.rtime.timetuple()),
            }
        d['screen'] = self.screen.json_dict
        d['page_ids'] = [p.id for p in self.pages]
        pages = {}
        for p in self.pages:
            pages[p.id] = p.json_dict
        d['pages'] = pages
        return d
