# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-07-25 16:54:16
# @Last Modified by:   anchen
# @Last Modified time: 2017-07-25 18:53:15
import gc
import sys

class CGcLeak(object):
    def __init__(self):
        self._text = '#' * 10

    def __def__(self):
        pass

def make_circle_ref():
    _gcleak = CGcLeak()
    #  _gcleak._self = _gcleak # test_code_1
    print '_gcleak ref count0:%d' % sys.getrefcount(_gcleak)
    del _gcleak
    try:
        print '_gcleak ref count1:%d' % sys.getrefcount(_gcleak)
    except UnboundLocalError:
        print '_gcleak is invalid!'
def test_gcleak():
    # Enable automatic garbage collection.
    gc.enable()
    # Set the garbage collection debugging flags.
    gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | /
    gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)

    print 'begin leak test...'
    make_circle_ref()

    print 'begin collect...'
    _unreachable = gc.collect()
    print 'unreachable object num:%d' % _unreachable
    print 'garbage object num:%d' % len(gc.garbage)

if __name__ == '__main__':
    test_gcleak()