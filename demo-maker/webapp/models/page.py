#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs import store, filestore
from MySQLdb import IntegrityError
from wand.image import Image
from webapp.models.app import Rect, Screen, App
from datetime import datetime
from config import SITE

class Action(object):

    TYPE_TOUCH       = 'T'
    TYPE_BACK        = 'B'
    TYPE_SLIDE       = 'E'
    TYPE_SLIDE_LEFT  = 'L'
    TYPE_SLIDE_RIGHT = 'R'
    TYPE_SLIDE_UP    = 'U'
    TYPE_SLIDE_DOWN  = 'D'
    TYPE_INPUT       = 'I'
    TYPE_GALLERY     = 'G'
    TYPE_CAMERA      = 'C'
    TYPE_SHARE       = 'S'

    FLAG_NORMAL = 'N'
    FLAG_DELETED = 'D'

    TYPE_NAMES = {
        TYPE_TOUCH : "点击",
        TYPE_BACK : "返回",
        TYPE_SLIDE_LEFT : "向左滑动",
        TYPE_SLIDE_RIGHT : "向右滑动",
        TYPE_SLIDE_UP : "向上滑动",
        TYPE_SLIDE_DOWN : "向下滑动",
        TYPE_INPUT : "输入框",
        TYPE_GALLERY : "调用相册",
        TYPE_CAMERA : "调用相机",
        TYPE_SHARE : "调用分享",
    }

    TYPE_ICONS = {
        TYPE_TOUCH : "glyphicon-hand-up",
        TYPE_SLIDE_LEFT : "glyphicon-arrow-left",
        TYPE_SLIDE_RIGHT : "glyphicon-arrow-right",
        TYPE_SLIDE_UP : "glyphicon-arrow-up",
        TYPE_SLIDE_DOWN : "glyphicon-arrow-down",
        TYPE_INPUT : "glyphicon-text-width",
        TYPE_GALLERY : "glyphicon-picture",
        TYPE_CAMERA : "glyphicon-camera",
        TYPE_SHARE : "glyphicon-share",
        TYPE_BACK : "icon-reply",
    }

    def __init__(self, id, page_id, to_page_id, rect_id, resp_rect_id, dismiss, type, flag, rtime):
        self.id = str(id)
        self.page_id = str(page_id)
        self.to_page_id = str(to_page_id)
        self.rect_id = str(rect_id)
        self.resp_rect_id = str(resp_rect_id)
        self.dismiss = dismiss != 'N'
        self.type = type
        self.flag = flag
        self.rtime = rtime

    @property
    def rect(self):
        return Rect.get(self.rect_id)

    @property
    def resp_rect(self):
        return Rect.get(self.resp_rect_id)

    @property
    def from_page(self):
        return Page.get(self.page_id)

    @property
    def app(self):
        return self.from_page.app

    @property
    def scale(self):
        return self.app.zoomout

    @property
    def to_page(self):
        return Page.get(self.to_page_id)

    @property
    def type_name(self):
        return self.TYPE_NAMES[self.type]

    @property
    def type_icon(self):
        return self.TYPE_ICONS[self.type]

    @classmethod
    def new(cls, page_id, rect, type, dismiss=None, to_page_id=0, resp_rect=None):
        rect_id = rect and rect.id or 0
        resp_rect_id = resp_rect and resp_rect.id or 0
        try:
            dismiss = dismiss == 'Y' and 'Y' or 'N'
            store.execute("insert into demo_action(page_id, to_page_id, rect_id, resp_rect_id, `type`, `dismiss`)"
                    " values(%s,%s,%s,%s,%s,%s)", (page_id, to_page_id, rect_id, resp_rect_id, type, dismiss))
            store.commit()
            id = store.get_cursor(table="demo_action").lastrowid
            return id
        except IntegrityError:
            store.rollback()

    @classmethod
    def get(cls, id):
        r = store.execute("select id, page_id, to_page_id, rect_id, resp_rect_id, dismiss, `type`,"
                " flag, rtime from demo_action where id=%s and flag=%s", (id, cls.FLAG_NORMAL))
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def gets_by_page(cls, page_id):
        rs = store.execute("select id, page_id, to_page_id, rect_id, resp_rect_id, dismiss, `type`,"
                " flag, rtime from demo_action where page_id=%s and flag=%s", (page_id, cls.FLAG_NORMAL))
        return [cls(*r) for r in rs]

    def remove(self):
        store.execute("update demo_action set flag=%s where id=%s", (self.FLAG_DELETED, self.id))
        store.commit()

    @property
    def json_dict(self):
        d = {
                'id': self.id,
                'type': self.type,
                'dismiss': self.dismiss,
                'page_id': self.page_id,
                'to_page_id': self.to_page_id,
                'x': self.rect.x*self.scale,
                'y': self.rect.y*self.scale,
                'width': self.rect.width*self.scale,
                'height': self.rect.height*self.scale,
            }
        return d

