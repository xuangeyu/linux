#coding=utf-8
__author__ = 'yubb'
import pika
import random

#用户名及密码
auth = pika.PlainCredentials('mq','123456')
#服务器地址，端口，虚拟机，以及上步的用户名及密码
con_info = pika.ConnectionParameters('192.168.138.139','5672','/',auth)
#创建连接
connection = pika.BlockingConnection(con_info)
#创建通道
channel = connection.channel()

'''
#测试发送消息到192.168.138.138的test队列
#产生随机数
number = random.randint(1,1000)
#定义消息信息
body = 'hello world:%s' %number
#发送消息到队列test
channel.basic_publish(exchange='',
                      routing_key='test',
                      body=body)
print "[x] Sent %s" %body
#关闭队列
connection.close()
'''


#接收消息
channel.queue_declare(queue='test',durable=True)
def callback(ch,method,properties,body):
    print " [x] Received %r" % (body,)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume('test',callback)
print '[*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
