"""Tester."""

import unittest
from ClickerMSU import Game
from ClickerMSU.insertion_deleting_sqlite import register, sighin, update_data, update_signed, get_data


class TestRegistration(unittest.TestCase):
    """Tester for registration."""

    def test1(self):
        """Try test1."""
        self.assertEqual(tuple(register(None, "", "123", 0)), (1, None))

    def test2(self):
        """Try test2."""
        self.assertEqual(tuple(register(None, "A" * 300, "", 0)), (2, None))

    def test3(self):
        """Try test3."""
        self.assertEqual(tuple(register(None, "123", "123", 0)), (3, None))


class TestSignIn(unittest.TestCase):
    """Tester for sign in procedure."""

    argss = {}
    print__ = None

    def test4(self):
        """Try test4."""
        self.assertEqual((list(sighin(None, "", "123", 0))[0:2]), [4, None])

    def test5(self):
        """Try test5."""
        self.assertEqual((list(sighin(None, "123", "", 0))[0:2]), [2, None])

    def test6(self):
        """Try test6."""
        self.assertEqual((list(sighin(None, "123", "124", 0))[0:2]), [3, None])


class TestDataUpdation(unittest.TestCase):
    """Tester for data updation."""

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


class TestResolutionManipulations(unittest.TestCase):
    """Tester for resolution manipulation."""

    def test10(self):
        """Try test10."""
        self.assertEqual(Game.resolution_to_tuple("1280x720"), (1280, 720))

    def test11(self):
        """Try test11."""
        with self.assertRaises(ValueError):
            Game.resolution_to_tuple("1280:1234")

    def test12(self):
        """Try test12."""
        with self.assertRaises(TypeError):
            Game.resolution_to_tuple(1920)

    def test13(self):
        """Try test13."""
        self.assertEqual(Game.resolution_to_str((1920, 1080)), "1920x1080")

    def test14(self):
        """Try test14."""
        with self.assertRaises(TypeError):
            Game.resolution_to_str(1920 * 1080)
