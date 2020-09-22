# coding=utf-8
__author__ = 'yubb'
# 查询一天内每个域名的访问量前十的IP；
# 统计这些IP访问URL的占比；

import datetime
from elasticsearch import Elasticsearch
import json
import requests