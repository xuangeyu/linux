# coding=utf-8
__author__ = 'yubb'
# 查询一天内的安卓上报，每天检查一次，触发以下条件报警。
# 单用户重连一天超过100次报警；
# 最新版本重连超过新版本上报的1%报警；
# 最新版本每天重连用户数超过2000报警；

import datetime
from elasticsearch import Elasticsearch
import json
import requests

# 重连率报警阈值
rate_threshold = 0.01
# 单个用户重连次数报警阈值
recon_threshold = 100
# 每天重连用户数报警阈值
reco_users_threshold = 2000
# 查询时间间隔（小时）
time_interval = 24
# es 地址
es_url = "http://192.168.1.52:9200"
today = datetime.datetime.now().strftime("%Y.%m.%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y.%m.%d")


# 获取查询索引和查询时间
def check_time():
    # 获取es时区的当前时间和time_interva前的时间
    now_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')
    past_time = (datetime.datetime.now() - datetime.timedelta(hours=8) - datetime.timedelta(hours=time_interval))\
        .strftime('%Y-%m-%dT%H:%M:%S')
    print(now_time, past_time)
    return past_time, now_time


# 获取最新的版本
def achieve_version(gt_time, lt_time):
    es = Elasticsearch(es_url)
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "version": {
                "terms": {
                    "field": "app_version.keyword"
                }
            }
        }
    }
    query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=query)
    version_list = []
    for version in query_data['aggregations']['version']['buckets']:
        version_list.append(version['key'])
    return max(version_list)


# 获取最新版本的重连率
def achieve_rate(gt_time, lt_time, version):
    es = Elasticsearch(es_url)
    total_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "app_version": "%s" % version
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        }
    }
    total_query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=total_query)
    total_nums = total_query_data['hits']['total']['value']
    recon_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "app_version.keyword": "%s" % version
                        }
                    },
                    {
                        "term": {
                            "event_type.keyword": "socket_reconnect"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        }
    }
    recon_query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=recon_query)
    recon_nums = recon_query_data['hits']['total']['value']
    print(recon_nums, total_nums)
    print("%s 版本重连率为: %.4f" % (version, recon_nums/total_nums))
    return recon_nums/total_nums


# 获取全部版本重连率
def achieve_all_rate(gt_time, lt_time):
    es = Elasticsearch(es_url)
    total_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        }
    }
    total_query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=total_query)
    total_nums = total_query_data['hits']['total']['value']
    recon_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "event_type.keyword": "socket_reconnect"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        }
    }
    recon_query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=recon_query)
    recon_nums = recon_query_data['hits']['total']['value']
    print(recon_nums, total_nums)
    print("总聊天重连率为: %.4f" % (recon_nums/total_nums))
    return recon_nums/total_nums


# 获取最新版本聊天重连次数大于100的user_id
def achieve_recon_nums(gt_time, lt_time, version):
    es = Elasticsearch(es_url)
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "app_version.keyword": "%s" % version
                        }
                    },
                    {
                        "term": {
                            "event_type.keyword": "socket_reconnect"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "reconnect_id": {
                "terms": {
                    "field": "user_id.keyword",
                    "order": {
                        "_count": "desc"
                    },
                    "size": 10
                }
            }
        }
    }
    query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=query)
    user_id_num_dict = {}
    for user_id in query_data['aggregations']['reconnect_id']['buckets']:
        if user_id['doc_count'] > recon_threshold:
            user_id_num_dict[user_id['key']] = user_id['doc_count']
    print("%s 版本聊天重连次数超过100次的用户列表 %s" % (version, user_id_num_dict))
    return user_id_num_dict


# 获取最新版本发生重连的用户数
def achieve_recon_total(gt_time, lt_time, version):
    es = Elasticsearch(es_url)
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "app_version.keyword": "%s" % version
                        }
                    },
                    {
                        "term": {
                            "event_type.keyword": "socket_reconnect"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % gt_time,
                                "lte": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "reconnect_id": {
                "cardinality": {
                    "field": "user_id.keyword"
                }
            }
        }
    }
    query_data = es.search(index="malog-*", scroll='1m', timeout='20s', body=query)
    print("%s 版本重连用户数为 %s" % (version, query_data['aggregations']['reconnect_id']['value']))
    return query_data['aggregations']['reconnect_id']['value']


# 发送钉钉报警
def send_dinging(text):
    headers = {"Content-Type": "application/json;charset=utf-8"}
    json_text = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    print(requests.post(
        'https://oapi.dingtalk.com/robot/send?'
        'access_token=37b461aa35ad3fc1cd03ce6388b58ffedd9057ae29a7bba67b99212156725c6c',
        json.dumps(json_text), headers=headers).content)


def main():
    gt_time, lt_time = check_time()
    version = achieve_version(gt_time, lt_time)
    all_rate = achieve_all_rate(gt_time, lt_time)
    version_rate = achieve_rate(gt_time, lt_time, version)
    recon_dict = achieve_recon_nums(gt_time, lt_time, version)
    recon_user = achieve_recon_total(gt_time, lt_time, version)
    if version_rate > rate_threshold or recon_user > reco_users_threshold:
        if len(recon_dict) > 0:
            text = "总聊天重连率为: %.4f%% \n \n%s 版本重连率为: %.4f%% \n \n%s 版本聊天重连次数超过100次的用户列表 %s \n \n%s 版本重连用户数为: %s" % (
                all_rate * 100, version, version_rate * 100, version, recon_dict, version, recon_user)
            send_dinging(text)
        else:
            text = "总聊天重连率为: %.4f%% \n \n%s 版本重连率为: %.4f%% \n \n%s 版本重连用户数为: %s" % (
                all_rate * 100, version, version_rate * 100, version, recon_user)
            send_dinging(text)
    else:
        if len(recon_dict) > 0:
            text = "总聊天重连率为: %.4f%% \n \n%s 版本重连率为: %.4f%% \n \n%s 版本聊天重连次数超过100次的用户列表 %s \n \n%s 版本重连用户数为: %s" % (
                all_rate * 100, version, version_rate * 100, version, recon_dict, version, recon_user)
            send_dinging(text)
        else:
            pass


if __name__ == '__main__':
    main()
