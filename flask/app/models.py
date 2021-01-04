# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine

db = MongoEngine()  # 初始化数据库连接db

# pylint: disable=no-member
class BidNotice (db.Document):
    meta = {
        # 'db_alias': 'cmccb2b-db-alias',
        'collection': 'BidNotice',              # 设置collection名称，默认是model的名字
        'indexes': [                            # 设置index
            ("-published_date", "-timestamp"),  # 用于flask的列表排序
            "type_id",                          # 用于flask的列表选择
            "-timestamp",                       # 用于xunsearch的update index
        ],
    }
    _id = db.StringField()                      # 必须增加，不然打开已存在的table时会报错
    nid = db.StringField(unique=True)           # 主键
    title = db.StringField()
    notice_type = db.StringField()
    source_ch = db.StringField()
    notice_content = db.StringField()
    published_date = db.DateTimeField()
    timestamp = db.DateTimeField()
    reminded_time = db.DateTimeField()
    type_id = db.StringField()
    spider = db.StringField()
    notice_url = db.StringField()
    # attachment_urls = db.ListField(required=False)
    # attachment_files = db.ListField(required=False)

    def __repr__(self):
        return 'nid=%s, title=%s' % (self.nid, self.title)
