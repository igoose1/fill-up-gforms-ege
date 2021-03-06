import unittest
import main


class TestProccesCommandMethod(unittest.TestCase):

    def test_arrows(self):
        previous_index, previous_problem_set = 10, 99
        strings, expected_results = ('<<', '>>>', '><>'), ((8, 99), (13, 99), (10, 99))

        for i in range(3):
            self.assertEqual(
                main.process_command(strings[i], previous_index, previous_problem_set),
                expected_results[i]
            )

    def test_at(self):
        previous_index, previous_problem_set = 10, 99
        strings, expected_results = ('@14', '@', '@abc'), ((14, 99), (10, 99), (10, 99))

        for i in range(3):
            self.assertEqual(
                main.process_command(strings[i], previous_index, previous_problem_set),
                expected_results[i]
            )

    def test_help(self):
        self.assertEqual(
            main.process_command('?', 123, '!@#$'),
            (123, '!@#$')
        )


class TestIsCommandMethod(unittest.TestCase):

    def test_smoke(self):
        strings = ('123', '>>', '@7', '$87', '?')
        expected_results = (False, True, True, True, True)

        for i in range(3):
            self.assertEqual(
                main.is_command(strings[i]),
                expected_results[i]
            )
