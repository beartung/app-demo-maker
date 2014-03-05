#!/usr/bin/python
# -*- coding: utf-8 -*-

from quixote.errors import TraversalError, AccessError
from libs.template import st, stf

from webapp.models.user import User
from webapp.models.app import App, Screen, Rect
from webapp.models.page import Page, Action

import simplejson as json

_q_exports = []

def _q_index(req):
    app_id = req.get_form_var("app_id", "")
    app = App.get(app_id)

    name = req.get_form_var("name", "")
    x = req.get_form_var("x", 0)
    y = req.get_form_var("y", 0)
    w = req.get_form_var("w", None)
    h = req.get_form_var("h", None)
    x = x and str(x).isdigit() and int(x) or 0
    y = y and str(y).isdigit() and int(y) or 0
    w = w and str(w).isdigit() and int(w) or 0
    h = h and str(h).isdigit() and int(h) or 0

    parent_id = req.get_form_var("parent_id", 0)
    page_type = req.get_form_var("type", Page.TYPE_NORMAL)
    parent = parent_id and Page.get(parent_id)
    rect = None
    if req.get_method() == 'POST':
        if w and h:
            rect = Rect.get(Rect.new(x, y, w, h))
        photo = req.get_form_var("photo", None)
        if name and app.can_admin(req.user):
            filename = photo and photo.tmp_filename
            page_id = Page.new(app, name, rect, filename, parent_id, page_type)
            if req.get_form_var("output", None) == 'json':
                req.response.set_content_type('application/json; charset=utf-8')
                ret = { 'err': 'ok', 'html': stf('/app.html', 'page_list', app=app, req=req) }
                return json.dumps(ret)
    else:
        rect = Rect(0, x*app.zoomout, y*app.zoomout, w*app.zoomout, h*app.zoomout)
        return stf('/app.html', 'page_form', app=app, rect=rect, parent=parent, page_type=page_type)

def _q_lookup(req, id):
    page = Page.get(id)
    if page:
        return PageUI(req, page)
    return TraversalError("no such page")

class PageUI(object):

    _q_exports = ['edit', 'remove', 'add_action', 'remove_action']

    def __init__(self, req, page):
        self.page = page

    def edit(self, req):
        name = req.get_form_var("name", "")
        photo = req.get_form_var("photo", None)
        app = self.page.app
        if app.can_admin(req.user):
            if name and req.get_method() == "POST":
                filename = photo and photo.tmp_filename
                self.page.update(name, filename)
                return json.dumps({'err':'ok', 'html': stf('/app.html', 'page_list', app=app, req=req)})
            return stf('/app.html', 'page_edit_form', page=self.page, req=req)
        return AccessError("need owner")

    def remove(self, req):
        page = self.page
        app = page.app
        if req.get_method() == "POST" and app.can_admin(req.user):
            if req.get_form_var("output", None) == 'json':
                req.response.set_content_type('application/json; charset=utf-8')
                page.remove()
                ret = { 'err': 'ok' }
                return json.dumps(ret)
        return AccessError("need owner")

    def add_action(self, req):
        page = self.page
        app = page.app
        if app.can_admin(req.user):
            x = req.get_form_var('x', None)
            y = req.get_form_var('y', None)
            w = req.get_form_var('w', None)
            h = req.get_form_var('h', None)
            x = x and str(x).isdigit() and int(x) or 0
            y = y and str(y).isdigit() and int(y) or 0
            w = w and str(w).isdigit() and int(w) or 0
            h = h and str(h).isdigit() and int(h) or 0
            type = req.get_form_var('type', None)
            dismiss = req.get_form_var('dismiss', None)
            to_page_id = req.get_form_var('to_page', 0)
            if req.get_method() == "GET":
                rect = Rect(0, x, y, w, h)
                return stf('/app.html', 'action_form', page=page, rect=rect, type=type)
            elif req.get_method() == "POST":
                if req.get_form_var("output", None) == 'json':
                    req.response.set_content_type('application/json; charset=utf-8')
                    rect = Rect.get(Rect.new(x, y, w, h))
                    Action.new(page.id, rect, type, dismiss, to_page_id)
                    ret = { 'err': 'ok' }
                    ret['html'] = stf('/app.html', 'page_worktable', p=page, req=req)
                    return json.dumps(ret)
        return AccessError("need owner")

    def remove_action(self, req):
        page = self.page
        app = page.app
        if req.get_method() == "POST" and app.can_admin(req.user):
            if req.get_form_var("output", None) == 'json':
                req.response.set_content_type('application/json; charset=utf-8')
                action_id = req.get_form_var("action_id", None)
                action = action_id and Action.get(action_id)
                if action:
                    action.remove()
                ret = { 'err': 'ok' }
                return json.dumps(ret)
        return AccessError("need owner")
