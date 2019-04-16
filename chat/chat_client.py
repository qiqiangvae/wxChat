import re
from datetime import datetime

import itchat
import xpinyin

from chat import reply_group_list, reply_friend_list
from chat.tuling import Tuling
from rule.rule_data.rule_client import RuleClient


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
    groups = list(
        filter(lambda group: group['NickName'] in reply_group_list and group['UserName'] == msg['FromUserName'],
               itchat.get_chatrooms()))
    if not groups:
        return
    group_ = groups[0]
    text_ = msg['Text']
    nick_name_ = pinyin.get_pinyin(group_['NickName']).replace("-", '')
    reply = '【七七回复】' + Tuling.get_response(text_, user=nick_name_)
    print('收到群%s消息：%s,回复消息： %s' % (nick_name_, text_, reply))
    return reply


@itchat.msg_register([itchat.content.TEXT], isFriendChat=True)
def text_listener(msg):
    friends = list(
        filter(lambda friend: friend['NickName'] in reply_friend_list and friend['UserName'] == msg['FromUserName'],
               itchat.get_friends()))
    if not friends:
        return
    friends_ = friends[0]
    text_ = msg['Text']
    nick_name_ = pinyin.get_pinyin(friends_['NickName']).replace("-", '')
    reply = '【七七回复】' + Tuling.get_response(text_, user=nick_name_)
    print('收到朋友%s消息：%s,回复消息 %s' % (nick_name_, text_, reply))
    return reply


# @itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
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
    pinyin = xpinyin.Pinyin()
    RuleClient.config()
    WxChat()
