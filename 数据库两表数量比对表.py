#coding=utf-8
import pymysql
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.header import Header

#-------------邮件设置----------------------
mail_host="mail.innodealing.com"
mail_user="bingbing.yu@innodealing.com"
mail_pass="yubb104710"
sender="monitor@innodealing.com"
receivers=['bingbing.yu@innodealing.com']

#设置数据库变量
db1 = pymysql.connect("116.62.54.90","sysmanage","dealing@2017","dmdi")
db2 = pymysql.connect("10.0.14.22","dataviewer","dataviewer2016","dmdc")
tab_lists = ['t_bond_basic_info','t_com_info','dm_analysis_indu']

#设置空集合函数中调用
dmdi_tab={}
dmdc_tab={}


#创建表格
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


#设置发送邮件
def sendmail(messages):
    mail_msg = """
    <p>Please check canal_image,There are differences in the number of tables!</p>
    <p>
    <body>
        <table border="0" frame=void>
        %s
        </table>
    </body>
    </p>
    """     %  messages
    msg = MIMEText(mail_msg,'html','utf-8')
    msg['From'] = Header("于",'utf8')
    msg['to'] = Header("兵兵",'utf8')
    subject = 'canal_image检测-_-'
    msg['Subject'] = Header(subject,'utf-8')
    notes = msg.as_string()
    try:
        server=smtplib.SMTP(mail_host,25)
        server.login(mail_user,mail_pass)
        server.sendmail(mail_user,receivers,notes)
        server.quit()
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "邮件发送失败"

#查询表数据量
def tab_count(con,cs):
        cursor = con.cursor()
        sql = "select count(1) from %s"   % cs
        cursor.execute(sql)
        data = cursor.fetchall()
        return data[0][0]
        cursor.close()
        con.close()
#比对数值

def check(name,data1,data2):
        if data1 != data2:
            print "%s table count diff" % name
            dmdi_tab.setdefault(name,data1)
            dmdc_tab.setdefault(name,data2)
        else:
            print "%s table num is ok" % name



def main():
    for tab_name in tab_lists:
        dmdi_data=tab_count(db1,tab_name)
        dmdc_data=tab_count(db2,tab_name)
        check(tab_name,dmdi_data,dmdc_data)
    if dmdi_tab:
        title=['表名','dmdi','dmdc']
        tab_values=[dmdi_tab,dmdc_tab]
        msg=convert_to_html([tab_values[0].keys(),tab_values[0].values(),tab_values[1].values()],title)
        sendmail(msg)
    else:
        print "All table is ok"

if __name__ == "__main__":
    main()