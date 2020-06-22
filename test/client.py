#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import grpc
import sys

sys.path.append("../proto")

import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import time
from config.mail_server_config import PORT, HOST


# 记录请求发送邮件的日志
def log_mail_request(receiver, title, content):
    with open('../log/mail_client_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content
        ))


# 记录请求发送邮件的日志
def log_mail_request_err(receiver, title, content, secretkey, err):
    with open('../log/mail_client_send_err.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||secretkey:%s||err:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, secretkey, err
        ))


# RPC专用类（客户端）
class GRPCClient(object):
    def __init__(self):
        server = '%s:%s' % (HOST, PORT)
        # 连接 rpc 服务器
        channel = grpc.insecure_channel(server)
        # 调用 rpc 服务，XxxxxStub 这个类名是固定生成的，参照 mail_pb2_grpc.py
        self.stub = mail_pb2_grpc.MailManagerServiceStub(channel)

    def send_mail(self, mail_data):
        receiver = mail_data['receiver']
        title = mail_data['title']
        content = mail_data['content']
        secretkey = mail_data['secretkey']
        # print(content)
        response = None
        try:
            # s 是一个基于 dict 的实例
            s = mail_pb2.SendTextMailRequest(receiver=receiver, title=title, content=content, secretkey=secretkey)
            log_mail_request(receiver=receiver, title=title, content=content)
            response = self.stub.SendMail(s)
            return response
        except BaseException as e:
            log_mail_request_err(receiver=receiver, title=title, content=content, secretkey=secretkey, err=str(e))
            return {
                'code': 0,
                'msg': 'send error',
                'data': e
            }


# 测试和示例代码
if __name__ == '__main__':
    client = GRPCClient()
    content = ''
    # 这里是测试读取 html 内容（即发送超文本样式），也可以只发纯文本
    with open('./content.html', 'r', encoding='utf-8') as f:
        content = ''.join(f.readlines()).replace(' ', '').replace('\n', '')
    mail_data = {
        'receiver': ['20004604@qq.com', 'qq20004604@icloud.com', '674714966@qq.com', 'zero931025@163.com'],
        'title': '同时发送4个收件人的测试邮件（测试序号：2）',
        'content': '这是一个群发邮件测试的内容》》》内容\n第二行的内容',
        'secretkey': 'Iuiu@8kvEFHPTWMTkp2kYxrH*d^q!s%6'
    }
    res2 = client.send_mail(mail_data)
    print(res2)
