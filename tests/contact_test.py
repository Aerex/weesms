from weesms import Contact
import pytest

def test_contact():
    expectedName = 'HayataShin'
    expectedPhone = '123-456-7890'
    contact = Contact(name=expectedName, phone=expectedPhone)
    assert contact.name == expectedName
    assert contact.phone == expectedPhone



