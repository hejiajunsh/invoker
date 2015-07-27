# -*- coding: utf-8 -*-
import tornado
import tornado.httpserver
import os
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.testing import AsyncHTTPTestCase, gen_test, bind_unused_port
import tornado.ioloop
import threading
import json
import urllib
from tornado.test.util import unittest
from tornado.httputil import url_concat

from config.settings import settings
from config.routes import url_patterns    
from libs.app import Application
from unit_test.request_configs import Request

class Unit_Test(AsyncHTTPTestCase):

	requests = []
	io_loop = None
	"""
		为测试环境进行一些初始化操作 重写父类的setUP
	"""
	def setUp(self):
		super(Unit_Test, self).setUp()
		self.requests = Request().get_requests()
		if not self.requests:
			print "nothing to be tested"
			exit()

		self.io_loop = self.get_new_ioloop()
		self.io_loop.make_current()

	"""
		get_app 这个方法必须重写
	"""
	def get_app(self):    
		return Application(url_patterns, **settings)

	"""
		每个测试用列需要以test_开头 
		不过这里相当于一个控制器异步循环调用要测试的每个接口
		在这个类里出现这一个就够用了
	"""
	def test_Test(self):
		self.http_fetch()
	@tornado.testing.gen_test
	def http_fetch(self):
		client = AsyncHTTPClient(self.io_loop)
		for req in self.requests:
			if not req["is_test"]:
				continue
			ctls = req["url"].split("/")
			cinstance = ctls[4]
			method = "_%s_%s"%(req["method"], ctls[5])
			
			if req["method"]=="get" and req["args"]:
				#此处有坑啊{"p":json.dumps(req["args"])}这种格式传p值而不可以直接在第二个参数传{p:{"arg1":..,...}}否则会报Expecting property name enclosed in double quotes: line 1 column 2 (char 1)这个参数服务端获取后看似json格式T__T
				req["url"] = url_concat(req["url"], {"p":json.dumps(req["args"])})
			request = HTTPRequest(
						url = req["url"],
						method = str(req["method"]).upper(),
						body = self.get_body(req["method"], req["args"]),
						connect_timeout = 20,
						request_timeout = 20,
					)
			response = yield client.fetch(request)
			proc = Proc()
			proc.explain(self, response, cinstance, method)

	"""
		请求为POST时构造参数
	"""

	def get_body(self, method, args):
		if method=="post":
			return "p="+json.dumps(args)
		else:
			return None

class Proc():
	"""
		一个解释控制调度器 使用对应请求的解释器解析返回值
	"""
	def explain(self, invoker, resp, cinstance, method):
		func = Request().get_explainer(cinstance, method)
		if func<0 or not func:
			if func<0:
				print "The Request has no explainer" + str(func) + ":" + resp.effective_url
			else:
				print cinstance + "The Request has no explainer" + method + ":" + resp.effective_url
		else:
			func(resp.body, invoker)

if __name__=="__main__":
	unittest.main()