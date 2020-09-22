#coding=utf-8
__author__ = 'yubb'
# 查询 mysql 中被封的 IP
# 如果 IP 被禁超过 7 天，则对其进行解封
# 配合api_flow_limit.py脚本一起使用

import pymysql
import os
import datetime

# mysql 连接信息
my_ip = "192.168.1.45"
my_user = "grafana"
my_pwd = "123kaibola"
my_db = "grafana_data"
# 调用 Iptables 解封 IP 的服务器地址
ser_list = ["192.168.1.34", "192.168.1.35"]
# IP封禁时间（天）
interval = 7


# 连接 Mysql 并将超限 IP 写入到表中
def mysql_con(types, sql):
    if types == "select":
        conn = pymysql.connect(host=my_ip, port=3306, user=my_user, passwd=my_pwd, db=my_db)
        cursor = conn.cursor()
        cursor.execute(sql)
        data_fetchall = cursor.fetchall()
        cursor.close()
        conn.close()
        return data_fetchall
    elif types == "update":
        conn = pymysql.connect(host=my_ip, port=3306, user=my_user, passwd=my_pwd, db=my_db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


# 解除iptables限制
def block_ip(ip):
    for ser_ip in ser_list:
        # os.system('ssh -p 4811 root@%s "iptables -D INPUT -s %s/32 -j DROP"' % (ser_ip, ip))
        print('ssh -p 4811 root@%s "iptables -D INPUT -s %s/32 -j DROP"' % (ser_ip, ip))


# 查询间隔时间之前的被封IP，调用block_ip解封，并更新其在数据库中的unblock_time时间和block字段
def unseal_ip():
    unseal_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    time_interval = (datetime.datetime.now() - datetime.timedelta(days=interval)).strftime('%Y-%m-%dT%H:%M:%S.000')
    print(unseal_time, time_interval)
    sql = 'select ip from iptables_ip where block = 1 and time < "%s";' % time_interval
    seal_ips = mysql_con("select", sql)
    for ip in seal_ips:
        block_ip(ip[0])
        sql = 'update iptables_ip set unblock_time = "%s", block = 0 where block = 1 and ip = "%s";' %\
              (unseal_time, ip[0])
        mysql_con("update", sql)


def main():
    unseal_ip()


if __name__ == '__main__':
    main()
