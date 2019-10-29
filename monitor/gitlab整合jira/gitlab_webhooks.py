# -*- coding: utf-8 -*-
# auther: yubb
#创建一个简单站点监听8009端口，webhook会调用此端口
#站点接收POST数据，并将数据传给achive_info文件。

from wsgiref.simple_server import make_server
from achive_info import achive_info
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0
	request_body = environ['wsgi.input'].read(request_body_size)
	print request_body
	info = achive_info(request_body)
	info.check_status()
	return ['api is up! Interface Start Successfully']

httpd = make_server('', 8009, application)  # 监听8009端口
print('Serving HTTP on port 8009...')
httpd.serve_forever()

