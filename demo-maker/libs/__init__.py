#!/usr/bin/python
# -*- coding: utf-8 -*-

from douban.sqlstore import SqlStore

from config import PERM_DIR, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

from datetime import datetime
import traceback
import time
import json
import os

class FileStore(object):

    def __init__(self):
        self.img_dir = os.path.join(PERM_DIR, "img")
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
        self.origin_dir = os.path.join(self.img_dir, "o")
        if not os.path.exists(self.origin_dir):
            os.mkdir(self.origin_dir)
        self.small_dir = os.path.join(self.img_dir, "s")
        if not os.path.exists(self.small_dir):
            os.mkdir(self.small_dir)

    def save_image(self, img, filename, cate="o"):
        img_dir = self.origin_dir
        if cate in ['s', 'small']:
            img_dir = self.small_dir
        filename = os.path.join(img_dir, filename)
        img.save(filename=filename)

filestore = FileStore()

store = SqlStore(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
