#coding=utf-8
# auther: yubb
#使用snmpwalk获取路由器已开启端口的详细信息（id,name,ip,类型）并存入数据库
import os
import pymysql
import re

hosts=["10.0.1.1","10.0.1.3"]
port_types=["wan","lan","LAN","WAN"]
public='dm'
ver='2c'
#连接数据库
def conndb():
    conn=pymysql.connect("10.0.14.21","zabbix","Zabbix&0524","monvalues")
    cur=conn.cursor()
    return (conn,cur)
#更新或插入数据
def exeupdate(conn,cur,sql):
    sta=cur.execute(sql)
    conn.commit()
    return (sta)
#查询数据
def exequery(cur,sql):
    cur.execute(sql)
    return (cur)
#关闭连接
def connclose(conn,cur):
    cur.close()
    conn.close()
#定义分隔符
def achive_data(msg,x):
    symbol="[\n\ .]+"
    achive = re.split(symbol,msg)
    return (achive[x])
#查询数据库是否存在相同记录
def check_sql(ip,id):
    conn,cur=conndb()
    sql="select * from snmp_router_basic WHERE  host='%s' AND app_id=%d" %(ip,id)
    num=exequery(cur,sql)
    return num.rowcount
#查询端口状态
def check_port_stat(host,id):
    msg=os.popen('/usr/bin/snmpwalk -v %s -c %s %s ifOperStatus' % (ver,public,host))
    for line in msg.readlines():
        if id in line:
            stat=achive_data(line,4)
            if stat == 'up(1)':
                return 1
            else:
                return 0

#获取基础信息方法
def achive_basicinfo():
    for route in hosts:
        msg=os.popen('/usr/bin/snmpwalk -v %s -c %s %s ifDescr' % (ver,public,route))
        for line in msg.readlines():
            for type in port_types:
                if type in line:
                    port_id=achive_data(line,1)
                    port_name=achive_data(line,4)
                    sta=check_port_stat(route,port_id)
                    if sta == 1:
                        num=check_sql(route,int(port_id))
                        if num<1:
                            conn,cur=conndb()
                            sql="insert into snmp_router_basic(name,host,app_id,port_type) values('%s','%s',%d,'%s')" %(port_name,str(route),int(port_id),type)
                            exeupdate(conn,cur,sql)
                            connclose(conn,cur)


#获取路由端口对应ip
def achive_ip():
    for route in hosts:
        conn,cur=conndb()
        sql="select app_id from snmp_router_basic WHERE host = '%s'" % route
        port_ids=exequery(cur,sql)
        connclose(conn,cur)
        for port_id in port_ids:
            msg=os.popen('/usr/bin/snmpwalk -v %s -c %s %s ipAdEntIfIndex' % (ver,public,route))
            condition='INTEGER: %s' % port_id
            for line in msg.readlines():
                if condition in line:
                    ip=achive_data(line,1)+'.'+achive_data(line,2)+'.'+achive_data(line,3)+'.'+achive_data(line,4)
                    conn,cur=conndb()
                    sql="update snmp_router_basic set port_ip = '%s' where host = '%s' and app_id = %d" %(ip,route,port_id[0])
                    exeupdate(conn,cur,sql)
                    connclose(conn,cur)






















