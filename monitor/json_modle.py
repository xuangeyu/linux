#encoding=utf8
# auther: yubb

import os
import json

r = file('/usr/local/script/ha/web.txt')
devices = []
for f in r.readlines():
    devices.append({"{#SITENAME}": f.strip()})
print json.dumps({'data': devices}, sort_keys=True, indent=4)


'''
web.txt中文件内容为以下
www.baidu.com
www.sina.com.cn
www.pingan.com.cn
www.weibo.com

'''