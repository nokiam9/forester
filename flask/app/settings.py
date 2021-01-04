# -*- coding: utf-8 -*-
import os 

# MONGODB_SETTINGS = {
#     'db': 'cmccb2b',
#     'username': os.getenv('MONGODB_USERNAME'),
#     'password': os.getenv('MONGODB_PASSWORD'),
#     'host': os.getenv('MONGODB_HOST'),
#     'port': int(os.getenv('MONGODB_PORT')),
#     'connect': False,  # set for pymongo bug fix
#     'authentication_source': 'admin', # set authentication source database， default is MONGODB_NAME
# }

MONGODB_SETTINGS = {
    'db': 'cmccb2b',
    'username': 'root',
    'password': 'forester',
    'host': '127.0.0.1',
    'port': 27017,
    'connect': False,  # set for pymongo bug fix
    'authentication_source': 'admin', # set authentication source database， default is MONGODB_NAME
}

# SECRET_KEY = "flask+mongoengine=<3"     # flask-debug必须设置该参数，为session提供加密处理

# DEBUG_TB_INTERCEPT_REDIRECTS = False
