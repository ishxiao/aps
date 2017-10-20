#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:13:25 2017

@author: ishxiao
~Email~: me@ishxiao.com

"""

from aps.about import about

def run():
    """
    Run the nose test scripts for aps.
    """
    # Call about to get all version info printed with tests
    about()
    import nose
    # runs tests in qutip.tests module only
    nose.run(defaultTest="aps.tests", argv=['nosetests', '-v'])