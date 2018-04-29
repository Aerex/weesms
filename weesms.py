# -*- coding: utf-8 -*-
try:
    import weechat 
except:
    pass
import os
import json


SCRIPT_NAME = "weesms"
SCRIPT_AUTHOR = "Aerex"
SCRIPT_VERSION = "1.0.0"
SCRIPT_DESC = "weechat plugin to send sms using pushbullet"
SCRIPT_LICENSE = ""

CONTACT_DIR = "~/.weechat/weesms.json"

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
            return w.WEECHAT_RC_ERROR
        if len(args) < 2:
            print "Missing phone"
            return w.WEECHAT_RC_ERROR

        nick = argv[0]
        phone = argv[1]
        contact_id = uuid.uuid4()
        contact = Contact(nick=nick, phone=phone, id=str(contact_id))
        contact.save()

class Wrapper(object):
    def __init__(self, w):
        self.w = w

    def prnt(**kwargs):
        self.w.prnt(kwargs)

class Contact(object):
    def __init__(self, nick='', id='', phone=''):
        self.nick = nick
        self.phone = phone
        self.id = id

    def __repr__(self):
        return "Nick:{} Identifier:{}".format(self.nick, self.id)


    def setInfo(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        print 'sdfsd'
        if not self.id:
            print "Contact does not have an id"
            return w.WEECHAT_RC_ERROR
        list_of_contacts = []
        try:
            if os.path.exists(CONTACT_DIR):
                with open(CONTACT_DIR, 'r') as fd:
                    list_of_contacts = json.load(fd)
                    if self.exists(list_of_contacts):
                        print "The contact {} already exists".format(self.__repr__)
                        fd.close()
                        return w.WEECHAT_RC_ERROR

            else:
                print 'hdsfad'
                with open(CONTACT_DIR, 'w') as fd:
                    print 'hello worl'
                    list_of_contacts.append({"nick": self.nick, "id": self.id, "phone": self.phone})
                    fd.write("{}".format(json.dump(list_of_contacts)))
                    fd.close()
        except Exception as e:
            print "There was a problem saving the contact due to {}".format(e)
            return w.WEECHAT_RC_ERROR

        return w.WEECHAT_RC_OK

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
