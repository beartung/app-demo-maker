# coding: utf-8

from os import path

SITE = "http://m.dapps.douban.com"
SITE_COOKIE = "dadm"
DOMAIN = ".douban.com"

MAKO_FS_CHECK = True

SITE_DIR = path.dirname(path.abspath(__file__))

UPLOAD_DIR = '/tmp/quixote_upload'
TMP_DIR = '/tmp'
PERM_DIR = '/tmp'

DB_HOST = '127.0.0.1'
DB_USER = 'demo'
DB_PASSWORD = ''
DB_NAME = 'demo'

try:
    from local_config import *
except ImportError:
    pass
