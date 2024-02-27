import unittest
from App.GUI import view

class TestGUI(unittest.TestCase):

    async def _start_app(self):
        self.app.run()

    def setUp(self):
        self.app = view

    def tearDown(self):
        self.app.destroy()
    def test_window(self):
        title_output = self.app.winfo_toplevel().title()
        expected = ""
        self.assertEqual(title_output,expected)