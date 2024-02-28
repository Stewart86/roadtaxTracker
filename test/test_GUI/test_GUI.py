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
        self.assertEqual(expected, title_output)

    def test_window_width(self):
        width_output = self.app.winfo_width()
        expected = 1024
        self.assertEqual(expected, width_output)

    def test_window_height(self):
        height_output = self.app.winfo_height()
        expected = 686
        self.assertEqual(expected, height_output)

    def test_title_frame(self):
        output = self.app.children["!frame"].winfo_name()
        expected = "!frame"
        self.assertEqual(expected, output)

    def test_children_of_root(self):
        children = self.app.children
        output = self.helper_assert_children(children)
        expected = ['!frame', '!label', '!labelframe', '!notebook']
        self.assertEqual(expected, output)

    def test_children_of_frame(self):
        children = self.app.children["!frame"].children
        output = self.helper_assert_children(children)
        expected = ['!label']
        self.assertEqual(expected, output)

    def test_children_of_notebook(self):
        children = self.app.children["!notebook"].children
        output = self.helper_assert_children(children)
        expected = ['!frame']
        self.assertEqual(expected, output)

    def test_children_of_frame_notebook(self):
        children = self.app.children["!notebook"].children["!frame"].children
        output = self.helper_assert_children(children)
        expected = ['!label',
                    '!treeview',
                    '!scrollbar',
                    '!entry',
                    '!checkbutton',
                    '!checkbutton2',
                    '!checkbutton3',
                    '!button']
        self.assertEqual(expected, output)


    def test_children_of_scrollbar(self):
        children = self.app.children["!notebook"].children["!frame"].children["!scrollbar"].children
        output = self.helper_assert_children(children)
        expected = []
        self.assertEqual(expected,output)

    def test_children_of_treeview(self):
        children = self.app.children["!notebook"].children["!frame"].children["!treeview"].children
        output = self.helper_assert_children(children)
        expected = []
        self.assertEqual(expected,output)

    def test_frame_notebook_button(self):
        output = self.app.children["!notebook"].children["!frame"].children["!button"].invoke()
        expected = 'None'
        self.assertEqual(expected,output)

    def test_frame_notebook_checkbutton1(self):
        output = self.app.children["!notebook"].children["!frame"].children["!checkbutton"].invoke()
        expected = 'None'
        self.assertEqual(expected,output)


    def test_frame_notebook_checkbutton2(self):
        output = self.app.children["!notebook"].children["!frame"].children["!checkbutton2"].invoke()
        expected = ''
        self.assertEqual(expected,output)


    def test_frame_notebook_checkbutton3(self):
        output = self.app.children["!notebook"].children["!frame"].children["!checkbutton3"].invoke()
        expected = ''
        self.assertEqual(expected,output)