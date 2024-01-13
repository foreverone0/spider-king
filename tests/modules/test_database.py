import unittest

from spider_king.modules import SpiderDatabase, PostEntity


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db = SpiderDatabase('sqlite:///:memory:', echo=True)

    def tearDown(self):
        self.db.close()

    def test_insert_post(self):
        post_id = self.db.insert_post(PostEntity(
            id=1,
            title='test',
            src_fid='1',
            src_url='http://test.com',
            dst_fid='2',
            dst_url='http://test.com'
        ))

        self.assertEqual(post_id, 1)

    def test_exist_post(self):
        self.db.insert_post(PostEntity(
            id=1,
            title='test',
            src_fid='1',
            src_url='http://test.com',
            dst_fid='2',
            dst_url='http://test.com'
        ))

        self.assertTrue(self.db.exist_post(1))
        self.assertFalse(self.db.exist_post(2))


if __name__ == '__main__':
    unittest.main()
