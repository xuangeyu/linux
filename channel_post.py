# coding=utf-8
__author__ = 'yubb'

import pymysql
import json
import requests
from urllib import request
import urllib.parse

# mysql 连接信息
my_ip = "192.168.31.233"
my_user = "root"
my_pwd = "123kaibola"
my_db = "flasky"
# api接口
api_url = "https://test-cryolite.memeyule.com/api/v1/app-update/upload-config"


def achieve_channel_info(sql):
    conn = pymysql.connect(host=my_ip, port=3306, user=my_user, passwd=my_pwd, db=my_db)
    cursor = conn.cursor()
    cursor.execute(sql)
    data_fetchall = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_fetchall


def json_info(channel_id, version, not_versions, max_not_version, min_not_version, closeable, update_tittle, update_infos):
    jsontext = {'infos': []}
    if channel_id == "all":
        sql = 'select channl_id,url from apk_url where channl_id in (select channl_id from channl_apk);'
        data = achieve_channel_info(sql)
        for channel_info in data:
            jsontext['infos'].append({
                "channel": "%s" % channel_info[0],
                "apk_url": "%s" % channel_info[1],
                "version_code": version,
                "version_not_force": not_versions,
                "not_force_max": max_not_version,
                "not_force_min": min_not_version,
                "closeable": closeable,
                "desc": {
                    "title": "%s" % update_tittle,
                    "items": update_infos
                }
            })
    else:
        for channel_info in channel_id:
            sql = 'select b.channl_id,a.url from apk_url a left join channl_apk b on a.channl_id = b.channl_id ' \
                   'left join channl_group_cons c on b.id = c.channl_id where c.sync = 1 and ' \
                   'b.channl_id = "%s" limit 1;' % channel_info
            data = achieve_channel_info(sql)
            jsontext['infos'].append({
                "channel": "%s" % channel_info,
                "apk_url": "%s" % data[0][1],
                "version_code": version,
                "version_not_force": not_versions,
                "not_force_max": max_not_version,
                "not_force_min": min_not_version,
                "closeable": closeable,
                "desc": {
                    "title": "%s" % update_tittle,
                    "items": update_infos
                }
            })
    jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '))
    print(jsondata)


def update_api():
    header = {
        'Content-Type': 'application/json'
    }
    json_data = {'infos': [
        {
            "channel": "test_develop",
            "apk_url": "http://dll.kuwyw.com/app/memezhibo_android_aishang10.apk",
            "version_code": 8056,
            "version_not_force": [8052, 8054],
            "not_force_max": 8054,
            "not_force_min": 8052,
            "closeable": True,
            "desc": {
                "title": "10.01 版本更新",
                "items": ["更多美女", "跟你连麦连到嗨"]
            }
        }
    ]}
    response = requests.post(url=api_url, data=json.dumps(json_data), headers=header)
    print(response)
    # postdata = bytes(json.dumps(json_data), 'utf8')
    # print(postdata)
    # request1 = urllib.request.Request(api_url, postdata, headers=header)
    # reponse = urllib.request.urlopen(request1).read()
    # print(request.urlopen(reponse).read().decode('utf-8'))


# def main():
#     # json_data = json_info()
#     update_api()
#
#
# if __name__ == '__main__':
#     main()


