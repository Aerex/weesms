# -*- coding: utf-8 -*-
try:
    import weechat 
except:
    pass
import os
import io 
try:
    to_unicode = unicode
except NameError:
   to_unicode = str 
import json
import uuid


SCRIPT_NAME = "weesms"
SCRIPT_AUTHOR = "Aerex"
SCRIPT_VERSION = "1.0.0"
SCRIPT_DESC = "weechat plugin to send sms using pushbullet"
SCRIPT_LICENSE = "MIT"

# TODO: have an option for this 
CONTACT_DIR = "{}/.weechat/weesms.json".format(os.path.expanduser('~'))


class Command(object):
    @classmethod
    def isValid(self, cmd):
        list_of_commands = ["add"]
        return cmd in list_of_commands
    @classmethod 
    def get(self, cmd):
        if not self.isValid(cmd):
            raise Exception("Invalid command {}".format(cmd))
        return eval(cmd)

class add(Command):
    def exc(self, *args):
        if not type(args) is tuple and not len(args) == 1:
            w.prnt("", "No valid arguments for {}".format(args))
        argv = args[0]

        if len(argv) < 0:
            w.prnt("", "Missing nickname")
            return w.WEECHAT_RC_ERROR
        if len(argv) < 1:
            w.prnt("", "Missing phone")
            return w.WEECHAT_RC_ERROR

        nick = argv[0]
        phone = argv[1]
        contact_id = uuid.uuid4()
        contact = Contact(nick=nick, phone=phone, id=str(contact_id))
        contact.save()

def sms_cb(data, buffer, argv):
    args = argv.split(' ')
    if len(args) < 0:
        w.prnt("", "sms is missing a command")
        return w.WEECHAT_RC_ERROR
    if len(args) < 1:
        w.prnt("", "{} is missing a command".format(args[1]))
    try:
        instanceClass = Command.get(args[0])
        command = instanceClass()
        command.exc(args[1:])
    except Exception as e:
        w.prnt('', 'There was an issue with {0}: \n{1}'.format(args[1], e))

    return w.WEECHAT_RC_OK

class Wrapper(object):
    def __init__(self, w):
        self.w = w

class Contact(object):
    def __init__(self, nick='', id='', phone=''):
        self.nick = nick
        self.phone = phone
        self.id = id

    def __repr__(self):
        return "Nick:{} Identifier:{}".format(self.nick, self.id)

    def exists(self, list_of_contacts, new_contact, unique="nick"):
        if not type(list_of_contacts) == list:
            raise Exception('list_of_contacts is a {} not a list'.format(str(type(list_of_contacts))))
        for contact in list_of_contacts:
            # TODO: Might want to extract these conditions checks into smaller utility methods
            if new_contact and unique in contact and contact[unique] == new_contact[unique]:
                return True
        return False
        

    def setInfo(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        if not self.id:
            w.prnt("", "Contact does not have an id")
            return w.WEECHAT_RC_ERROR
        list_of_contacts = []
        contact = {"nick": self.nick, "id": self.id, "phone": self.phone}
        try:
            # TODO: If using `CONTACT_DIR` as an option you may need to refactor this to create subdir if it doesn't exist
            if os.path.exists(CONTACT_DIR):
                with io.open(CONTACT_DIR, 'r') as fd:
                    list_of_contacts = json.load(fd)
                    fd.close()
                if self.exists(list_of_contacts, contact):
                    w.prnt("", "The contact {} already exists".format(self.__repr__))
                    return w.WEECHAT_RC_ERROR

            list_of_contacts.append(contact)
            with io.open(CONTACT_DIR, 'w', encoding='utf-8') as fd:
                output = json.dumps(list_of_contacts, indent=4, 
                        sort_keys=True, separators=(',', ': '), ensure_ascii=False)
                fd.write(to_unicode(output))
                fd.close()
        except Exception as e:
            w.prnt("", "There was a problem saving the contact due to {}".format(e))
            return w.WEECHAT_RC_ERROR

        w.prnt("", "Added {} contact".format(self.nick))
        return w.WEECHAT_RC_OK

def init():
    w.hook_command(
            "weesms",   # command
            "Plugin that uses pushbullet to send and receive sms messages",
            "add <nickname> <phone>  || open|o <nickname>"
            "|| close|quit|q <nickname>"
            "|| remove|rm <nickname>"
            "|| change|chg <oldnickname> <newnickname> [[--phone| -p [>=<value>]]"
            "|| list|ls <nickname>\n\n",
            "   add: add contract\n"
            "\n"
            "Examples:\n"
            "   Add a contact: /sms add Buddy 18419745 (include country code)\n",
            "",
            "sms_cb", "")

if __name__ == "__main__":

    w = weechat
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, 'script_unloaded', ''):
        init()
