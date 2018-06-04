import sys
import pytest
sys.path.append(".")

import weesms

class fake_weechat():
    WEECHAT_RC_ERROR = 0
    WEECHAT_RC_OK = 1
    WEECHAT_RC_OK_EAT = 2
    def __init__(self):
        pass
    def prnt(message):
        print message


@pytest.fixture
def fake_weechat_instance():
    weesms.w = fake_weechat()
    weesms.w.WEECHAT_RC_OK = 0
    pass
