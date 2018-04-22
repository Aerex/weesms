import uuid
import pytest
import sys

sys.path.append(".")

from weesms import Contact

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

