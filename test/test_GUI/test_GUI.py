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

    def test_window_width(self):
        width_output = self.app.winfo_width()
        expected = 1024
        self.assertEqual(expected,width_output)


    def test_window_height(self):
        height_output = self.app.winfo_height()
        expected = 686
        self.assertEqual(expected,height_output)

    def test_title_frame(self):
        name_title_fram = self.app.titleframe.winfo_name()
        expected = ''
        self.assertEqual(expected,name_title_fram)

    def test_update_button(self):
        output = self.app.update.invoke()
        expected = None
        self.assertEqual(expected,output)