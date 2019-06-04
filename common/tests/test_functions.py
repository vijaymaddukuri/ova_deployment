import os
import unittest

from os.path import dirname, abspath, join
from common import functions

current_dir = dirname(dirname(abspath(__file__)))

COMMON_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestYaml(unittest.TestCase):
    def setUp(self):
        self.configPath_postive = join(current_dir, "tests", "test_resources", "text.yaml")
        self.configPath_negative = "tests/test_resourcess/text.yaml"
        self.data = {'a list': [1, 42, 3.141, 1337, 'help'],
                     'another_dict': {'foo': 'bar',
                                      'key': 'value',
                                      'the answer': 42}}

    def test_utils_yaml_positive(self):
        # Write YAML file
        functions.dict_to_yaml(self.data, self.configPath_postive)
        self.assertEqual(functions.get_config('another_dict', 'foo', self.configPath_postive), 'bar')

    def test_utils_yaml_negative(self):
        # # Write YAML file
        with self.assertRaises(Exception) as context:
            functions.dict_to_yaml(self.data, self.configPath_negative)
            self.assertTrue('No such file' in str(context.exception))



if __name__ == '__main__':
    unittest.main()
