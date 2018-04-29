import uuid
import pytest
import sys
import json
import mock
import os
from pytest_mock import mocker

sys.path.append(".")

from weesms import Contact

CONTACT_DIR = '~/.weechat/weesms.json'


def test_contact():
    expectedNick = 'raikage'
    expectedId = uuid.uuid4()
    contact = Contact(nick=expectedNick, id=expectedId)
    expectedRep = "Nick:{} Identifier:{}".format(expectedNick, expectedId) 
    actualRep = repr(contact)

    assert actualRep == expectedRep


def test_info():
    expectedNick = 'raikage'
    expectedFirstName = 'Shin'
    expectedLastName = 'Hayata'
   
    contact = Contact(nick=expectedNick)
    contact.setInfo(first_name=expectedFirstName, last_name=expectedLastName)
   
    assert contact.last_name == expectedLastName
    assert contact.first_name == expectedFirstName
    assert contact.nick == expectedNick

def test_save_with_empty_contact_list(mocker, fake_weechat_instance):
    expected_nick = 'mizukage'
    expected_phone = '+11234567890'
    expected_id = str(uuid.uuid4())
    expected_list_of_contacts = [{"nick": expected_nick, "id": expected_id, "phone": expected_phone}]

    contact = Contact(nick=expected_nick, phone=expected_phone, id=expected_id)
    
    mocker.patch('os.path.exists')
    os.path.exists.return_value = False
    fd = mocker.mock_open()
    with mocker.patch('__builtin__.open', new_callable=fd) as contact_list:
        with mocker.patch('json.dump') as mock_json:
            contact.save()
            print 'hello  ' 
            mock_json.assert_called_with(expected_list_of_contacts)



    os.path.exists.assert_called_with(CONTACT_DIR)

