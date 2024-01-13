import unittest
from io import BytesIO

from modules.publish.api import PublishPostAttachment
from modules.publish.repository import PublishRepository


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.repository = PublishRepository('我为人人', 'dio0924', "8", '2048')

    def test_login(self):
        self.repository.login()

    def test_get_post_info_not_login(self):
        with self.assertRaises(Exception):
            self.repository.get_post_info(3)

    def test_get_post_info(self):
        self.repository.login()
        verify, hexie = self.repository.get_post_info(3)
        self.assertEqual(len(verify), 8)
        self.assertEqual(len(hexie), 8)

    def test_post_not_login(self):
        with self.assertRaises(Exception):
            self.repository.post(3, 'test', 'test', 'test', 'test')

    def test_post(self):
        self.repository.login()
        verify, hexie = self.repository.get_post_info(3)

        fid = 18
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

        self.repository.post(fid, title, content, verify, hexie)
        self.repository.post(fid, title, content, verify, hexie, attachments=attachments)

        with self.assertRaises(Exception):
            self.repository.post(fid, title, content, verify, hexie, attachments=[
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


if __name__ == '__main__':
    unittest.main()
