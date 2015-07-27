# -*- coding: utf-8 -*-
from explainers.explainer_test import TestExplainer

class Request():
	__requests = []
	__instances = []
	__port = -1
	def __init__(self):
		self.__port = 8704
		self.__requests = [
			#url接口地址 、method请求方式：get, post一律小写、is_test是否需要测、args请求参数 iscypt是否需要加密
			{"url":"http://此处填写域名或ip:%s/api/test/test_api1"%self.__port, "method": "get", "is_test": True, "args":{"exp":"哈哈", "exp2": "mm"}, "iscypt": False},
			{"url":"http://此处填写域名或ip:%s/api/test/test_api2"%self.__port, "method": "post", "is_test": True, "args":{"car1":"i'm car one", "car2":"i'm car tow"}, "iscypt": False},
		]
		self.__instances = {
			"test": TestExplainer(),
		}

	def get_requests(self):
		return self.__requests

	def get_explainer(self, cinstance, method):
		if cinstance and method:
			if self.__instances.has_key(cinstance):
				func = getattr(self.__instances[cinstance], method, None)
				if not func:
					return -1
				else:
					return func
			else:
				return -2
		else:
			return -3
