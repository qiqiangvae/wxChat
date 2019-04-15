import itchat

from rule.rule_data.rule_client import RuleClient
from datetime import datetime
from chat.tuling import Tuling
from chat import reply_group_list, reply_friend_list
import re


class WxChat(object):
    def __init__(self):
        itchat.auto_login(loginCallback=WxChat.login_callback, exitCallback=WxChat.exit_callback)
        itchat.run()

    @staticmethod
    def login_callback():
        print('login success')

    @staticmethod
    def exit_callback():
        print('login success')


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def text_listener(msg):
    # 获取所有群组
    chatrooms = itchat.get_chatrooms()
    # 获取授权群组
    can_next = False
    for group in chatrooms:
        if not can_next:
            if group['NickName'] in reply_group_list and group['UserName'] == msg['FromUserName']:
                can_next = True
                break
    if not can_next:
        return
    text_ = msg['Text']
    reply = Tuling.get_response(text_)
    print('收到消息：%s,回复消息：%s' % (text_, reply))
    return reply


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def text_listener(msg):
    msg_text_ = msg['Text']
    print('收到消息%s' % msg_text_)
    can_next = False
    rule_list = RuleClient.query(order='sort')
    for rule in rule_list:
        if rule['startTime'] and rule['endTime']:
            if rule['startTime'] < datetime.now() < rule['endTime']:
                break
            else:
                continue
        elif rule['startTime'] is None and rule['endTime'] is None:
            if re.match(rule['rule'], msg_text_):
                itchat.send_msg(rule['reply'])
                break


if __name__ == '__main__':
    RuleClient.config()
    WxChat()
