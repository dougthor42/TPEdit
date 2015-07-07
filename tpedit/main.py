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
YELLOW = wx.Colour(255, 255, 0)
FP = "C:\\WinPython27\\projects\\github\\TPEdit\\tpedit\\tests\\data\\2.xml"


### Classes

class XmlElement(object):
    """
    A XML element.

    For FTI files, these are of the format:
    <Name>TestNumber</Name>
    <Value>&lt;unsignedInt&gt;10&lt;/unsignedInt&gt;</Value>
    <Value>&lt;boolean&gt;false&lt;/boolean&gt;</Value>

    where "&lt;" means "<"
    and   "&gt;" means ">"

    It seems like "Value" tags will *sometimes* contain these type
    specifiers while "Name" tags will never have types.

    """
    def __init__(self, name, dtype, value):
        self._name = name
        self._dtype = dtype  # default to enum.String?
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, val):
        self._dtype = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.value = val


class ParseTP(object):
    """
    Parses a Test Program file.

    Parameters:
    -----------
    fp : file path (string)
        The absolute path of the file to parse.

    Returns:
    --------
    None

    Notes:
    ------
    ????

    Attributes:
    -----------
    ????

    Methods:
    --------
    ???

    Private Attributes:
    -------------------
    ???

    Private Methods:
    ----------------
    ???

    """
    def __init__(self, fp):
        self.fp = fp

        # open the file
        with open(self.fp) as openf:
            self.parse(openf)

    def parse(self, openf):
        """ Parses the entire file or string """
        self.soup = BeautifulSoup(openf, "xml")

        if len(self.soup.contents) == 0:
            raise EOFError("The OFX file was empty I guess?")

        recurse(self.soup)


def recurse(soup):
    """
    """
    for child in soup.children:
        if isinstance(child, bs4.element.NavigableString):
            if child.string == "\n":
                continue
            elem_name = child.string
            print("adding value:        {}".format(elem_name))
        elif isinstance(child, bs4.element.Tag):
            l = len(list(child.children))
            if l != 1:
                print("adding section:  {}".format(child.name))
            else:
                print("adding element:    {}".format(child.name))
            recurse(child)
    return



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
#        self._bind_events()

        # Initialize default states
#        self._set_defaults()

        # Set the MenuBar and create a status bar
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

        self.panel = MainPanel(self)

    def _create_menus(self):
        """ Create each menu for the menu bar """
        self._create_file_menu()
#        self._create_edit_menu()
#        self._create_view_menu()
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
        self.mf_new = wx.MenuItem(self.mfile, 101, "&New\tCtrl+N",
                                  "Create a new FTI Test Program file")
        self.mf_open = wx.MenuItem(self.mfile, 102, "&Open\tCtrl+O",
                                   "Open a Test Program file")
        self.mf_exit = wx.MenuItem(self.mfile, 103, "&Exit\tCtrl+Q",
                                   "Exit the application")

        # Add menu items to the menu
        self.mfile.AppendItem(self.mf_new)
        self.mfile.AppendItem(self.mf_open)
        self.mfile.AppendSeparator()
        self.mfile.AppendItem(self.mf_exit)
        self.menu_bar.Append(self.mfile, "&File")


class MainPanel(wx.Panel):
    """
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self._init_ui()

    def _init_ui(self):
        """
        """
        tree_style = (wx.TR_DEFAULT_STYLE
#                      | wx.TR_HAS_BUTTONS
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
        self.tree.AddColumn("TestProgram 1")
        self.tree.AddColumn("TestProgram 2")
        self.tree.AddColumn("TestProgram 3")
        self.tree.SetMainColumn(0)          # contains the tree
        self.tree.SetColumnWidth(0, 325)
        self.tree.SetColumnWidth(1, 200)
        self.tree.SetColumnWidth(2, 220)
        self.tree.SetColumnWidth(3, 220)
        self.tree.SetColumnWidth(4, 220)

        self.root = self.tree.AddRoot("root")

        # add buncha items
        with open(FP) as openf:
            soup = BeautifulSoup(openf, 'xml')
            self._recurse(soup, self.root)


        # Expand some items by default
        self.tree.ExpandAll(self.root)

        # Add a logging window
        log_style = (wx.TE_MULTILINE
                     | wx.TE_PROCESS_ENTER
                     )
        self.log = wx.TextCtrl(self, wx.ID_ANY, style=log_style)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.tree, 4, wx.EXPAND)
        self.vbox.Add(self.log, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

        self._bind_events()

    def _bind_events(self):
        """
        """
        self.tree.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self._on_dclick)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, None)

    def _on_dclick(self, event):
        """
        """
        pos = event.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        msg_text = """Double-clicking on an item will copy the value
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

    def _recurse(self, soup, parent=None):
        """
        Recursively traverses the XML and adds items to the GUI tree.
        """
        for child in soup.children:
            # if we're a navString, then we're probably at an element
            if isinstance(child, bs4.element.NavigableString):
                # ignore newline elements
                if child.string == "\n":
                    continue
                # Set the item text for the column.
                # TODO: pull the data type from child.string
                try:
                    new_soup = BeautifulSoup(child.string, "xml")
                    dtype = new_soup.contents[0].name
                    val = new_soup.contents[0].string
                    self.tree.SetItemText(parent, new_soup.contents[0].name, 1)
                    print(val)
                except IndexError:
                    val = child.string
                self.tree.SetItemText(parent, val, 2)
            # if we're a Tag, then we're probably at a tree
            elif isinstance(child, bs4.element.Tag):
                # TODO: refactor
                if len(child.contents) == 1:
                    if child.contents[0].string == "\n":
                        continue
                new_parent = self.tree.AppendItem(parent, child.name)
                self._recurse(child, new_parent)

    def parse_dtype(string):
        """ parses a dtype from a string """
        pass


def add_tp_values(tree, child, value):
    """ """
    for _i in range(2, 5):
        tree.SetItemText(child, value, _i)


def add_attribute(tree, parent, name, databype, value):
    """ """
    child = tree.AppendItem(parent, name)
    tree.SetItemText(child, databype, 1)
    add_tp_values(tree, child, value)


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)
    MainApp()


if __name__ == "__main__":
    main()
