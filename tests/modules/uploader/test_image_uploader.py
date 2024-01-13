import unittest

from king.modules.uploader import ImageUploader


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.uploader = ImageUploader()

    def test_get_auth_token(self):
        auth_token = self.uploader.get_auth_token()
        self.assertIsNotNone(auth_token)

        # 测试缓存
        auth_token1 = self.uploader.get_auth_token()
        self.assertEqual(auth_token, auth_token1)

        # 测试缓存过期
        self.uploader.get_auth_token.cache_clear()
        auth_token2 = self.uploader.get_auth_token()
        self.assertNotEqual(auth_token, auth_token2)

    def test_upload(self):
        url = self.uploader.upload('url', 'https://post.imgso.net/images/2024/01/10/filed4ab2.jpg')
        self.assertIsNotNone(url)
        print(url)

        with open('a.jpeg', 'rb') as f:
            url = self.uploader.upload('file', f.read())
            self.assertIsNotNone(url)
            print(url)

        with open('a.gif', 'rb') as f:
            url = self.uploader.upload('file', f.read())
            self.assertIsNotNone(url)
            print(url)

        with open('a.webp', 'rb') as f:
            url = self.uploader.upload('file', f.read())
            self.assertIsNotNone(url)
            print(url)


if __name__ == '__main__':
    unittest.main()
