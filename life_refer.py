#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import re
import socket
import ssl
import json
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


# sock = ssl.wrap_socket(socket.socket()) # https
sock = socket.socket()

# sock.connect(("tieba.baidu.com", 443)) # https
sock.connect(("tieba.baidu.com", 80))

req = "GET /hottopic/browse/topicList HTTP/1.1\r\nConnection: close\r\nHost: tieba.baidu.com\r\n\r\n".encode()
sock.send(req)

data = b''
while True:
    tmp = sock.recv(1024)
    if tmp:
        data += tmp
    else:
        break

sock.close()

data = data.decode("unicode_escape", errors="ignore") # \u 编码时用unicode_escape解码；遇到差错时用errors忽略
# print(data)

r = re.findall("topic_name\":\"(.+?)\",", data) # 小括号分组
print(r)

r = re.findall("discuss_num\":(.+?),", data)
print(r)
