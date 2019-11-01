#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import ssl
import json
import re

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
