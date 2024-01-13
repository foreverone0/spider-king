import unittest

from spider_king.modules import PublishApi


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = PublishApi(username='test', password='test')

    def test_login(self):
        html = self.api.login()
        self.assertIsNotNone(html)
        self.assertIn('不存在', html)

    def test_get_post_info(self):
        html = self.api.get_post_info(3)
        self.assertIsNotNone(html)

    def test_post(self):
        html = self.api.post(3, 'test', 'test', 'test', 'test')
        self.assertIsNotNone(html)
        self.assertIn('非法请求，请返回重试', html)


if __name__ == '__main__':
    unittest.main()
