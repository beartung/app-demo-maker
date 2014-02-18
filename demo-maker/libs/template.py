# -*- encoding:utf-8

from os.path import join

from mako.lookup import TemplateLookup
from mako import exceptions

from libs.import_obj import import_obj

from config import SITE_DIR, MAKO_FS_CHECK, TMP_DIR

MAKO_CACHE_DIR = join(TMP_DIR, "tmp_mako_0606", "mako_cache")

c = import_obj("c")
request = import_obj("request")

def mylookup():
    _mylookup = TemplateLookup(
        directories=SITE_DIR + '/webapp/templates',
        module_directory=MAKO_CACHE_DIR,
        disable_unicode=True,
        input_encoding='utf8',
        #output_encoding='utf8',
        encoding_errors='ignore',
        default_filters=['str','h'],
        filesystem_checks=MAKO_FS_CHECK,
    )
    return _mylookup

def serve_template(uri, **kwargs):
    _t = mylookup().get_template(str(uri))
    if 'self' in kwargs:
        kwargs.pop('self')
    try:
        return _t.render(c=c._real, **kwargs)
    except Exception, err:
        print "Mako error in %s: %s" % (uri, err)
        print exceptions.text_error_template().render()
        return exceptions.html_error_template().render(full=True)

def _render_tmpl_func(tmpl, func, **kwargs):
    # 先尝试寻找本template中的func
    func = str(func)
    if tmpl.has_def(func):
        _t = tmpl.get_def(func)
    else:
        # 在当前template的parent中寻找该func
        from mako import util
        from mako.template import DefTemplate
        from mako.runtime import Context, _populate_self_namespace

        # disable unicode 状态下生成 context
        buf = util.StringIO()
        context = Context(buf, **kwargs)
        context._with_template = tmpl

        # 将当前的namespace, 如'self', 'next'等放入context
        func_render_body, context = _populate_self_namespace(context, tmpl)

        # 找到当前template的inherits
        self_ns = context['self']
        inherit_m = self_ns.inherits.module

        # 在inherits中寻找该func // mako 模板中为render_xxx
        func_name = "render_%s" % func
        if hasattr(inherit_m, func_name):
            _t = DefTemplate(tmpl, getattr(inherit_m, func_name))
        else:
            _t = None

    if 'self' in kwargs:
        kwargs.pop('self')

    return _t and _t.render(**kwargs) or ''


def serve_template_func(uri, func, **kwargs):
    tmpl = mylookup().get_template(str(uri))
    return _render_tmpl_func(tmpl, func, **kwargs)

st = serve_template
stf = serve_template_func
