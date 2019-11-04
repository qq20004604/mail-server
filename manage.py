#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
import yagmail
from config.mail import MAIL_CONFIG
import grpc
import proto.mail_pb2 as mail_pb2
import proto.mail_pb2_grpc as mail_pb2_grpc
import time

# 邮件服务的端口
PORT = 49999
MAX_WORKERS = 10


# 记录请求发送邮件的日志
def log_mail_request(receiver, title, content, account, pw):
    with open('./log/mail_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw
        ))


# 记录请求发送邮件的错误
def log_mail_request_err(receiver, title, content, account, pw, err):
    with open('./log/mail_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s||err:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw, err
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
        self.account = request.accountw
        self.pw = request.pw

    # 校验逻辑。例如校验账号密码，收件人，邮件标题和正文
    def verify(self):
        vr = self._verify_receiver()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if vr.code is not 200:
            return {
                'code': va.code,
                'msg': va.msg
            }

        va = self._verify_account()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if va.code is not 200:
            return {
                'code': va.code,
                'msg': va.msg
            }

        vc = self._verify_content()
        # 如果返回结果不是200，说明验证失败，返回错误信息
        if vc.code is not 200:
            return {
                'code': va.code,
                'msg': va.msg
            }

        # 此时校验全部通过，允许发送邮件
        return {
            'code': 200,
            'msg': 'success'
        }

    # 校验推送人的账号密码
    def _verify_account(self):
        # 这里进行校验，校验通过返回True，否则返回False
        account = self.account
        pw = self.pw
        # todo 测试时，默认通过，正常情况下应该从内存或者数据库验证一遍
        # 1、验证推送邮件时是否提供账号密码
        # 2、验证账号是否存在
        # 3、验证账号密码是否正确
        return {
            'code': 200,
            'msg': 'success'
        }

    # 校验接受者的邮件地址
    def _verify_receiver(self):
        receiver = self.receiver
        # 校验邮件地址是否合法
        # todo 调试阶段默认正确
        return {
            'code': 200,
            'msg': 'success'
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
    def send_text(self, receiver, title, content):
        ver = self.verify()
        if ver.code is not 200:
            return {
                'code': ver.code,
                'msg': ver.msg
            }
        try:
            # 发送邮件
            self.mail_sender.send(receiver, title, content)
            # 打个日志，记录一下发送的邮件
            log_mail_request(self.receiver, self.title, self.content, self.account, self.pw)
            # 返回处理结果
            return {
                'code': 200,
                'msg': 'success'
            }
        except BaseException as e:
            # 打个日志，记录一下错误的发送信息
            log_mail_request_err(self.receiver, self.title, self.content, self.account, self.pw)
            # 如果抛出异常，说明发送失败了
            return {
                'code': 0,
                'msg': str(e)
            }


# 实现 proto 文件中定义的 GreeterServicer
class Mail(mail_pb2_grpc.MailManagerServiceServicer):
    # 当 proto 文件中定义的 rpc 被触发时（指 rpc SendMail 这个方法），执行本函数
    def SendMail(self, request, context):
        # 初始化实例
        mm = MailManager(request)
        # 发送邮件
        send_result = mm.send_text()
        # 返回处理结果
        return mail_pb2.SendTextMailReply(send_result.code, send_result.msg)


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
    pass
