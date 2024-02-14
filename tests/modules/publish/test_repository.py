import unittest
from datetime import datetime
from io import BytesIO

from spider_king.modules.publish import PublishRepository, PublishPostAttachment


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repository = PublishRepository('摸逼校尉', 'dio0924', "8", '2048')

    def test_login(self):
        self.repository.login()

    def test_get_post_info_not_login(self):
        with self.assertRaises(Exception):
            self.repository.get_post_info(3)

    def test_get_post_info(self):
        self.repository.login()
        verify, hexie = self.repository.get_post_info(3)
        verify, hexie = self.repository.get_post_info(3)
        verify, hexie = self.repository.get_post_info(3)
        self.assertEqual(len(verify), 8)
        self.assertEqual(len(hexie), 8)

    def test_post_not_login(self):
        with self.assertRaises(Exception):
            self.repository.post(3, 'test', 'test', 'test', 'test')

    def test_post(self):
        self.repository.login()
        fid = 283

        title = '测试标题'
        content = '测试内容'
        with open('test.png', 'rb') as f:
            png_attach = PublishPostAttachment(
                name='测试图片1.jpg',
                content=f.read(),
            )
        with open('test.torrent', 'rb') as f:
            torrent_attach = PublishPostAttachment(
                name='测试种子1.torrent',
                content=f.read(),

            )

        with open('test.rar', 'rb') as f:
            rar_attach = PublishPostAttachment(
                name='测试压缩包1.rar',
                content=f.read(),
            )

        attachments = [
            png_attach,
            torrent_attach,
            rar_attach,
        ]

        self.repository.post(fid, title, content, )
        self.repository.post(fid, title, content, attachments=attachments)
        self.repository.post(fid, title, content, category_id=592, attachments=attachments)

        with self.assertRaises(Exception):
            self.repository.post(fid, title, content, attachments=[
                PublishPostAttachment(
                    name='测试压缩包1.rar',
                    content=BytesIO(b'1234567890'),
                ),
                PublishPostAttachment(
                    name='测试压缩包2.png',
                    content=BytesIO(b'1234567890'),
                ),
                PublishPostAttachment(
                    name='测试种子.torrent',
                    content=BytesIO(b'1234567890'),
                ),

            ])

    def test_sell(self):
        self.repository.login()
        fid = 283

        title = '测试标题'
        content = '测试内容'

        with open('test.torrent', 'rb') as f:
            torrent_attach = PublishPostAttachment(
                name='测试种子1.torrent',
                content=f.read(),
                ctype="3",
                special="2",
                needrvrc="10"
            )


        attachments = [

            torrent_attach,

        ]

        self.repository.post(fid, title, content, )
        self.repository.post(fid, title, content, attachments=attachments)


if __name__ == '__main__':
    unittest.main()
