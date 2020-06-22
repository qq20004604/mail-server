#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
import yagmail
from config.mail_server_config import MAIL_CONFIG, PORT, SECRET_KEY
import grpc
import sys
import re

sys.path.append("proto")

import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import time

# GRPC的最大工作线程（应该是线程吧）
MAX_WORKERS = 10


# 记录请求发送邮件的日志
def log_mail_request(receiver, title, content):
    if type(receiver) is list:
        receiver = str(receiver)
    with open('./log/mail_server_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content
        ))


# 记录请求发送邮件的错误
def log_mail_request_err(receiver, title, content, secretkey, err):
    with open('./log/mail_server_send_err.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||secretkey:%s||err:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, secretkey, err
        ))


# 邮件发送类
class MailManager(object):
    # 初始化
    def __init__(self, request):
        self.mail_sender = yagmail.SMTP(user=MAIL_CONFIG['user'], password=MAIL_CONFIG['password'],
                                        host=MAIL_CONFIG['host'])
        self._mixin_request(request)

    # 将request初始化到实例里
    def _mixin_request(self, request):
        self.receiver = request.receiver
        self.title = request.title
        self.content = request.content
        self.secretkey = request.secretkey

    # 校验逻辑。例如校验账号密码，收件人，邮件标题和正文
    def _verify(self):
        vr = self._verify_receiver()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if vr['code'] is not 200:
            return {
                'code': vr['code'],
                'msg': vr['msg']
            }

        va = self._verify_key()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if va['code'] != 200:
            return {
                'code': va['code'],
                'msg': va['msg']
            }

        vc = self._verify_content()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if vc['code'] != 200:
            return {
                'code': va['code'],
                'msg': va['msg']
            }

        # 此时校验全部通过，允许发送邮件
        return {
            'code': 200,
            'msg': 'success'
        }

    # 校验推送人的账号密码
    def _verify_key(self):
        secretkey = self.secretkey
        # 1、验证推送邮件时是否提供账号密码
        # 1.1 没有——》False， code = 404
        # 1.2 有，在 SECRET_KEY 里，返回 True
        # 2. 返回 False
        if secretkey is None:
            return {
                'code': 404,
                'msg': '你必须提供密钥，方能调用邮件服务'
            }
        if secretkey in SECRET_KEY:
            return {
                'code': 200
            }
        return {
            'code': 0,
            'msg': '密钥错误，请联系邮件服务管理员：QQ：20004604'
        }

    # 校验接受者的邮件地址
    def _verify_receiver(self):
        receiver_list = self.receiver
        # 校验邮件地址是否合法
        p = re.compile(r"[^@]+@[^@]+\.[^@]+")
        err_list = []
        for receiver in receiver_list:
            if p.match(receiver) is None:
                err_list.append(receiver)
        if len(err_list) > 0:
            return {
                'code': 0,
                'msg': '邮箱地址：%s ，其格式错误' % str(err_list)
            }

        return {
            'code': 200
        }

    # 校验内容
    def _verify_content(self):
        # 校验标题、内容是否正确
        # todo 调试阶段默认正确
        return {
            'code': 200,
            'msg': 'success'
        }

    # 发送纯文本
    def send_text(self):
        v_info = self._verify()
        if v_info['code'] is not 200:
            return {
                'code': v_info['code'],
                'msg': v_info['msg']
            }
        try:
            if len(self.receiver) <= 1:
                self.receiver = [self.receiver[0], ]
            # 打个日志，记录一下发送的邮件
            log_mail_request(self.receiver, self.title, self.content)
            # 发送邮件
            self.mail_sender.send(self.receiver, self.title, self.content)
            print('send success')
            # 返回处理结果
            return {
                'code': 200,
                'msg': 'success'
            }
        except BaseException as e:
            print('send error')
            # 打个日志，记录一下错误的发送信息
            log_mail_request_err(self.receiver, self.title, self.content, self.secretkey, e)
            # 如果抛出异常，说明发送失败了
            return {
                'code': 0,
                'msg': e
            }


# 实现 proto 文件中定义的 GreeterServicer
class Mail(mail_pb2_grpc.MailManagerServiceServicer):
    # 当 proto 文件中定义的 rpc 被触发时（指 rpc SendMail 这个方法），执行本函数
    def SendMail(self, request, context):
        print('get a mail send request')
        # 初始化实例
        mm = MailManager(request)
        # 发送邮件
        send_result = mm.send_text()
        # 返回处理结果
        return mail_pb2.SendTextMailReply(code=send_result['code'], msg=send_result['msg'])


# 邮件服务
class GRPCServer(object):
    def run(self):
        # 启动 rpc 服务，设置连接池，最大为10个用户
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
        # 设置 Server，并启用响应函数
        mail_pb2_grpc.add_MailManagerServiceServicer_to_server(Mail(), server)
        # 监听本机的 PORT 端口（这里默认配置为49999）
        server.add_insecure_port('[::]:%s' % PORT)
        # 启动服务
        server.start()
        print('server start!')
        # 这个是为了维持 Server 一直在启动。从这里可以推断，上面应该是起了一个新的线程或者进程。
        try:
            while True:
                time.sleep(60 * 60 * 24)  # one day in seconds
        except KeyboardInterrupt:
            # 如果用户手动中断（比如 ctrl + c？）
            server.stop(0)


if __name__ == '__main__':
    # mail = MailManager()
    # mail.send_text(receiver='20004604@qq.com', title='消息通知', content='这个是正文内容啦')
    GRPCServer().run()
