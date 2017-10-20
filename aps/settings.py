#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:29:51 2017

@author: ishxiao
~Email~: me@ishxiao.com

"""

from __future__ import absolute_import

try:
    import logging
    _logger = logging.getLogger(__name__)
    _logger.addHandler(logging.NullHandler())
    del logging  # Don't leak names!
except:
    _logger = None