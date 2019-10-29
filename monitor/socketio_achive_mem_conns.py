#!/usr/local/python2.7/bin/python

#coding=utf-8
# auther: yubb
import os
import sys
import re

port=sys.argv[1]
stat=sys.argv[2]

'''
def check_mem(port):
	msg=os.popen('/usr/local/bin/pm2 list')
	for lines in msg.readlines():
        	if port in lines:
			symbol="[\xe2\x94\x82\ ]+"
			avichive=re.split(symbol, lines)
			print avichive[9]
'''

#根据端口获取内存使用量
def check_mem(port):
        msg=os.popen('/usr/local/bin/pm2 list')
        for lines in msg.readlines():
                if port in lines:
                        symbol="[\xe2\x94\x82\ ]+"  #拼接分割符
                        avichive=re.split(symbol, lines)
                        print avichive[9]

#根据端口获取连接数
def check_net(port):
	msg=os.popen('netstat -ant')
	count=0
	for lines in msg.readlines():
		if port in lines:
			count=count+1
	print count

if __name__ == "__main__":
	if stat == "mem":
		check_mem(port)
	elif stat == "conns_num":
		check_net(port)