class Page(object):

    TYPE_NORMAL = 'N'
    TYPE_LIST = 'L'
    TYPE_PAGER = 'P'
    TYPE_ITEM = 'I'
    TYPE_DIALOG = 'D'

    FLAG_NORMAL = 'N'
    FLAG_DELETED = 'D'

    def __init__(self, id, name, parent_id, app_id, photo_ver, rect_id, rtime, type, flag):
        self.id = str(id)
        self.name = name
        self.parent_id = str(parent_id)
        self.app_id = str(app_id)
        self.photo_ver = photo_ver
        self.rect_id = str(rect_id)
        self.rtime = rtime
        self.type = type
        self.flag = flag

    @classmethod
    def get(cls, id):
        r = store.execute("select id, name, parent_page_id, app_id, photo_ver, rect_id,"
                " rtime, `type`, flag from demo_page where id=%s and flag=%s", (id, cls.FLAG_NORMAL))
        if r and r[0]:
            return cls(*r[0])

    @classmethod
    def gets_by_app(cls, app_id):
        rs = store.execute("select id, name, parent_page_id, app_id, photo_ver, rect_id,"
                " rtime, `type`, flag from demo_page where app_id=%s and flag=%s", (app_id, cls.FLAG_NORMAL))
        return [cls(*r) for r in rs]

    @classmethod
    def gets_by_page(cls, page_id):
        rs = store.execute("select id, name, parent_page_id, app_id, photo_ver, rect_id,"
                " rtime, `type`, flag from demo_page where parent_page_id=%s and flag=%s", (page_id, cls.FLAG_NORMAL))
        return [cls(*r) for r in rs]

    def remove(self):
        store.execute("update demo_page set flag=%s where id=%s", (self.FLAG_DELETED, self.id))
        store.commit()

    @classmethod
    def new(cls, app, name, rect, photo_filename='', parent_id='', page_type=None):
        screen = app.screen
        page_type = page_type or cls.TYPE_NORMAL
        try:
            photo_ver = photo_filename and 1 or 0
            store.execute("insert into demo_page(name, parent_page_id, app_id, photo_ver, rect_id, `type`)"
                    " values(%s,%s,%s,%s,%s,%s)", (name, parent_id or '0', app.id, photo_ver, rect.id, page_type))
            store.commit()
            id = store.get_cursor(table="demo_page").lastrowid

            if photo_filename:
                data = open(photo_filename).read()
                with Image(blob=data) as img:
                    if page_type == cls.TYPE_ITEM:
                        rect.height = rect.width*img.height/img.width
                        rect.save()
                    img.resize(rect.width, rect.height, "catrom")
                    filestore.save_image(img, "page-photo-%s-%s.jpg" % (id, photo_ver))
                    img.resize(rect.width/app.zoomout, rect.height/app.zoomout, "catrom")
                    filestore.save_image(img, "page-photo-%s-%s.jpg" % (id, photo_ver), "s")
            else:
                rect.height = 100 #default height
                rect.save
            return id
        except IntegrityError:
            #traceback.print_exc()
            store.rollback()

    def update(self, name, photo_filename=''):
        try:
            now = datetime.now()
            if name and name != self.name:
                store.execute("update demo_page set name=%s, rtime=%s"
                        " where id=%s", (name, now, self.id))
                store.commit()

            if photo_filename:
                photo_ver = self.photo_ver + 1
                data = open(photo_filename).read()
                rect = self.rect
                zoomout = self.app.zoomout
                with Image(blob=data) as img:
                    img.resize(rect.width, rect.height, "catrom")
                    filestore.save_image(img, "page-photo-%s-%s.jpg" % (self.id, photo_ver))
                    img.resize(rect.width/zoomout, rect.height/zoomout, "catrom")
                    filestore.save_image(img, "page-photo-%s-%s.jpg" % (self.id, photo_ver), "s")

                store.execute("update demo_page set photo_ver=%s, rtime=%s"
                        " where id=%s", (photo_ver, now, self.id))
                store.commit()

        except IntegrityError:
            #traceback.print_exc()
            store.rollback()

    @property
    def photo(self):
        if self.photo_ver:
            return "/per/img/s/page-photo-%s-%s.jpg" % (self.id, self.photo_ver)
        return ""

    @property
    def src_photo(self):
        if self.photo_ver:
            return "/per/img/o/page-photo-%s-%s.jpg" % (self.id, self.photo_ver)
        return ""

    @property
    def path(self):
        return "/page/%s/" % self.id

    @property
    def rect(self):
        return Rect.get(self.rect_id)

    @property
    def app(self):
        return App.get(self.app_id)

    @property
    def parent(self):
        return self.parent_id and Page.get(self.parent_id)

    @property
    def screen(self):
        return self.app.screen

    @property
    def zoomed_width(self):
        return self.rect.width/self.app.zoomout

    @property
    def zoomed_height(self):
        return self.rect.height/self.app.zoomout

    @property
    def zoomed_x(self):
        return self.rect.x/self.app.zoomout

    @property
    def zoomed_y(self):
        return self.rect.y/self.app.zoomout

    @property
    def sub_pages(self):
        return self.gets_by_page(self.id)

    @property
    def actions(self):
        return Action.gets_by_page(self.id)

    @property
    def json_dict(self):
        d = {
                'id': self.id,
                'name': self.name,
                'parent_id': self.parent_id,
                'x': self.rect.x,
                'y': self.rect.y,
                'width': self.rect.width,
                'height': self.rect.height,
                'type': self.type,
            }
        d['photo'] = self.src_photo and '%s%s' % (SITE, self.src_photo) or ''
        d['actions'] = [a.json_dict for a in self.actions]
        d['sub_page_ids'] = [p.id for p in self.sub_pages]
        return d
