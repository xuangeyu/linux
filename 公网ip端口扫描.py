#coding=utf-8
# auther: yubb
#过滤nmap扫描结果文件，将结果发送到固定邮箱

import re
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#报告设置
file = open(r'F:\20190618.log')
mess = file.read()
file.close()
mess_1= mess.split("Nmap scan")   #定义段落分割符（分割后内容被分为一个主机一段）
tit=["端口","协议","状态","服务"]

#邮件设置
mail_host="smtp.exmail.qq.com"
mail_user="redmine@2339.com"
mail_pass="123kaibola"
receivers=['bingbing.yu@2339.com']
#定义表格生成函数
def convert_to_html(result,title,tab_width):
    d = {}
    index = 0
    for t in title:
        d[t] = result[index]
        index +=1
    df = pd.DataFrame(d)
    #如数据过长，可能在表格中无法显示，加上pd.set_option语句可以避免这一情况
    pd.set_option('max_colwidth',200)
    pd.set_option('display.colheader_justify','center')
    df = df [title]
    h =df.to_html(index=False,col_space=tab_width)  #col_space设置列宽（http://pandas.pydata.org/pandas-docs/version/0.19.0/generated/pandas.DataFrame.to_html.html#）
    return h
#获取表格具体信息函数
def achive_info():
    i=1
    a=''
    while i < len(mess_1):
        mess_info =  mess_1[i]
        p_ip = r"report for .+"
        ip_info = re.compile(p_ip)
        host_ip = ip_info.findall(mess_info)   #获取的主机ip信息
        p_info= r"[0-9].+/tcp.+|[0-9].+/udp.+"
        info = re.compile(p_info)
        host_info=info.findall(mess_info)
        j = 0
        port_list=[]
        type_list=[]
        stat_list=[]
        server_list=[]
        while j < len(host_info):
            port=re.split(r'[/\s]\s*',host_info[j])[0]    #每个主机开放端口的list下同
            type=re.split(r'[/\s]\s*',host_info[j])[1]
            stat=re.split(r'[/\s]\s*',host_info[j])[2]
            server=re.split(r'[/\s]\s*',host_info[j])[3]
            port_list.append(port)
            type_list.append(type)
            stat_list.append(stat)
            server_list.append(server)
            j = j + 1
        b=convert_to_html([host_ip],['主机IP'],618)        #生成每个主机ip表格的html语句
        c=convert_to_html([port_list,type_list,stat_list,server_list],tit,150)   #生成每个主机具体信息表格的html语句
        i = i + 1
        a=a+b+c #将所有主机及具体信息的表格的html语句加在一起
    return a
#生成html并发送语句
def sendmail(messages):
    mail_msg = """
    <p>
        <center>
            <span style="background:green;color:yellow;font-size:37px;">The following is the scanned Report</span>
        </center>
    </p>
    <p>
        <center>
            <body>
                %s
            </body>
        </center>
    </p>
    """     %  messages
    msg = MIMEText(mail_msg,'html','utf-8')
    msg['From'] = Header("nmap检测",'utf8')
    msg['to'] = Header("运维",'utf8')
    subject = '阿里云NMAP端口扫描报告-_-'
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

def main():
    sendmail(achive_info())

if __name__ == '__main__':
    main()





