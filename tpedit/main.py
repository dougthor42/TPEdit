# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Thu Jul 02 10:56:57 2015
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""
### Imports
# Standard Library
from __future__ import print_function, division
from __future__ import absolute_import
import logging
import os.path

# Third Party
import wx
import wx.gizmos as wxdv
from docopt import docopt
import bs4
from bs4 import BeautifulSoup

# Package / Application
try:
    # Imports used for unittests
#    from . import __init__ as __pybank_init
#    from . import pbsql
    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
#        import __init__ as __pybank_init
#        import pbsql
        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
#        from pybank import __init__ as __pybank_init
#        from pybank import pbsql
        logging.debug("imports for Executable")

__author__ = "Douglas Thor"
__version__ = "v0.1.0"

### Module Constants
HIGHLIGHT = wx.Colour(255, 255, 0)
HIGHLIGHT2 = wx.Colour(255, 128, 30)

ROOT_PATH = "C:\\WinPython27\\projects\\github\\TPEdit\\tpedit\\tests\\data"
FNs = ("PT_07G11_B.xml",
       "PT_07G13_B.xml",
       "PT_07G14_B.xml",
       "PT_07G16_B.xml",
       )

FPs = [os.path.join(ROOT_PATH, x) for x in FNs]


class MainApp(object):
    """
    """
    def __init__(self):
        self.app = wx.App()

        self.frame = MainFrame("gTPEditor_Mockup", (1200, 650))

        self.frame.Show()
        self.app.MainLoop()


