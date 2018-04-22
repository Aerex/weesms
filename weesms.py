# -*- coding: utf-8 -*-
try:
    import weechat as w
except:
    pass

SCRIPT_NAME = "weesms"
SCRIPT_VERSION = "1.0.0"
SCRIPT_DESC = "weechat plugin to send sms using pushbullet"

class Contact(object):
    def __init__(self, name='', phone=''):
        self.name = name
        self.phone = phone
    
