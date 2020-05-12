# coding: utf-8
# auther: yubb

from elasticsearch import Elasticsearch
import datetime
import sys
program = str(sys.argv[1])


def get_date(index, max_time, min_time):
    es = Elasticsearch([{"host": "192.168.1.51", "port": 9200}, ])
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": "error",
                            "fields": ["message"]
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "%s" % min_time,
                                "lte": "%s" % max_time
                            }
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index=index, timeout='60s', size=100, body=query)
    total = res['hits']['total']
    return total


def get_time(time_interval, hours_interval=8):
    # 获取es时区的当前时间和time_interval分钟前的时间
    now_time = (datetime.datetime.now() - datetime.timedelta(hours=hours_interval)).strftime('%Y-%m-%dT%H:%M:%S')
    past_time = (datetime.datetime.now() - datetime.timedelta(hours=hours_interval) -
                 datetime.timedelta(minutes=time_interval)).strftime('%Y-%m-%dT%H:%M:%S')
    return now_time, past_time


# 两分钟内的程序报错数量
def err_nums(interval=2):
    now_time, past_time = get_time(interval)
    err_num = get_date(program + '-' + '*', now_time, past_time)
    # print(now_time, past_time)
    print(err_num)


def err_trend(interval=10):
    # 获取现在时间间隔内的报错数量
    now_time, past_time = get_time(interval)
    today_num = get_date(program + '-' + '*', now_time, past_time)
    # 获取昨天对应时间的报错数量
    yesterday_time, yesterday_past_time = get_time(interval, 32)
    yesterday_num = get_date(program + '-' + '*', yesterday_time, yesterday_past_time)
    # 获取前天对应时间的报错数量
    before_yes_time, before_yes_past_time = get_time(interval, 56)
    before_yes_num = get_date(program + '-' + '*', before_yes_time, before_yes_past_time)
    # 获取前两天报错数量的最大值
    max_num = max(yesterday_num, before_yes_num)
    # print(today_num, yesterday_num, before_yes_num)
    if max_num == 0:
        if today_num == 0:
            print(0)
        elif today_num < 10:
            print(1)
        else:
            print(2)
    else:
        if today_num == 0:
            print(0)
        else:
            print(format(float(today_num)/float(max_num), '.2f'))


def main():
    if sys.argv[2] == "err_nums":
        err_nums()
    else:
        err_trend()


if __name__ == '__main__':
    main()

