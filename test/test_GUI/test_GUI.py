import unittest
from App.GUI import view

class TestGUI(unittest.TestCase):

    async def _start_app(self):
        self.app.run()

    def setUp(self):
        self.app = view.get_root()
    def test_window(self):
        title_output = self.app.winfo_toplevel().title()
        expected = 'RoadTax Renewal Tracker'
        self.assertEqual(expected,title_output)