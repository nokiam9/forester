from pyecharts import Bar, Pie
from pyecharts_javascripthon.api import TRANSLATOR

from flask import render_template
from mongoengine.queryset.visitor import Q
from models import BidNotice

import datetime


REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# pylint: disable=no-member
def chart_view01():
    # 从mongo中获取数据
    (x, y) = get_records_group_by_published_date(days_before=-30)

    # 设置bar图形的基本属性
    bar = Bar("招标公告发布趋势图", "From: cmccb2b")
    bar.use_theme('light')
    bar.add("发布日期", x, y,                   # 从Mongo读取的数据存放在这里
            is_stack=False,
            is_datazoom_show=True,             # 设置bar图形的datazoom的拖拽效果
            datazoom_type="both",
            datazoom_range=[80, 100])
    javascript_snippet = TRANSLATOR.translate(bar.options)  # 将bar的属性设置翻译为js脚本

    # bar.print_echarts_options()                  # 该行只为了打印配置项，方便调试时使用
    return render_template(
        "pyecharts.html",                                       # 自定义，位于templates/的模版文件
        chart_id=bar.chart_id,                                 # 默认设置，
        host=REMOTE_HOST,                                       # 常量定义，存放js文件的url地址
        renderer=bar.renderer,                                 # 默认设置，
        my_width="100%",                                        # 默认设置，定义图表的宽度
        my_height=600,                                          # 默认设置，定义图表的高度
        custom_function=javascript_snippet.function_snippet,    # 默认设置，保存图片的方法，似乎基于node.js
        options=javascript_snippet.option_snippet,              # 默认设置，
        script_list=bar.get_js_dependencies(),                 # 默认设置，需要动态加载的js文件
    )


def chart_view02():
    # 从mongo中获取数据
    (x, y) = get_records_group_by_source_ch()

    bar = Bar("发布单位分析图")
    bar.add("发布单位", x, y,
            is_label_show=True,
            is_datazoom_show=True,
            datazoom_type='both',
            datazoom_range=[0, 20])
    javascript_snippet = TRANSLATOR.translate(bar.options)  # 将bar的属性设置翻译为js脚本

    return render_template(
        template_name_or_list="pyecharts.html",
        chart_id=bar.chart_id,
        host=REMOTE_HOST,
        renderer=bar.render,
        my_width="100%",  # 默认设置，定义图表的宽度
        my_height=600,  # 默认设置，定义图表的高度
        custom_function=javascript_snippet.function_snippet,  # 默认设置，保存图片的方法，似乎基于node.js
        options=javascript_snippet.option_snippet,  # 默认设置，
        script_list=bar.get_js_dependencies(),  # 默认设置，需要动态加载的js文件
    )


def chart_view03():
    # 从mongo中获取数据
    (x, y) = get_records_group_by_notice_type()

    # 设置bar图形的基本属性
    pie = Pie("公告类型分析图", "From: cmccb2b")
    pie.use_theme('light')
    pie.add("公告类型", x, y, is_stack=False)  # 从Mongo读取的数据存放在这里

    javascript_snippet = TRANSLATOR.translate(pie.options)  # 将bar的属性设置翻译为js脚本
    # pie.print_echarts_options()                  # 该行只为了打印配置项，方便调试时使用

    return render_template(
        "pyecharts.html",  # 自定义，位于templates/的模版文件
        chart_id=pie.chart_id,  # 默认设置，
        host=REMOTE_HOST,  # 常量定义，存放js文件的url地址
        renderer=pie.renderer,  # 默认设置，
        my_width="100%",  # 默认设置，定义图表的宽度
        my_height=600,  # 默认设置，定义图表的高度
        custom_function=javascript_snippet.function_snippet,  # 默认设置，保存图片的方法，似乎基于node.js
        options=javascript_snippet.option_snippet,  # 默认设置，
        script_list=pie.get_js_dependencies(),  # 默认设置，需要动态加载的js文件
    )


def chart_view04():
    # 从mongo中获取数据
    (x, y) = get_records_group_by_timestamp(days_before=-30)

    # 设置bar图形的基本属性
    bar = Bar("招标公告爬取时间图", "From: cmccb2b")
    bar.use_theme('light')
    bar.add("爬取日期", x, y,  # 从Mongo读取的数据存放在这里
            is_stack=False,
            is_datazoom_show=True,  # 设置bar图形的datazoom的拖拽效果
            datazoom_type="both",
            datazoom_range=[80, 100])
    javascript_snippet = TRANSLATOR.translate(bar.options)  # 将bar的属性设置翻译为js脚本
    # bar.print_echarts_options()                  # 该行只为了打印配置项，方便调试时使用

    return render_template(
        "pyecharts.html",  # 自定义，位于templates/的模版文件
        chart_id=bar.chart_id,  # 默认设置，
        host=REMOTE_HOST,  # 常量定义，存放js文件的url地址
        renderer=bar.renderer,  # 默认设置，
        my_width="100%",  # 默认设置，定义图表的宽度
        my_height=600,  # 默认设置，定义图表的高度
        custom_function=javascript_snippet.function_snippet,  # 默认设置，保存图片的方法，似乎基于node.js
        options=javascript_snippet.option_snippet,  # 默认设置，
        script_list=bar.get_js_dependencies(),  # 默认设置，需要动态加载的js文件
    )

def get_records_group_by_published_date(days_before=-7):
    k, v = [], []
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # TimeZone 8
    for t0 in _get_days_list(now, days_before):
        t1 = t0 + datetime.timedelta(days=1)
        records = BidNotice.objects(Q(published_date__lte=t1) & Q(published_date__gte=t0)).count()
        k.append(t0.strftime('%Y-%m-%d'))
        v.append(records)
    return k, v

def get_records_group_by_timestamp(days_before=-7):
    k, v = [], []
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # TimeZone 8
    for t0 in _get_days_list(now, days_before):
        t1 = t0 + datetime.timedelta(days=1)
        records = BidNotice.objects(Q(timestamp__lte=t1) & Q(timestamp__gte=t0)).count()
        k.append(t0.strftime('%Y-%m-%d'))
        v.append(records)
    return k, v

def get_records_group_by_source_ch():
    k, v = [], []
    cursor = BidNotice.objects().aggregate(
        {"$group": {"_id": "$source_ch", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    )
    for doc in cursor:
        k.append(doc['_id'])
        v.append(doc['count'])
    return k, v

def get_records_group_by_notice_type():
    k, v = [], []
    cursor = BidNotice.objects().aggregate(
        {"$group":
            {"_id": "$notice_type", "count":
                {"$sum": 1}
                }
            }
    )
    for doc in cursor:
        k.append(doc['_id'])
        v.append(doc['count'])
    return k, v

"""
Function: 获得t0为基准的UTCTime日期序列数组，时间元素固定为0h0m0s，并按升序排列
    days_delta为正数时，［t0, t0+1day...］; 为负数时，［...,t0-1day,t0］
"""
def _get_days_list(base_time, days_delta):
    arr = []
    t0 = datetime.datetime(base_time.year, base_time.month, base_time.day)
    if days_delta > 0:
        for i in range(0, days_delta+1):
            t = t0 + datetime.timedelta(days=i)
            arr.append(t)
    else:
        for i in range(days_delta, 1):
            t = t0 + datetime.timedelta(days=i)
            arr.append(t)
    return arr



