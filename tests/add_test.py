import uuid
import pytest
import sys
import mock
from pytest_mock import mocker
import os

sys.path.append(".")

from weesms import send

def test_add():
    expectedNick = 'raikage'
    expectedId = uuid.uuid4()
    contact = Contact(nick=expectedNick, id=expectedId)
    expectedRep = "Nick:{} Identifier:{}".format(expectedNick, expectedId) 
    actualRep = repr(contact)

    assert actualRep == expectedRep

def test_nonick():
    pass

def test_nophone():
    pass
