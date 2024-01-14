import unittest

from spider_king.modules.uploader.image_uploader import ImageUploader


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.uploader = ImageUploader()

    async def test_get_auth_token(self):
        auth_token = await self.uploader.get_auth_token()
        self.assertIsNotNone(auth_token)

        # 测试缓存
        auth_token1 = await self.uploader.get_auth_token()
        self.assertEqual(auth_token, auth_token1)

        # 测试缓存过期
        # self.uploader.get_auth_token.cache_clear()
        # auth_token2 = await self.uploader.get_auth_token()
        # self.assertNotEqual(auth_token, auth_token2)

    async def test_upload(self):
        with open('a.jpeg', 'rb') as f:
            url = await self.uploader.upload(f.read())
            self.assertIsNotNone(url)
            print(url)

        with open('a.gif', 'rb') as f:
            url = await self.uploader.upload(f.read())
            self.assertIsNotNone(url)
            print(url)

        with open('a.webp', 'rb') as f:
            url = await self.uploader.upload(f.read())
            self.assertIsNotNone(url)
            print(url)


if __name__ == '__main__':
    unittest.main()
