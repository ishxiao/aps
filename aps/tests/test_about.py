#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 19:52:50 2017

@author: ishxiao
~Email~: me@ishxiao.com

"""

from aps import about

def test_about():
    try:
        about()
    except:
        assert False
    assert True