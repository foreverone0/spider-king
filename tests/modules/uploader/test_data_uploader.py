import unittest

from modules.uploader.data_uploader import DataUploader


class MyTestCase(unittest.TestCase):
    def test_upload(self):
        with open('a.gif', 'rb') as f:
            url = DataUploader.upload(f.read(), 'a.gif')
            self.assertTrue(url.startswith('http://get.datapps.org/'))

        with open('a.jpeg', 'rb') as f:
            url = DataUploader.upload(f.read(), 'a.jpeg')
            self.assertTrue(url.startswith('http://get.datapps.org/'))

        with open('a.webp', 'rb') as f:
            url = DataUploader.upload(f.read(), 'a.webp')
            self.assertTrue(url.startswith('http://get.datapps.org/'))


if __name__ == '__main__':
    unittest.main()
