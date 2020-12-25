# coding: utf-8
# auther: yubb
import requests
import os
import re

os.makedirs('./image/', exist_ok=True)


def achieve_url():
    with open(r'C:\Users\Administrator\Desktop\url2.txt', 'r') as f:
        content = f.read().splitlines()
        return content


def request_download(url_lists):
    for url_list in url_lists:
        r = requests.get(url_list)
        name = re.split(r'/', url_list)
        print(name)
        with open('./image/%s' % name[-1], 'wb') as f:
            f.write(r.content)


url_lists = achieve_url()
request_download(url_lists)
