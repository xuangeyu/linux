#coding=utf-8
# auther: yubb
import pandas as pd
def convert_to_html(result,title):
    d = {}
    index = 0
    for t in title:
        d[t] = result[index]
        index +=1
    df = pd.DataFrame(d)
    #如数据过长，可能在表格中无法显示，加上pd.set_option语句可以避免这一情况
    pd.set_option('max_colwidth',200)
    df = df [title]
    h =df.to_html(index=False)
    return h

a=({'dm_analysis_indu': 155396, 't_bond_basic_info': 161717, 't_com_info': 8465}, {'dm_analysis_indu': 155396, 't_bond_basic_info': 161717, 't_com_info': 8465})
tit=['表名','dmdi','dmdc']
print a[0].values()
print convert_to_html([a[0].keys(),a[0].values(),a[1].values()],tit)