class MainFrame(wx.Frame):
    """
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self._init_ui()

    def _init_ui(self):
        """ Initi UI Components """
        # Create the menu bar and bind events
        self.menu_bar = wx.MenuBar()
        self._create_menus()
        self._bind_events()

        # Initialize default states
#        self._set_defaults()

        # Set the MenuBar and create a status bar
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

        self._create_panel()

    def _create_panel(self):
        self.panel = MainPanel(self)

    def _create_menus(self):
        """ Create each menu for the menu bar """
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
#        self._create_tools_menu()
#        self._create_options_menu()
#        self._create_help_menu()

    def _create_file_menu(self):
        """
        Creates the File menu.

        wxIDs:
        ------
        + 101: New
        + 102: Open
        + 103: Exit

        """
        # Create the menu and items
        self.mfile = wx.Menu()
        self.mf_new = wx.MenuItem(self.mfile, wx.ID_NEW, "&New\tCtrl+N",
                                  "Create a new FTI Test Program file")
        self.mf_open = wx.MenuItem(self.mfile, wx.ID_OPEN, "&Open\tCtrl+O",
                                   "Open a Test Program file")
        self.mf_close = wx.MenuItem(self.mfile, wx.ID_CLOSE, "&Close",
                                    "Closes all open files")
        self.mf_exit = wx.MenuItem(self.mfile, wx.ID_EXIT, "&Exit\tCtrl+Q",
                                   "Exit the application")

        # Add menu items to the menu
        self.mfile.AppendItem(self.mf_new)
        self.mfile.AppendItem(self.mf_open)
        self.mfile.AppendItem(self.mf_close)
        self.mfile.AppendSeparator()
        self.mfile.AppendItem(self.mf_exit)
        self.menu_bar.Append(self.mfile, "&File")

    def _create_edit_menu(self):
        """
        Creates the Edit menu

        wxIDs:
        ------
        + 201: ???
        + 202: ???

        """
        # Create the menu and items
        self.medit = wx.Menu()
        self.me_temp = wx.MenuItem(self.medit, wx.ID_EDIT, "&Temp",
                                   "TempItem")

        # Add menu items to the menu
        self.medit.AppendItem(self.me_temp)
        self.menu_bar.Append(self.medit, "&Edit")

    def _create_view_menu(self):
        """
        Creates the View menu.

        wxIDs:
        ------
        + 301: ???
        + 302: ???
        """
        # Create the menu and items
        self.mview = wx.Menu()
        self.mv_expand_all = wx.MenuItem(self.mview, 301,
                                         "&Expand All", "Expand All")
        self.mv_collapse_all = wx.MenuItem(self.mview, 302,
                                           "&Collapse All", "Collapse All")

        # Add menu items to the menu
        self.mview.AppendItem(self.mv_expand_all)
        self.mview.AppendItem(self.mv_collapse_all)
        self.menu_bar.Append(self.mview, "&View")

    def _bind_events(self):
        """ Bind all initial events """
        # File Menu
        self.Bind(wx.EVT_MENU, self._on_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self._on_open, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._on_close, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self._on_exit, id=wx.ID_EXIT)

        # Edit Menu
#        self.Bind(wx.EVT_MENU, self._on_edit_menu1)

        # View Menu
#        self.Bind(wx.EVT_MENU, self._nothing)
        self.Bind(wx.EVT_MENU, self._on_expand_all, self.mv_expand_all)
        self.Bind(wx.EVT_MENU, self._on_collapse_all, self.mv_collapse_all)

        # Tools Menu

        # Options Menu

        # Help Menu

    def _on_new(self, event):
        self.panel.log.AppendText("'New' command not yet implemented.\n")

    def _on_open(self, event):
        # TODO: Fix that user needs to resize or min/max before panel shown.
        self._create_panel()
#        w, h = self.GetClientSize()
#        self.SetSize((w + 1, h + 1))
        self.Refresh()
        self.Update()

    def _on_close(self, event):
#        self.panel.tree.DeleteAllItems()
        self.panel.Destroy()

    def _on_expand_all(self, event):
        self.panel.tree.ExpandAll(self.panel.root)

    def _on_collapse_all(self, event):
        collapse_all(self.panel.tree)

    def _on_exit(self, event):
        """ Execute Exit actions """
#        logging.debug("on quit")
        self.Close(True)


class MainPanel(wx.Panel):
    """
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.diff_count = 0

        self._init_ui()

    def _init_ui(self):
        """
        """
        tree_style = (wx.TR_DEFAULT_STYLE
                      | wx.TR_ROW_LINES
                      | wx.TR_COLUMN_LINES
                      | wx.TR_FULL_ROW_HIGHLIGHT
                      )
        self.tree = wxdv.TreeListCtrl(self,
                                      wx.ID_ANY,
                                      style=tree_style,
                                      )

        self.tree.AddColumn("MainColumn")
        self.tree.AddColumn("DataType")
        self.tree.SetMainColumn(0)          # contains the tree
        self.tree.SetColumnWidth(0, 325)
        self.tree.SetColumnWidth(1, 140)

        # Add colulmns for each file
        for _n, fp in enumerate(FPs):
            _, fn = os.path.split(fp)
            self.tree.AddColumn(fn)
            self.tree.SetColumnWidth(_n + 2, 160)

        self.root = self.tree.AddRoot("root")

        # process each file into soup.
        soups = []
        for fp in FPs:
            with open(fp) as openf:
                soups.append(BeautifulSoup(openf, 'xml'))

        self._recurse(self.root, soups)

        # Expand some items by default
        self.tree.ExpandAll(self.root)

        # Add a logging window
        log_style = (wx.TE_MULTILINE
                     | wx.TE_PROCESS_ENTER
                     )
        self.log = wx.TextCtrl(self, wx.ID_ANY, style=log_style)

        log_txt = "# of differences found: {}\n"
        self.log.AppendText(log_txt.format(self.diff_count))

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.tree, 4, wx.EXPAND)
        self.vbox.Add(self.log, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

        self._bind_events()

    def _bind_events(self):
        """
        """
        main_win = self.tree.GetMainWindow()
        main_win.Bind(wx.EVT_RIGHT_DCLICK, self._on_right_dclick)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, None)

    def _on_right_dclick(self, event):
        """
        """
        pos = event.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        msg_text = """Right Double-clicking on an item will copy the value
too all open files:

Item: '{}', Value: '{}' propagated to all open files!"""
        if item:
            item_text = self.tree.GetItemText(item)
            col_text = self.tree.GetItemText(item, col)
            msg_text = msg_text.format(item_text, col_text)
            dialog = wx.MessageDialog(self,
                                      msg_text,
                                      "Item Propagated",
                                      wx.OK,
                                      )

        dialog.ShowModal()
        dialog.Destroy()

    def _recurse(self, parent, soups):
        """
        """
        skipped_items = ("FTI.Subsystems.Variables.Variables",
                         "FTI.TesterInstruments6.TesterInstruments",
                         "FTI.Subsystems.Coordinators.Coordinators",
                         )

        all_children = ((x for x in soup.children if x != '\n')
                        for soup in soups)
        for childs in zip(*all_children):
            # assume that the 1st file is the "master file" that everything
            # compares to.
            child = childs[0]

            # Ignore some stuff that I don't care about.
            if child.name in skipped_items:
                continue

            # if the child is "Properties" then the next two items are
            # going to be Name and Value
            if child.name == "Properties":
                # find the grandchildren
                grandchildren = ([x for x in _child.children if x != '\n']
                                 for _child in childs)

                # collect the names and values of the grandchildren
                names = []
                values = []
                for grandchild in grandchildren:
                    names.append(grandchild[0].string)
                    values.append(grandchild[1].string)

                # set the item name as the 1st item
                key = self.tree.AppendItem(parent, names[0])

                # add the units to the units column
                dtype = None
                try:
                    value = unicode(values[0])
                    dtype, _ = parse_dtype(value)
                except IndexError:
                    pass

                if dtype is None:
                    dtype = ""

                self.tree.SetItemText(key, dtype, 1)

                # add values to each column
                for _n, value in enumerate(values):
                    try:
                        value = unicode(value)
                        _, value = parse_dtype(value)
                    except IndexError:
                        pass
                    if value is None:
                        value = ""
                    self.tree.SetItemText(key, value, _n + 2)

                # If any values are different, highlight the row and parents
                if any(values[0] != x for x in values):
                    self._highlight_item_and_parents(key)

                continue

            # if we're at a NavigableString, then we need to add it
            if isinstance(child, bs4.element.NavigableString):
                # check for duplicates, highlight if true
                if any(childs[0].string != x.string for x in childs):
                    self._highlight_item_and_parents(parent)

                for _n, item in enumerate(childs):
                    self.tree.SetItemText(parent, item.string, _n + 2)

            # if the child is a tag, then we set it as the new parent
            # and recurse
            if isinstance(child, bs4.element.Tag):
                new_parent = self.tree.AppendItem(parent, child.name)
                self._recurse(new_parent, childs)

    def _highlight_item_and_parents(self, item):
        """ highlights an item row and parents """
        self.diff_count += 1
        self.tree.SetItemBackgroundColour(item, HIGHLIGHT)
        for parent in get_parents(self.tree, item):
            self.tree.SetItemBackgroundColour(parent, HIGHLIGHT2)


