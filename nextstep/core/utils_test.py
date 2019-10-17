import unittest

from nextstep.core.utils import rebuild_cmdline


class UtilsTests(unittest.TestCase):
    def test_rebuild_cmdline(self):
        self.assertEqual(
            rebuild_cmdline(['/c', '--input', 'filename with spaces.exe']),
            '/c --input "filename with spaces.exe"'
        )
        self.assertEqual(
            rebuild_cmdline(['/c', '--input', 'filename.exe']),
            '/c --input "spaces.exe"'
        )

        self.assertRaises(ValueError, rebuild_cmdline, "bad data")
        self.assertRaises(ValueError, rebuild_cmdline, 12345)