#文件内容示例如下：
# Starting Nmap 6.40 ( http://nmap.org ) at 2019-06-18 14:50 CST
# Nmap scan report for 42.62.80.34
# Host is up (0.039s latency).
# Not shown: 65530 filtered ports
# PORT     STATE  SERVICE
# 21/tcp   closed ftp
# 80/tcp   open   http
# 443/tcp  open   https
# 2121/tcp open   ccproxy-ftp
# 4811/tcp open   unknown
# 2222/udp open   unknown
#
# Nmap scan report for 42.62.80.35
# Host is up (0.038s latency).
# Not shown: 65531 filtered ports
# PORT     STATE  SERVICE
# 21/tcp   closed ftp
# 80/tcp   open   http
# 443/tcp  open   https
# 4811/tcp open   unknown
# 2222/udp closed   unknown
#
# Nmap scan report for 42.62.80.36
# Host is up (0.038s latency).
# Not shown: 65533 filtered ports
# PORT    STATE  SERVICE
# 80/tcp  closed http
# 443/tcp closed https
#
# Nmap scan report for 42.62.80.39
# Host is up (0.038s latency).
# Not shown: 65530 closed ports
# PORT      STATE SERVICE
# 80/tcp    open  http
# 443/tcp   open  https
# 1311/tcp  open  rxmon
# 4811/tcp  open  unknown
# 19876/tcp open  unknown
#
# Nmap scan report for admin.memeyule.com (42.62.80.40)
# Host is up (0.038s latency).
# Not shown: 65530 filtered ports
# PORT     STATE  SERVICE
# 21/tcp   closed ftp
# 80/tcp   open   http
# 443/tcp  open   https
# 2121/tcp closed ccproxy-ftp
# 4811/tcp open   unknown
#
# Nmap scan report for 42.62.80.41
# Host is up (0.039s latency).
# Not shown: 65528 filtered ports
# PORT     STATE SERVICE
# 80/tcp   open  http
# 443/tcp  open  https
# 6010/tcp open  x11
# 6020/tcp open  unknown
# 6110/tcp open  softcm
# 6120/tcp open  unknown
# 9527/tcp open  unknown
#
# Nmap scan report for 42.62.80.42
# Host is up (0.039s latency).
# Not shown: 65533 filtered ports
# PORT    STATE SERVICE
# 80/tcp  open  http
# 443/tcp open  https
#
# Nmap scan report for 42.62.80.43
# Host is up (0.038s latency).
# Not shown: 65530 filtered ports
# PORT     STATE  SERVICE
# 80/tcp   closed http
# 90/tcp   closed dnsix
# 4811/tcp closed unknown
# 6010/tcp closed x11
# 6020/tcp closed unknown
#
# Nmap scan report for 42.62.80.45
# Host is up (0.038s latency).
# Not shown: 65530 filtered ports
# PORT     STATE  SERVICE
# 80/tcp   open   http
# 443/tcp  open   https
# 4811/tcp closed unknown
# 6010/tcp open   x11
# 6110/tcp open   softcm
#
# Nmap scan report for 42.62.80.50
# Host is up (0.038s latency).
# Not shown: 65520 closed ports
# PORT     STATE SERVICE
# 443/tcp  open  https
# 1311/tcp open  rxmon
# 4811/tcp open  unknown
# 6010/tcp open  x11
# 6011/tcp open  unknown
# 6012/tcp open  unknown
# 6013/tcp open  unknown
# 6020/tcp open  unknown
# 6030/tcp open  x11
# 6050/tcp open  arcserve
# 6110/tcp open  softcm
# 6120/tcp open  unknown
# 6130/tcp open  unknown
# 7278/tcp open  oma-dcdocbs
# 8080/tcp open  http-proxy
#
# Nmap scan report for 42.62.80.51
# Host is up (0.038s latency).
# Not shown: 65518 closed ports
# PORT      STATE SERVICE
# 80/tcp    open  http
# 443/tcp   open  https
# 1311/tcp  open  rxmon
# 4811/tcp  open  unknown
# 6010/tcp  open  x11
# 6011/tcp  open  unknown
# 6012/tcp  open  unknown
# 6013/tcp  open  unknown
# 6020/tcp  open  unknown
# 6030/tcp  open  x11
# 6050/tcp  open  arcserve
# 6110/tcp  open  softcm
# 6120/tcp  open  unknown
# 6130/tcp  open  unknown
# 8080/tcp  open  http-proxy
# 54188/tcp open  unknown
# 62209/tcp open  unknown
#
# Nmap scan report for 42.62.110.162
# Host is up (0.038s latency).
# Not shown: 65528 filtered ports
# PORT     STATE  SERVICE
# 80/tcp   open   http
# 443/tcp  open   https
# 4811/tcp closed unknown
# 8006/tcp closed unknown
# 8106/tcp open   unknown
# 8107/tcp open   unknown
# 9001/tcp open   tor-orport
#
# Nmap scan report for 42.62.110.163
# Host is up (0.039s latency).
# Not shown: 65527 filtered ports
# PORT     STATE  SERVICE
# 80/tcp   open   http
# 443/tcp  open   https
# 4811/tcp closed unknown
# 8006/tcp closed unknown
# 8106/tcp open   unknown
# 8107/tcp open   unknown
# 9001/tcp open   tor-orport
# 9050/tcp closed tor-socks
#
# Nmap done: 14 IP addresses (13 hosts up) scanned in 503.96 seconds





