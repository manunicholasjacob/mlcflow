"""
Unit tests for mlc.utils.convert_args_to_dictionary.

automation/script/module.py reads MLC_SCRIPT_EXTRA_CMD from the environment
and passes it here as a single string. The function used to iterate that
string one character at a time, so "--adr.python.name=mlperf" came back as
{"": ""} and every option in the variable was dropped. A string is now split
like a shell command line; an argv list behaves as before.
"""

import unittest

from mlc.utils import convert_args_to_dictionary


class ConvertArgsToDictionaryTests(unittest.TestCase):

    def test_list_input_unchanged(self):
        r = convert_args_to_dictionary(
            ["--quiet", "--env.FOO=bar", "--adr.python.name=mlperf"])
        self.assertEqual(r["return"], 0)
        self.assertEqual(r["args_dict"], {
            "quiet": True,
            "env": {"FOO": "bar"},
            "adr": {"python": {"name": "mlperf"}},
        })

    def test_string_input_is_split_like_argv(self):
        r = convert_args_to_dictionary(
            "--quiet --env.FOO=bar --adr.python.name=mlperf")
        self.assertEqual(r["return"], 0)
        self.assertEqual(r["args_dict"], {
            "quiet": True,
            "env": {"FOO": "bar"},
            "adr": {"python": {"name": "mlperf"}},
        })

    def test_single_option_string(self):
        # The form documented for MLC_SCRIPT_EXTRA_CMD in user reports.
        r = convert_args_to_dictionary("--adr.python.name=mlperf")
        self.assertEqual(
            r["args_dict"], {
                "adr": {
                    "python": {
                        "name": "mlperf"}}})

    def test_string_with_quoted_value(self):
        r = convert_args_to_dictionary("--env.MSG=\"hello world\" -j")
        self.assertEqual(r["args_dict"],
                         {"env": {"MSG": "hello world"}, "j": True})

    def test_string_list_value(self):
        r = convert_args_to_dictionary("--tags,=a,b,c")
        self.assertEqual(r["args_dict"], {"tags": ["a", "b", "c"]})

    def test_empty_string(self):
        r = convert_args_to_dictionary("")
        self.assertEqual(r, {"return": 0, "args_dict": {}})


if __name__ == "__main__":
    unittest.main()
