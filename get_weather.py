#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import datetime

def sock(sock_ip, net_path, find_province):
    sock = socket.socket()
    sock.connect((sock_ip, 80))
    req = ("GET %s HTTP/1.1\r\nConnection: close\r\nHost: %s \r\n\r\n" % (net_path, sock_ip))
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
    return data


def cat(data):
    for i in data:
        # print(i)
        if find_province in i:
            # print(i)
            # print(type(i))
            i = i.split("\"")[-2]
            return i

# 第三方 SMTP 服务
def send_mail(weather_report):
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="taolang25@foxmail.com"    #用户名
    mail_pass="zgrlczmcuvdnfieg"   #口令zgrlczmcuvdnfieg
    
    
    sender = 'taolang25@foxmail.com'
    receivers = ['1134794665@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText(weather_report, 'plain', 'utf-8')
    message['From'] = Header("shuijing", 'utf-8')
    message['To'] =  Header("yours", 'utf-8')
    
    subject = weather_report
    message['Subject'] = Header(subject, 'utf-8')
    
    while True:
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)  # SMTP over SSL 默认端口号为465
            smtpObj.login(mail_user,mail_pass)  
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print("邮件发送成功")
            break
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)


day_time = datetime.date.today() # 获取当前日期
r = str(day_time).split("-", 1)[1].replace("-", '月')
sock_ip = "www.nmc.cn"
net_path = "/f/rest/province"
find_province = "湖北省"
data = sock(sock_ip, net_path, find_province)
data = re.findall("{.*?}", data)
find_city = cat(data)
data = sock(sock_ip, find_city, find_province)
data = re.findall("<tbody>(.*?)</tbody>", data, flags=re.S)
data = re.sub("<.*?>", '',data[1]).replace(" ", '')

with open('今日天气.txt', 'wb') as f:
    f.write(data.encode()) 
    f.close
send_mail(data)
