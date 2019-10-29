#coding=utf-8

import datetime
from elasticsearch import Elasticsearch

#
today = (datetime.datetime.now()).strftime("%Y.%m.%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y.%m.%d")
now_time=(datetime.datetime.now()  - datetime.timedelta(hours = 8)).strftime('%Y-%m-%dT%H:%M:%S')
past_time= (datetime.datetime.now() - datetime.timedelta(hours = 8) - datetime.timedelta(minutes = 2)).strftime('%Y-%m-%dT%H:%M:%S')
es_url="http://192.168.1.51:9200"

index_name="star-slow-{date}".format(date=today)
index_name2 = "mongodb-slow-log-{date}".format(date=today)
es = Elasticsearch(es_url,timeout=120)

#查询一分钟内的日志量
m_query={
    "query": {
        "bool":{
            "filter":{
                "range": {
                    "@timestamp": {
                        "gte": "%s" %past_time,
                        "lte": "%s" %now_time
                    }
                }
            }
        }
    }
}

def query(db):
    queryData = es.search(index=db,scroll='1m',timeout='5s',size=1000,body=m_query)
    total = queryData["hits"]["total"]
    print "%s 日志数量为：%s"  %(db,total)

def main():
    print "%s到%s查询结果" %(past_time,now_time)
    query(index_name)
    query(index_name2)

if __name__ == "__main__":
    main()

'''
mdata = queryData.get("hits").get("hits")
if not mdata:
    print 'empty'
scroll_id = queryData["_scroll_id"]d
total = queryData["hits"]["total"]
print total
for i in range(total/100):
    res = es.scroll(scroll_id=scroll_id,scroll='5m')
    mdata += res["hits"]["hits"]
    print res
print mdata
'''