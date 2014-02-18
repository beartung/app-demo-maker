#!/usr/bin/python
# -*- coding: utf-8 -*-

from StringIO import StringIO
from quixote.errors import TraversalError, AccessError
from libs.template import st, stf

from webapp.models.user import User
from webapp.models.app import App, Screen

from qrencode import encode_scaled

import simplejson as json

_q_exports = []

def _q_index(req):
    if req.get_method() == 'POST':
        name = req.get_form_var("app_name", None)
        icon = req.get_form_var("app_icon", None)
        screen_id = req.get_form_var("app_screen", None)
        screen = Screen.get(screen_id)
        if name and icon and req.user and screen:
            filename = icon.tmp_filename
            app_id = App.new(req.user.id, name, filename, screen.id)
            if req.get_form_var("output", None) == 'json':
                req.response.set_content_type('application/json; charset=utf-8')
                total, apps = App.gets_by_user(req.user.id)
                ret = { 'err': 'ok', 'html': stf('/apps.html', 'app_list', apps=apps) }
                return json.dumps(ret)
            app = App.get(app_id)
            if app:
                return req.redirect(app.path)

def _q_lookup(req, id):
    app = App.get(id)
    if app:
        return AppUI(req, app)
    return TraversalError("no such app")

class AppUI(object):

    _q_exports = ['edit', 'remove', 'qrcode']

    def __init__(self, req, app):
        self.app = app

    def qrcode(self, req):
        app = self.app
        _, _, im = encode_scaled(data=app.api, size=190)
        io = StringIO()
        im.save(io, 'JPEG', quality=100)
        resp = req.response
        resp.set_content_type('image/jpeg')
        resp.set_header('Cache-Control', 'max-age=%d' % (365*24*60*60))
        resp.set_header('Expires', 'Wed, 01 Jan 2020 00:00:00 GMT')
        if 'pragma' in resp.headers:
            del resp.headers['pragma']
        return io.getvalue()

    def _q_index(self, req):
        app = self.app
        user = req.user
        if req.get_form_var("output", None) == 'json':
            req.response.set_content_type('application/json; charset=utf-8')
            return json.dumps(app.json_dict)
        return st('/app.html', **locals())

    def remove(self, req):
        app = self.app
        if req.get_method() == "POST" and app.can_admin(req.user):
            if req.get_form_var("output", None) == 'json':
                req.response.set_content_type('application/json; charset=utf-8')
                app.remove()
                total, apps = App.gets_by_user(req.user.id)
                ret = { 'err': 'ok', 'html': stf('/apps.html', 'app_list', apps=apps) }
                return json.dumps(ret)

    def edit(self, req):
        app = self.app
        if req.get_method() == "POST" and app.can_admin(req.user):
            name = req.get_form_var("app_name", None)
            icon = req.get_form_var("app_icon", None)
            if name or icon:
                filename = icon and icon.tmp_filename
                app.update(name, filename)
                if req.get_form_var("output", None) == 'json':
                    req.response.set_content_type('application/json; charset=utf-8')
                    total, apps = App.gets_by_user(req.user.id)
                    ret = { 'err': 'ok', 'html': stf('/apps.html', 'app_list', apps=apps) }
                    return json.dumps(ret)
        return stf('/apps.html', 'app_edit_dialog', app=app)
