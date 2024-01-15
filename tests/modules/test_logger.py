import unittest

from spider_king.modules.logger import get_logger


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = get_logger(__name__)

    def test_logger(self):
        self.logger.info("[green]test logger[/green], info", extra={"markup": True})
        self.logger.debug("[green]test logger[/green], debug", extra={"markup": True})

if __name__ == '__main__':
    unittest.main()
