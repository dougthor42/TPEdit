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
HIGHLIGHT = wx.Colour(255, 255, 0)
HIGHLIGHT2 = wx.Colour(255, 128, 30)

FP1 = "C:\\WinPython27\\projects\\github\\TPEdit\\tpedit\\tests\\data\\PT_07G11_B.xml"
FP2 = "C:\\WinPython27\\projects\\github\\TPEdit\\tpedit\\tests\\data\\PT_07G13_B.xml"


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
        self._bind_events()

        # Initialize default states
#        self._set_defaults()

        # Set the MenuBar and create a status bar
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

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
        self.me_temp = wx.MenuItem(self.medit, 201, "&Temp", "TempItem")

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
#        self.Bind(wx.EVT_MENU, self._on_new, id=101)
#        self.Bind(wx.EVT_MENU, self._on_open, id=102)
        self.Bind(wx.EVT_MENU, self._on_quit, id=103)

        # Edit Menu
#        self.Bind(wx.EVT_MENU, self._on_edit_menu1)

        # View Menu
#        self.Bind(wx.EVT_MENU, self._nothing)
        self.Bind(wx.EVT_MENU, self._on_expand_all, id=301)
        self.Bind(wx.EVT_MENU, self._on_collapse_all, id=302)

        # Tools Menu

        # Options Menu

        # Help Menu

    def _on_expand_all(self, event):
        self.panel.tree.ExpandAll(self.panel.root)

    def _on_collapse_all(self, event):
        self.panel.tree.Collapse()

    def _on_quit(self, event):
        """ Execute quit actions """
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
        with open(FP1) as openf:
            with open(FP2) as openf2:
                soup = BeautifulSoup(openf, 'xml')
                soup2 = BeautifulSoup(openf2, 'xml')
                self._recurse2(soup, soup2, self.root)

        # Expand some items by default
        self.tree.ExpandAll(self.root)

        # Add a logging window
        log_style = (wx.TE_MULTILINE
                     | wx.TE_PROCESS_ENTER
                     )
        self.log = wx.TextCtrl(self, wx.ID_ANY, style=log_style)

        self.log.SetValue("# of differences found: {}".format(self.diff_count))

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

    def _recurse(self, soup, parent=None):
        """
        Recursively traverses the XML and adds items to the GUI tree.
        """
        for child in soup.children:
            # if we're a navString, then we're at an element
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
#                    print(val)
                except IndexError:
                    val = child.string
                try:
                    self.tree.SetItemText(parent, val, 2)
                except TypeError:
                    pass
            # if we're a Tag, then we're probably at a tree
            elif isinstance(child, bs4.element.Tag):
                if len(child.contents) == 1:
                    if child.contents[0].string == "\n":
                        continue
#                    self.tree.AppendItem(parent, child.contents[0])
#                elif all(x == child.contents[0] for x in child.contents):
#                    print("same!")
                new_parent = self.tree.AppendItem(parent, child.name)
                self._recurse(child, new_parent)

    def _recurse2(self, soup, soup2, parent=None):
        """
        """
        skipped_items = ("FTI.Subsystems.Variables.Variables",
                         "FTI.TesterInstruments6.TesterInstruments",
                         "FTI.Subsystems.Coordinators.Coordinators",
                         )
        for child, child2 in zip((x for x in soup.children if x != '\n'),
                                 (x for x in soup2.children if x != '\n')):
            if child.name in skipped_items:
                continue

            # if the child is "Properties" then the next two items are
            # going to be Name and Value
            if child.name == "Properties":
                # find the grandchildren and set them as elements of the
                # *grandparent*.
                grandparent = self.tree.GetItemParent(parent)
                grandchildren = [x for x in child.children if x != '\n']
                grandchildren2 = [x for x in child2.children if x != '\n']
#                print(grandchildren['Name'])
                name = grandchildren[0].string
                value = grandchildren[1].string
                value2 = grandchildren2[1].string
                key = self.tree.AppendItem(parent, name)
                try:
                    value = unicode(value)
                    dtype, value = parse_dtype(value)
                    value2 = unicode(value2)
                    _, value2 = parse_dtype(value2)
                    self.tree.SetItemText(key, dtype, 1)
                except IndexError:
                    # the parse_dtype function was unable to get a value,
                    # most likely because there's no dtype tag
                    pass

                # Prevent TypeError on SetItemText (None != str or unicode)
                if value is None:
                    value = ""
                if value2 is None:
                    value2 = ""

                log_str = "Name: {: <15.15s}  Value: {: <15.15s}"
#                print(log_str.format(name, value))
                self.tree.SetItemText(key, value, 2)
                self.tree.SetItemText(key, value2, 3)
                if value != value2:
                    self.diff_count += 1
                    self.tree.SetItemBackgroundColour(key, HIGHLIGHT)
                    # also highlight all the parents
                    for _par in get_parents(self.tree, key):
                        self.tree.SetItemBackgroundColour(_par, HIGHLIGHT2)

                # don't recurse into this tree
                continue

            # if we're at a NavigableString, then we need to add it
            if isinstance(child, bs4.element.NavigableString):
                self.tree.SetItemText(parent, child.string, 2)
                self.tree.SetItemText(parent, child2.string, 3)
                # TODO: remove code duplication
                if child.string != child2.string:
                    self.diff_count += 1
                    self.tree.SetItemBackgroundColour(parent, HIGHLIGHT)
                    # also highlight all the parents
                    for _par in get_parents(self.tree, parent):
                        self.tree.SetItemBackgroundColour(_par, HIGHLIGHT2)

            # if the child is a tag, then we set it as the new parent
            # and recurse
            if isinstance(child, bs4.element.Tag):
                new_parent = self.tree.AppendItem(parent, child.name)
                self._recurse2(child, child2, new_parent)

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



def parse_dtype(string):
    """ parses a dtype from a string """
    soup = BeautifulSoup(string, 'xml')
    dtypes = [x.name for x in soup.find_all(True, recursive=True)]
    dtype = ".".join(dtypes)
    value = soup.find(dtypes[-1]).string
    return dtype, value


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
#    string = "<Double>-30</Double>"
#    string = "<A><B><C>value</C></B></A>"
#    parse_dtype(string)
