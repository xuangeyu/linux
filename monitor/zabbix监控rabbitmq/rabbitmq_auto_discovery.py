#coding=utf-8
__author__ = 'yubb'
# 通过rabbitmq的接口获取所有队列
# 将队列名发送给zabbix
import json
import os
import requests
from urllib import urlencode
from sender_info import zabbix_sender

#mq的信息
mq_host="192.168.1.166"
mq_port=15672
mq_user="admin"
mq_pass="odobfBx4UXx2KpFwygAt"
queues_url="http://%s:%d/api/queues" % (mq_host,mq_port)
#zabbix的信息
zab_ser='192.168.1.45'
zab_por=10051
zab_cli='1.187'
#获取rabbitmq的所有队列信息
def achive_info():
    respones=requests.get(url=queues_url,auth=(mq_user,mq_pass))
    # print respones.status_code   查看返回头信息
    data=json.loads(respones.content.decode())
    return data
#定义rabbit类
class rabbit:
    #初始化队列的名字，消息数，消费者数等
    def __init__(self,data):
        self.queue_names=[]
        self.queue_messge={}
        self.queue_unack_messge={}
        self.queue_ready={}
        self.queue_consume={}
        self.zabbix_send = zabbix_sender(zab_ser, zab_por)
        for i in data:
            self.queue_names.append(i['name'])
            self.queue_messge[i['name']]=i['messages']
            self.queue_unack_messge[i['name']]=i['messages_unacknowledged']
            self.queue_ready[i['name']]=i['messages_ready']
            self.queue_consume[i['name']]=i['consumers']
        # print self.queue_messge
        # print self.queue_consume
    #队列名字转换为json格式发给zabbix,实现自动发现
    def auto_discovery_mq(self):
        queues = []
        for i in self.queue_names:
            queues += [{'{#QUE_NAME}': i}]
        queues_data=json.dumps({'data':queues},sort_keys=True,indent=4)
        self.zabbix_send.adddata(zab_cli,'discovery_queues',queues_data) #discovery_queues为zabbix服务端定义的key
    def send_consumer(self):
        for name in self.queue_consume.keys():
            self.zabbix_send.adddata(zab_cli,'consumers[%s]' % name,self.queue_consume[name])
    def send_ready(self):
        for name in self.queue_ready.keys():
            self.zabbix_send.adddata(zab_cli,'messages_ready[%s]' % name,self.queue_ready[name])
    def send_unmgs(self):
        for name in self.queue_unack_messge.keys():
            self.zabbix_send.adddata(zab_cli,'messages_unacknowledged[%s]' % name,self.queue_unack_messge[name])
    def send_msgs(self):
        for name in self.queue_messge.keys():
            self.zabbix_send.adddata(zab_cli,'messages[%s]' % name,self.queue_messge[name])
def main():
    mq=rabbit(achive_info())
    mq.auto_discovery_mq()
    mq.send_consumer()
    mq.send_ready()
    mq.send_unmgs()
    mq.send_msgs()
    response = mq.zabbix_send.send()
    print response
if __name__ == '__main__':
    main()






