import unittest
import main


class TestNewIndexMethod(unittest.TestCase):

    def test_arrows(self):
        previous_index = 10
        strings, expected_results = ('<<', '>>>', '><>'), (8, 13, 10)

        for i in range(3):
            self.assertEqual(
                main.new_index(strings[i], previous_index),
                expected_results[i]
            )

    def test_at(self):
        previous_index = 10
        strings, expected_results = ('@14', '@', '@abc'), (14, 10, 10)

        for i in range(3):
            self.assertEqual(
                main.new_index(strings[i], previous_index),
                expected_results[i]
            )

class TestIsCommandMethod(unittest.TestCase):

    def test_smoke(self):
        strings, expected_results = ('123', '>>', '@7'), (False, True, True)

        for i in range(3):
            self.assertEqual(
                main.is_command(strings[i]),
                expected_results[i]
            )
