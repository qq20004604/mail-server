#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yagmail
from config import MAIL_CONFIG


# 链接邮箱服务器

class MailManager(object):
    # 初始化
    def __init__(self):
        self.mail_sender = yagmail.SMTP(user=MAIL_CONFIG['user'], password=MAIL_CONFIG['password'], host=MAIL_CONFIG['host'])

    # 发送纯文本
    def send_text(self, receiver, title, text):
        self.mail_sender.send(receiver, title, text)


if __name__ == '__main__':
    mail = MailManager()
    mail.send_text(receiver='11@qq.com', title='消息通知', text='这个是正文内容啦')
