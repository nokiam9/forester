# # -*- coding: utf-8 -*-

from flask import request, render_template, abort
from mongoengine.errors import NotUniqueError

from models import BidNotice

import json, datetime

NOTICE_TYPE_CONFIG = {
    '0': '全部招标公告',
    '1': '单一来源采购公告',
    '2': '采购公告',
    '7': '中标结果公示',
    '3': '资格预审公告',
    '8': '供应商信息收集',
    '99': '供应商公告',
}
PAGE_SIZE = 10

# pylint: disable=no-member
# 所有route的定义，采用add_url_rule（），而不是修饰符，便于将应用隐藏在views.py中
def index():
    return render_template('index.html')

def content_view(nid):
    content = BidNotice.objects(nid=nid).first().notice_content
    if not content:
        abort(status=404)
    else:
        return content


def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.6 (from the example template)"


def notice_page_view(type_id):
    """  View of /notice/pagination/[012378]/?page_id=1 """
    try:
        title = NOTICE_TYPE_CONFIG[type_id]
    except KeyError:
        abort(status=406)   # Unacceptable url para
    page_id=request.args.get('page_id', default=1, type=int)

    # 为了解决order by排序时内存溢出的问题，document的meta定义增加了index
    if type_id == '0' or type_id is None:
        todos_page = BidNotice.objects(). \
            order_by("-published_date", "-timestamp"). \
            paginate(page=page_id, per_page=PAGE_SIZE)
    else:
        todos_page = BidNotice.objects(type_id=type_id). \
            order_by("-published_date", "-timestamp"). \
            paginate(page=page_id, per_page=PAGE_SIZE)

    return render_template('pagination.html',
                           todos_page=todos_page,
                           type_id=type_id,
                           title=title)

'''
    Func: 试图插入一条Notice
'''
def api_post_notice(nid):
    json_data = json.loads(request.get_data().decode("utf-8"))
    try:    # try to insert new record
        BidNotice(
            title = json_data['title'], 
            nid = json_data['nid'],
            notice_type = json_data['notice_type'],
            type_id = json_data['type_id'], 
            spider = json_data['spider'], 
            source_ch = json_data['source_ch'],
            notice_url = json_data['notice_url'],
            # notice_content = json_data['notice_content'], 
            published_date = datetime.datetime.strptime(json_data['published_date'], '%Y-%m-%d'),   # 日期转换

            # 填入API网关当前时间
            timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=8),   
        ).save()               
    except (NotUniqueError):  ## DuplicateKeyError,
        abort(204, 'Dup rec')
    except ValueError as e:
        abort(400, str(e))
    return  'ok', 200
    
def api_get_list_of_empty_content():
    return  'ok', 200

def api_post_notice_content(nid):
    return  'ok', 200