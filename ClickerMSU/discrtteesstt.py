"""Tester."""

import unittest
# try:
from .insertion_deleting_sqlite import register, sighin, update_data, update_signed, get_data
# except Exception:
#    from insertion_deleting_sqlite import register, sighin, update_data, update_signed, get_data


class TestAdder(unittest.TestCase):
    """This is tester."""

    argss = {}
    print__ = None

    def test1(self):
        """Try test1."""
        self.assertEqual(tuple(register(None, "", "123", 0)), (1, None))

    def test2(self):
        """Try test2."""
        self.assertEqual(tuple(register(None, "A" * 300, "", 0)), (2, None))

    def test3(self):
        """Try test3."""
        self.assertEqual(tuple(register(None, "123", "123", 0)), (3, None))

    def test4(self):
        """Try test4."""
        self.assertEqual((list(sighin(None, "", "123", 0))[0:2]), [4, None])

    def test5(self):
        """Try test5."""
        self.assertEqual((list(sighin(None, "123", "", 0))[0:2]), [2, None])

    def test6(self):
        """Try test6."""
        self.assertEqual((list(sighin(None, "123", "124", 0))[0:2]), [3, None])

    def test7(self):
        """Try test7."""
        self.assertEqual(type(get_data()), type([0, 1, 2]))

    def test8(self):
        """Try test8."""
        sighin(None, "123", "123", 0)
        self.assertEqual(update_data(None), True)

    def test9(self):
        """Try test9."""
        self.assertEqual(update_signed(None, "234", 0), True)
