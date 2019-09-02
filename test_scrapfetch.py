import unittest
from unittest.mock import patch
import scrapfetch
import validators


class TestScrapFetch(unittest.TestCase):
    def setUp(self):
        self.url1 = 'google.com'
        self.url2 = 'www.google.com'
        self.url3 = 'https://google.com'
        self.url4 = 'https://www.google.com'

    def tearDown(self):
        self.url1 = None
        self.url2 = None
        self.url3 = None
        self.url4 = None

    def test_validate(self):
        self.assertIsInstance(scrapfetch.validate(self.url1), validators.utils.ValidationFailure)
        self.assertIsInstance(scrapfetch.validate(self.url2),
                              validators.utils.ValidationFailure)
        self.assertTrue(scrapfetch.validate(self.url3))
        self.assertTrue(scrapfetch.validate(self.url4))

    def test_content_fetch(self):
        with patch('scrapfetch.requests.get') as mocked_get:
            test = scrapfetch.content_fetch(self.url1)
            mocked_get.assert_called_with(self.url1)
            self.assertIsInstance(test, unittest.mock.MagicMock)

            test = scrapfetch.content_fetch(self.url2)
            mocked_get.assert_called_with(self.url2)
            self.assertIsInstance(test, unittest.mock.MagicMock)

            test = scrapfetch.content_fetch(self.url3)
            mocked_get.assert_called_with(self.url3)
            self.assertIsInstance(test, unittest.mock.MagicMock)

            test = scrapfetch.content_fetch(self.url4)
            mocked_get.assert_called_with(self.url4)
            self.assertIsInstance(test, unittest.mock.MagicMock)

    def test_request_successful(self):
        with patch('scrapfetch.requests.get') as mocked_get:
            mocked_get.return_value.status_code = False
            test = scrapfetch.content_fetch(self.url1)
            mocked_get.assert_called_with(self.url1)
            test2 = scrapfetch.request_successful(test)
            self.assertFalse(test2)

            mocked_get.return_value.status_code = False
            test = scrapfetch.content_fetch(self.url2)
            mocked_get.assert_called_with(self.url2)
            test2 = scrapfetch.request_successful(test)
            self.assertFalse(test2)

            mocked_get.return_value.status_code = scrapfetch.requests.codes.ok
            test = scrapfetch.content_fetch(self.url3)
            mocked_get.assert_called_with(self.url3)
            test2 = scrapfetch.request_successful(test)
            self.assertTrue(test2)

            mocked_get.return_value.status_code = scrapfetch.requests.codes.ok
            test = scrapfetch.content_fetch(self.url3)
            mocked_get.assert_called_with(self.url3)
            test2 = scrapfetch.request_successful(test)
            self.assertTrue(test2)

    def test_fetch_links(self):
        pass

    def test_give_choices(self):
        pass

    def test_choose_from(self):
        with patch('scrapfetch.input') as mocked_input:
            choices = ('as', 'asf', 'wfew', 'end')
            mocked_input.return_value = 'end'
            test = scrapfetch.choose_from('Please choose from: ', *choices)
            mocked_input.assert_called_with('Please choose from: ')
            self.assertNotEqual(test, 'afs')

            mocked_input.return_value = 'end'
            test = scrapfetch.choose_from('Please choose from: ', *choices)
            mocked_input.assert_called_with('Please choose from: ')
            self.assertEqual(test, 'end')

            mocked_input.return_value = 'ASF'
            test = scrapfetch.choose_from('Please choose from: ', *choices)
            mocked_input.assert_called_with('Please choose from: ')
            self.assertEqual(test, 'asf')

    def test_fetch_file_name(self):
        self.assertEqual(scrapfetch.fetch_file_name('www.google.com/test.html'),
                         'test.html')
        self.assertEqual(scrapfetch.fetch_file_name('www.google.com/index/newFile.html'),
                         'newFile.html')
        self.assertEqual(scrapfetch.fetch_file_name(self.url1),
                         self.url1)
        self.assertEqual(scrapfetch.fetch_file_name(self.url2),
                         self.url2)
        self.assertEqual(scrapfetch.fetch_file_name(self.url3),
                         'google.com')
        self.assertEqual(scrapfetch.fetch_file_name(self.url4),
                         'www.google.com')

    def test_verify_file_exist(self):
        pass

    def test_write_to_file(self):
        pass

    def test_remove_from_file(self):
        pass


if __name__ == '__main__':
    unittest.main()
