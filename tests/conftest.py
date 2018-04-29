import sys
import pytest
sys.path.append(".")

import weesms

class fake_weechat():
    WEECHAT_RC_OK = 0
    def __init__(self):
        self.WEECHAT_RC_OK = 0
        self.WEECHAT_RC_ERROR = -1
    def prnt(message):
        print message


@pytest.fixture
def fake_weechat_instance():
    weesms.w = fake_weechat()
    weesms.w.WEECHAT_RC_OK = 0
    pass
