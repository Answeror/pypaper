#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
from nose.tools import assert_false, assert_equal
from .. import tor


def test_single():
    root = tempfile.mkdtemp()
    try:
        t = tor.Tor(root=root)
        t.run()
        import time
        time.sleep(10)
        t.stop()
        #assert_false(pid_exists(read_pid(root)))
        assert_equal(
            read_output(root)[-2:],
            [
                'Opening Socks listener on 127.0.0.1:9050',
                'Opening Control listener on 127.0.0.1:8118'
            ]
        )
    finally:
        try:
            shutil.rmtree(root)
        except:
            pass


def pid_exists(pid):
    """Check whether pid exists in the current process table."""
    import errno
    if pid < 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError, e:
        return e.errno == errno.EPERM
    else:
        return True


def read_pid(root):
    with open(os.path.join(root, 'tor.pid'), 'r') as f:
        return int(f.read())


def read_output(root):
    with open(os.path.join(root, 'out'), 'r') as f:
        return [trim(line.decode('utf-8')) for line in f]


def trim(s):
    import re
    ret = re.search(r'.*\[\w+\] (.*)', s)
    assert ret
    return ret.group(1).strip()
