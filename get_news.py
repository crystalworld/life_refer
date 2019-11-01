#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time


sock = socket.socket()

sock.connect(("paper.people.com.cn", 80))

req = "GET /rmrb/html/2019-08/13/nw.D110000renmrb_20190813_2-01.htm HTTP/1.1\r\nConnection: close\r\nHost: paper.people.com.cn\r\n\r\n"
sock.send(req.encode())

data = b''
while True:
    tmp = sock.recv(1024)
    if tmp:
        data += tmp 
    else:
        break

sock.close()
data = data.decode(errors="ignore")
# print(data)

# p1 = data.find("<title>") + len("<title>")
# p2 = data.find("</title>")
# news_title = data[p1:p2]
# print(news_title)


news_title = re.search("<title>(.+?)</title>", data).group(1)

print(news_title)

r = re.search("<!--enpcontent-->(.+?)<!--/enpcontent-->", data, flags=re.S)
data = r.group(1)
data =data.replace("&nbsp;", " ")

r = re.findall("<P>(.*?)</P>", data, flags=re.S)
news_content = '\n'.join(r)
with open(news_title + ".txt", "w") as f:
    f.write(news_content)


 
# 第三方 SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_user="taolang25@foxmail.com"    #用户名
mail_pass="vcnpthnckxosjebf"   #口令
 
 
sender = 'taolang25@foxmail.com'
receivers = ['1134794665@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
message = MIMEText(news_content, 'plain', 'utf-8')
message['From'] = Header("dj", 'utf-8')
message['To'] =  Header("张三", 'utf-8')
 
subject = news_content
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP_SSL(mail_host)  # SMTP over SSL 默认端口号为465
    smtpObj.login(mail_user,mail_pass)  
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("Error: 无法发送邮件", e)
