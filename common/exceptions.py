#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Shen Bin
@contact: shenbin@maimiaotech.com
@date: 2013-09-10 10:20
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""

class JsonDecodeException(Exception):
	"""
	raise this exception when api output is not json schema
	"""
	def __init__(self, msg=None):
	    self.msg = msg

	def __str__(self):
	    return "JsonDecodeException:%s "%(self.msg)


class InvalidInputException(Exception):
	"""
	raise this exception when the request data of ajax is not as expected
	"""
	def __init__(self, msg=None):
	    self.msg = msg

	def __str__(self):
	    return "InvalidInputException:%s"%(self.msg)


class MongodbException(Exception):
	"""
	raise this exception when meet a mongodb exception, such as  pymongo.errors.OperationFailure
	"""
	def __init__(self, msg=None):
	    self.msg = msg

	def __str__(self):
	    return "MongodbException:%s"%(self.msg)