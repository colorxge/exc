# smtplib 发送邮件流程
# 连接到smtp服务器
smtp = smtplib.SMTP('smtp.qq.com', 25)

# 发送SMTP的'hello'信息
smtp.ehlo()
Out[24]: 
(250,
 b'smtp.qq.com\nPIPELINING\nSIZE 73400320\nSTARTTLS\nAUTH LOGIN PLAIN\nAUTH=LOGIN\nMAILCOMPRESS\n8BITMIME')

# 将当前会话加密
smtp.starttls()
Out[25]: (220, b'Ready to start TLS')

# 登陆到SMTP服务器（密码为SMTP服务第三方授权码）
smtp.login('4****1@qq.com', 'b****h')
Out[26]: (235, b'Authentication successful')

# 发送邮件
smtp.sendmail('4xxx2@qq.com', 'xixxx@163.com', 'Subject:this is test\nthis is a')
Out[27]: {}

# 关闭连接
smtp.quit()

# email 构造邮件
from email.mime.text import MIMEText


def send_mail(fromuser, password, toaddr, title, msg):
    msg = MIMEText(msg)
    msg['Subject'] = title
    msg['From'] = fromuser
    msg['To'] = toaddr
    
    smtp = smtplib.SMTP(SEMP_SERVER, SERVER_PORT)
    try:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_addr, password)
        smtp.sendmail(from_addr, to_add, msg.as_string())
    except Exception:
        raise
    finally:
        smtp.quit()


send_mail(from_addr, password, to_add, title, msg)

# 发送附件表格（构造一个APP对象）
msg = MIMEMultipart()
msg['Subject'] = title
msg['From'] = from_addr
msg['To'] = to_addr
msg.attach(MIMEText('kabuka'))
with open('D:\\dsb.xlsx', 'rb') as f:
    a = MIMEApplication(f.read())
    a.add_header('Content-Disposition', 'attachment', filename='xxx.xlsx')
    msg.attach(a)


s = smtplib.SMTP('smtp.qq.com', 25)
s.ehlo()
s.starttls()
s.login(from_addr, password)
s.sendmail(from_addr, to_addr, msg.as_string())
s.quit()


import yagmail


yag = yagmail.SMTP(user='4xxx@qq.com', password='bxxxxh', host='smtp.qq.com')

contents = ['This is the body', '   D:\\dsdfb.xlsx']

yag.send('xxx9@163.com', 'subject', contents)
yag.close()


