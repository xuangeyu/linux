# coding=utf-8
__author__ = 'yubb'
# 每五分钟查询elasticsearch的api-memeyule-*索引
# 过滤出状态码为500,502,503等错误
# 如果出现数量超过阈值则发送邮件报警
import datetime
from elasticsearch import Elasticsearch

# 获取今天和昨天日期
today = datetime.datetime.now().strftime("%Y.%m.%d")
yestoday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y.%m.%d")
es_url = "http://192.168.1.51:9200"
time1 = datetime.datetime.now().strftime('%H:%M:%S')


def check_time():
    # 获取es时区的当前时间和5分钟前的时间
    now_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')
    past_time = (datetime.datetime.now() - datetime.timedelta(hours=8) -
                 datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S')
    # 当执行时间在凌晨零点零五分之前查询时，要查询的数据为今天的索引加上昨天的索引数据
    now = datetime.datetime.now()
    zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
    complexs = zero + datetime.timedelta(minutes=5)
    if now < complexs:
        ret = complexs-now
        diff_time = zero-ret-datetime.timedelta(hours=8)
        gt_time = diff_time.strftime('%Y-%m-%dT%H:%M:%S')
        lt_time = now_time
        indexs = ["api-memeyule-%s" % today, "api-memeyule-%s" % yestoday]
        return gt_time, lt_time, indexs
    else:
        gt_time = past_time
        lt_time = now_time
        indexs = ["api-memeyule-%s" % today, ]
        return gt_time, lt_time, indexs


def check_data(indexs, gt_time, lt_time):
    es = Elasticsearch(es_url, timeout=120)
    check_time()
    total_num = 0
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "prefix": {
                            "status.keyword": "5"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gt": "%s" % gt_time,
                                "lt": "%s" % lt_time
                            }
                        }
                    }
                ]
            }
        }
    }
    for index in indexs:
        query_data = es.search(index=index, scroll='1m', timeout='60s', size=10000, body=query)
        total = query_data["hits"]["total"]
        total_num = total_num + total
        print(total)


def main():
    gt_time = check_time()[0]
    lt_time = check_time()[1]
    indexs = check_time()[2]
    print(gt_time, lt_time)
    check_data(indexs, gt_time, lt_time)


if __name__ == '__main__':
    main()
