#coding=utf-8
# auther: yubb
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#监控两个数据库中的几个表，比较相同表中的条目。如果不同则发送html邮件（包括表格）

mail_host="mail.innodealing.com"
mail_user="bingbing.yu@innodealing.com"
mail_pass="yubb104710"
sender="monitor@innodealing.com"
receivers=['bingbing.yu@innodealing.com',]
def sendmail(message):
    mail_msg = """
    <p>Please check canal_image,There are differences in the number of tables!</p>
    <p>
    <body>
        <table border="0" frame=void>
            <tr>
                <td>表名</td>
                <td>dmdi</td>
                <td>dmdc</td>
            </tr>
            <tr>
                <td>%s</td>
                <td>%d</td>
                <td>%d</td>
            </tr>
        </table>
    </body>
    </p>
    """
    #获取邮件正文
    msg = MIMEText(mail_msg,'html','utf-8')
    msg['From'] = Header("于",'utf8')
    msg['to'] = Header("兵兵",'utf8')
    subject = 'Python SMTP 邮件测试-_-'
    msg['Subject'] = Header(subject,'utf-8')
    notes = msg.as_string()
    #发送邮件
    try:
        server=smtplib.SMTP(mail_host,25)
        server.login(mail_user,mail_pass)
        server.sendmail(mail_user,receivers,notes)
        server.quit()
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "邮件发送失败"

sendmail('测试')
