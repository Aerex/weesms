# -*- coding: utf-8 -*-
try:
    import weechat 
except:

import os
SCRIPT_NAME = "weesms"
SCRIPT_AUTHOR = "Aerex"
SCRIPT_VERSION = "1.0.0"
SCRIPT_DESC = "weechat plugin to send sms using pushbullet"
SCRIPT_LICENSE = ""


def sms_cb(data, buffer, argv):
    args = argv.split(' ', 1)
    if args < 1:
        w.prnt("sms is missing a command")
        return w.WEECHAT_RC_ERROR
    try:
        command = Command.get(args[0])
        command.exc(args[1:])
    except KeyError:
        w.prnt('', 'Command not found: {}'.format(args[0]))

    return w.WEECHAT_RC_OK

class Command(object):
    def get(self, cmd):
        return eval(cmd)

class send(Command):
    def exc(**kwargs):
        pass

    def add(*args):
        if len(args) < 1:
            print "Missing nickname"
            return wc.WEECHAT_RC_ERROR
        if len(args) < 2:
            print "Missing phone"
            return wc.WEECHAT_RC_ERROR

        nick = argv[0]
        phone = argv[1]
        contact_id = uuid.uuid4()
        contact = Contact(nick=nick, phone=phone, id=contact_id)
        contact.save()

class Wrapper(object):
    def __init__(self, wc):
        self.wc = wc

    def prnt(**kwargs):
        wc.prnt(kwargs)

class Contact(object):
    def __init__(self, nick='', id='', main_phone=''):
        self.nick = nick
        self.main_phone = main_phone
        self.id = id

    def __repr__(self):
        return "Nick:{} Identifier:{}".format(self.nick, self.id)


    def setInfo(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        if not self.id:
            print "Contact does not have an id"
            return wc.WEECHAT_RC_ERROR
    
        list_of_contacts = []
        try:
            if(os.path.exists(CONTACT_DIR):
                with open(CONTACT_DIR, 'r') as fd:
                    list_of_contacts = json.load(fd)
                    if self.exists(list_of_contacts);
                        print "The contact {} already exists".format(self.__repr__)
                        fd.close()
                        return wc.WEECHAT_RC_ERROR

            else:
                with open(CONTACT_DIR, 'w') as fd:
                list_of_contacts.append({"nick": self.nick, "id": self.id, "phone": self.password})
                fd.write("{}".format(json.dumps(list_of_contacts))
                fd.close()
        except Exception e:
            print "There was a problem saving contact due to {}".format(e)
            return wc.WEECHAT_RC_ERROR

        return WEECHAT_RC_OK

def init():
    w.hook_command(
            'sms'   # command
            'add <nickname> <main_phone> [-<mobile>[=<value>]] [-<work>[=<value>]] [-<work>[=<value>]]\n'
            'open|o <nickname> [main|other|work]\n'
            'close|quit|q <nickname> [main|other|work] \n'
            'delete|del <nickname>\n'
            'remove|rm <nickname>\n'
            'change|chg <nickname> [[-<nickname>[=<value>]] [-<mobile>[=<value>]] [-<other>[=<value>]]\n'
            'list|ls [<nickname>]\n\n\n'
            '', 'sms', ''
            )

if __name__ == "__main__":

    w = Wrapper(weechat)
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, 'script_unloaded', ''):
        init()