def get_parents(tree, item, retval=None):
    """ Gets all the parents of a tree item """
    if retval is None:
        retval = []
    try:
        parent = tree.GetItemParent(item)
        retval.append(parent)
        get_parents(tree, parent, retval)
    except AssertionError:
        # we're at the top, ignore the error and return.
        pass
    return retval[:-1]


def collapse_all(tree, item=None):
    """ collapse all items in a tree """
    if item is None:
        item = tree.GetRootItem()

    # get the first child, returning if no children exist.
    try:
        child = tree.GetFirstExpandedItem()
    except AssertionError:
        pass

    expanded_items = [item, child]
    while True:
        try:
            child = tree.GetNextExpanded(child)
        except:
            break
        expanded_items.append(child)

    for item in reversed(expanded_items):
        try:
            tree.Collapse(item)
        except:
            pass


def parse_dtype(string):
    """ parses a dtype from a string """
    soup = BeautifulSoup(string, 'xml')
    dtypes = [x.name for x in soup.find_all(True, recursive=True)]
    dtype = ".".join(dtypes)
    value = soup.find(dtypes[-1]).string
    return dtype, value


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)
    MainApp()


if __name__ == "__main__":
    main()
#    string = "<Double>-30</Double>"
#    string = "<A><B><C>value</C></B></A>"
#    parse_dtype(string)
