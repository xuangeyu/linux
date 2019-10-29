#coding=utf-8
import re
'''
文字处理——拼接多个分割符
'''
def go_split(s, symbol):
    # 拼接正则表达式
    symbol = "[" + symbol + "]+"
    # 一次性分割字符串
    print (symbol)
    result = re.split(symbol, s)
    # 去除空字符
    return [x for x in result if x]

if __name__ == "__main__":
    # 根据port获取内存
    s = '12;;7.osjd;.jshdjdknx+'
    # 定义分隔符
    symbol = ';./+'

    result = go_split(s, symbol)
    print(result)