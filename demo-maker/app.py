#!/usr/bin/python
# coding:utf8

import os
import quixote

from webapp import views as controllers
from quixote.qwip import QWIP
from libs.gzipper import make_gzip_middleware
from config import UPLOAD_DIR
import time
import re

class Publisher(quixote.Publisher):
    def __init__(self, *args, **kwargs):
        quixote.Publisher.__init__(self, *args, **kwargs)
        display = 'html' if os.environ.get('DOUBAN_PRODUCTION') else 'plain'
        self.configure(DISPLAY_EXCEPTIONS=display, UPLOAD_DIR=UPLOAD_DIR)

    def start_request(self, request):
        os.environ['SQLSTORE_SOURCE'] = request.get_url()

        resp = request.response
        resp.set_content_type('text/html; charset=utf-8')
        resp.set_header('Expires', 'Sun, 1 Jan 2006 01:00:00 GMT')
        resp.set_header('Pragma', 'no-cache')
        resp.set_header('Cache-Control', 'must-revalidate, no-cache, private')
        request.enable_ajax = False
        request.browser = request.guess_browser_version()
        request.method = request.get_method()
        request.url = '/'
        request.start_time = time.time()
        request.user = None

    def try_publish(self, request, path):
        output = quixote.Publisher.try_publish(self, request, path)
        return output

    def _generate_cgitb_error(self, request, original_response, exc_type, exc_value, tb):
        return "500"

def create_publisher():
    return Publisher(controllers)

app = make_gzip_middleware(QWIP(create_publisher()))
