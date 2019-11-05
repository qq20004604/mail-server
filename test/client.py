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
def log_mail_request(receiver, title, content, account, pw):
    with open('../log/mail_client_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw
        ))


# 记录请求发送邮件的日志
def log_mail_request_err(receiver, title, content, account, pw, err):
    with open('../log/mail_client_send_err.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s||err:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw, err
        ))


# RPC专用类（客户端）
class GRPCClient(object):
    def __init__(self):
        server = '%s:%s' % (HOST, PORT)
        # 连接 rpc 服务器
        channel = grpc.insecure_channel(server)
        # 调用 rpc 服务，XxxxxStub 这个类名是固定生成的，参照 mail_pb2_grpc.py
        self.stub = mail_pb2_grpc.MailManagerServiceStub(channel)

    def send_mail(self):
        is_error = False
        error_msg = ''
        receiver = ['test@qq.com']
        title = '剁手器通知'
        content = ''
        account = ''
        pw = ''
        with open('./content.html', 'r', encoding='utf-8') as f:
            content = ''.join(f.readlines()).replace(' ', '').replace('\n', '')
        # print(content)
        response = None
        try:
            # s 是一个基于 dict 的实例
            s = mail_pb2.SendTextMailRequest(receiver=receiver, title=title, content=content, account=account, pw=pw)
            log_mail_request(receiver=receiver, title=title, content=content, account=account, pw=pw)
            response = self.stub.SendMail(s)
        except BaseException as e:
            log_mail_request_err(receiver=receiver, title=title, content=content, account=account, pw=pw, err=str(e))
            return {
                'code': 0,
                'msg': 'send error',
                'data': e
            }
        finally:
            return response


# 测试和示例代码
if __name__ == '__main__':
    client = GRPCClient()
    res2 = client.send_mail()
    print(res2)
