#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import grpc
import sys

sys.path.append("../proto")

import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import time
from config.mail_server_config import PORT, HOST
from email.mime.text import MIMEText
from email.header import Header


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
    sender = 'LESS信息流'
    receiver = '20004604@qq.com'

    mail_body = ''
    # 这里是测试读取 html 内容（即发送超文本样式），也可以只发纯文本
    with open('./test.html', 'r', encoding='utf-8') as f:
        mail_body = ''.join(f.readlines()).replace(' ', '').replace('\n', '')

    # 邮件主题
    mail_title = '测试邮件，推送时间%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    contents = ['这是一个测试邮件', mail_body, '<a href="https://www.baidu.com">退订这个订阅号2</a>']
    mail_data = {
        'receiver': [receiver],
        'title': '同时发送4个收件人的测试邮件（测试序号：2）',
        'content': contents,
        'secretkey': 'Iuiu@8kvEFHPTWMTkp2kYxrH*d^q!s%6'
    }
    res2 = client.send_mail(mail_data)
    print(res2)
