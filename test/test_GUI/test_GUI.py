import unittest
from App.GUI import view

class TestGUI(unittest.TestCase):

    async def _start_app(self):
        self.app.run()

    def setUp(self):
        self.app = view.get_root()

    def helper_assert_children(self, children):
        output = [child for child in children]
        return output
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
        output = self.app.children["!frame"].winfo_name()
        expected = "!frame"
        self.assertEqual(expected,output)

    def test_children_of_root(self):
        children = self.app.children
        output = self.helper_assert_children(children)
        expected = ['!frame', '!label', '!labelframe', '!notebook']
        self.assertEqual(expected,output)