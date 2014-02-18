#!/usr/bin/python
# -*- coding: utf-8 -*-

from quixote.errors import TraversalError, AccessError
from libs.template import st, stf
from webapp.models.user import User
from webapp.models.app import App, Screen, DEFAULT_SCREEN

from webapp.views.utils import is_validate_email, check_session, set_session, expire_session

_q_exports = ["login", "app", "page", "mpage", "logout"]

def logout(req):
    expire_session(req)
    return req.redirect("/")

def _q_access(req):
    check_session(req)

def _q_index(req):
    if not req.user:
        return req.redirect('/login')
    return demos(req)

def demos(req):
    total, apps = App.gets_by_user(req.user.id)
    screens = [DEFAULT_SCREEN] + Screen.gets()
    return st("/apps.html", **locals())

def login(req):
    email = req.get_form_var("email", '').rstrip()
    if req.get_method() == 'POST':
        password = req.get_form_var("password", '')
        error = None
        if not is_validate_email(email):
            error = "请输入合法的邮箱"
        if not password:
            error = "请输入密码"
        elif len(password) < 4 or not password.isalnum():
            error = "密码请用长于4位的字母数字组合"
        if not error:
            u = User.get_by_email(email)
            if req.get_form_var("login", None):
                if not u:
                    error = "该邮箱还未注册"
                else:
                    u = User.login(email, password)
                    if u:
                        set_session(req, u)
                        return req.redirect("/")
                    else:
                        error = "邮箱和密码不匹配"
            elif req.get_form_var("register", None):
                if u:
                    error = "该邮箱已经注册，请直接登录"
                else:
                    u = User.register(email, password)
                    if u:
                        set_session(req, u)
                        return req.redirect("/")
                    else:
                        error = "注册失败..."
    return st("/login.html", **locals())
