# -*- coding: utf-8 -*-

class TestExplainer():

	"""
		断言食用说明::
		
		assertEqual(a, b)			a == b	 
		assertNotEqual(a, b)		a != b	 
		assertTrue(x)				bool(x) is True	 
		assertFalse(x)				bool(x) is False	 
		assertIs(a, b)				a is b	
		assertIsNot(a, b)			a is not b	
		assertIsNone(x)				x is None	
		assertIsNotNone(x)			x is not None	
		assertIn(a, b)				a in b	
		assertNotIn(a, b)			a not in b	
		assertIsInstance(a, b)		isinstance(a, b)	
		assertNotIsInstance(a, b)	not isinstance(a, b)	
		文档参考地址: https://docs.python.org/2/library/unittest.html
	"""

	def _get_test_api1(self, body, invoker):
		invoker.assertEqual("xxxx", body)
	def _post_test_api2(self, body, invoker):
		pass