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
import functools
import abc
import inspect
import datetime
import time

# Third Party
import wx
import wx.gizmos as wxdv
from docopt import docopt
import bs4
from bs4 import BeautifulSoup

# Package / Application
try:
    # Imports used for unittests
    from . import __init__ as __tpedit_init
    logging.debug("Imports for UnitTests")
except (SystemError, ValueError):
    try:
        # Imports used by Spyder
        import __init__ as __tpedit_init
        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
        from tpedit import __init__ as __tpedit_init
        logging.debug("imports for Executable")

__author__ = "Douglas Thor"
__version__ = "v0.1.0"

### Module Constants
HIGHLIGHT = wx.Colour(255, 255, 0)
HIGHLIGHT2 = wx.Colour(255, 128, 30)
DEFAULT_LOG_LEVEL = logging.INFO

ROOT_PATH = "C:\\WinPython27\\projects\\github\\TPEdit\\tpedit\\tests\\data"


def logged(func):
    """
    Decorator that logs entry and exit points of a function.
    """
    # Customize these messages
    entry_msg = '+Entering  {}'
    exit_msg = '-Exiting   {}. Exec took {:.6}ms'
    logger = logging.getLogger()

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        logger.debug(entry_msg.format(func.__name__))
#        start = datetime.datetime.utcnow()
        start = time.time()
        f_result = func(*args, **kwds)
#        end = datetime.datetime.utcnow()
        end = time.time()
#        elapsed = (end - start).total_seconds() * 1000
        elapsed = (end - start) * 1000
        logger.debug(exit_msg.format(func.__name__, elapsed))
        return f_result
    return wrapper


class LocalLogHandler(logging.StreamHandler):
    """
    A logging handler that directs logs to a ``target`` wx.TextCtrl.
    """
    def __init__(self, target):
        logging.StreamHandler.__init__(self)
        self.target = target

    def emit(self, record):
        msg = self.format(record)
        self.target.WriteText(msg + "\n")
        self.target.ShowPosition(self.target.GetLastPosition())
        self.flush()


def _init_logging(target, level=DEFAULT_LOG_LEVEL):
    """
    Initialize logging to the on-screen log
    """

    logfmt = ("%(asctime)s.%(msecs)03d"
              " [%(levelname)-8.8s]"    # Note implicit string concatenation.
              "  %(message)s"
              )
    datefmt = "%Y-%m-%d %H:%M:%S"
#    datefmt = "%H:%M:%S"

    logger = logging.getLogger()
    handler = LocalLogHandler(target)
    handler.setLevel(level)
    formatter = logging.Formatter(logfmt, datefmt)
    handler.setFormatter(formatter)
    handler.set_name("GUI Handler")
    logger.addHandler(handler)

    logging.info("GUI Logging Initialized, level = {}".format(level))


class MainApp(object):
    """
    """
    def __init__(self):
        self.app = wx.App()

        self.frame = MainFrame("TPEdit", (1200, 650))

        self.frame.Show()
        logging.info("App init complete")
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
        logging.info("Frame init complete")

    @logged
    def _init_ui(self):
        """ Initi UI Components """
        # normally I'd make the panel later, but I want to be able to log
        # things to it.
        self.panel = MainPanel(self)

        # Start logging.
        _init_logging(self.panel.log_panel.log)
        logging.info("Panel init complete")

        # Create the menu bar and bind events
        self.menu_bar = wx.MenuBar()
        self._create_menus()
        self._bind_events()

        # Initialize default states
        self._set_defaults()

        # Set the MenuBar and create a status bar
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

    @logged
    def _create_menus(self):
        """ Create each menu for the menu bar """
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
#        self._create_tools_menu()
#        self._create_options_menu()
#        self._create_help_menu()

    @logged
    def _set_defaults(self, default_log_level=DEFAULT_LOG_LEVEL):
        """
        """
        # TODO: refactor this hack
        try:
            if default_log_level == logging.DEBUG:
                logging.info("Setting log level to DEBUG.")
                self.sm_ll_debug.Check()
            elif default_log_level == logging.INFO:
                logging.info("Setting log level to INFO.")
                self.sm_ll_info_.Check()
            elif default_log_level == logging.WARNING:
                logging.info("Setting log level to WARNING.")
                self.sm_ll_warn_.Check()
            elif default_log_level == logging.ERROR:
                logging.info("Setting log level to ERROR.")
                self.sm_ll_error.Check()
            elif default_log_level == logging.CRITICAL:
                logging.info("Setting log level to CRITICAL.")
                self.sm_ll_crit_.Check()
            else:
                err_txt = "Invalid default log level `{}`."
                raise ValueError(err_txt.format(DEFAULT_LOG_LEVEL))
        except NameError:
            logging.warning("Default log level not found, setting to INFO.")
            default_log_level = logging.INFO
            self.sm_ll_info_.Check()
        except ValueError:
            logging.warning("Invalid default log level, setting to INFO.")
            default_log_level = logging.INFO
            self.sm_ll_info_.Check()
        except Exception:
            raise

    @logged
    def _create_file_menu(self):
        """
        Creates the File menu.
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

    @logged
    def _create_edit_menu(self):
        """
        Creates the Edit menu
        """
        # Create the menu and items
        self.medit = wx.Menu()
        self.me_temp = wx.MenuItem(self.medit,
                                   wx.ID_EDIT,
                                   "&Temp",
                                   "TempItem")

        self.sm_loglevel = wx.Menu()
        self.sm_ll_debug = wx.MenuItem(self.sm_loglevel,
                                       wx.ID_ANY,
                                       "&Debug",
                                       "Sets the log level to DEBUG",
                                       wx.ITEM_RADIO)
        self.sm_ll_info_ = wx.MenuItem(self.sm_loglevel,
                                       wx.ID_ANY,
                                       "&Info",
                                       "Sets the log level to INFO",
                                       wx.ITEM_RADIO)
        self.sm_ll_warn_ = wx.MenuItem(self.sm_loglevel,
                                       wx.ID_ANY,
                                       "&Warning",
                                       "Sets the log level to WARNING",
                                       wx.ITEM_RADIO)
        self.sm_ll_error = wx.MenuItem(self.sm_loglevel,
                                       wx.ID_ANY,
                                       "&Error",
                                       "Sets the log level to ERROR",
                                       wx.ITEM_RADIO)
        self.sm_ll_crit_ = wx.MenuItem(self.sm_loglevel,
                                       wx.ID_ANY,
                                       "&Critical",
                                       "Sets the log level to CRITICAL",
                                       wx.ITEM_RADIO)

        self.sm_loglevel.AppendItem(self.sm_ll_debug)
        self.sm_loglevel.AppendItem(self.sm_ll_info_)
        self.sm_loglevel.AppendItem(self.sm_ll_warn_)
        self.sm_loglevel.AppendItem(self.sm_ll_error)
        self.sm_loglevel.AppendItem(self.sm_ll_crit_)

        # Add menu items to the menu
        self.medit.AppendItem(self.me_temp)
        self.medit.AppendMenu(wx.ID_ANY,
                              "Logging Level",
                              self.sm_loglevel,
                              "Change the logging level.")
        self.menu_bar.Append(self.medit, "&Edit")

    @logged
    def _create_view_menu(self):
        """
        Creates the View menu.
        """
        # Create the menu and items
        self.mview = wx.Menu()
        self.mv_expand_all = wx.MenuItem(self.mview,
                                         wx.ID_ANY,
                                         "&Expand All",
                                         "Expand All")
        self.mv_collapse_all = wx.MenuItem(self.mview,
                                           wx.ID_ANY,
                                           "&Collapse All",
                                           "Collapse All")

        # Add menu items to the menu
        self.mview.AppendItem(self.mv_expand_all)
        self.mview.AppendItem(self.mv_collapse_all)
        self.menu_bar.Append(self.mview, "&View")

    @logged
    def _bind_events(self):
        """ Bind all initial events """
        # File Menu
        self.Bind(wx.EVT_MENU, self._on_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self._on_open, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._on_close, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self._on_exit, id=wx.ID_EXIT)

        # Edit Menu
        self.Bind(wx.EVT_MENU, self._on_loglevel_change, self.sm_ll_debug)
        self.Bind(wx.EVT_MENU, self._on_loglevel_change, self.sm_ll_info_)
        self.Bind(wx.EVT_MENU, self._on_loglevel_change, self.sm_ll_warn_)
        self.Bind(wx.EVT_MENU, self._on_loglevel_change, self.sm_ll_error)
        self.Bind(wx.EVT_MENU, self._on_loglevel_change, self.sm_ll_crit_)

        # View Menu
#        self.Bind(wx.EVT_MENU, self._nothing)
        self.Bind(wx.EVT_MENU, self._on_expand_all, self.mv_expand_all)
        self.Bind(wx.EVT_MENU, self._on_collapse_all, self.mv_collapse_all)

        # Tools Menu

        # Options Menu

        # Help Menu

    @logged
    def _on_loglevel_change(self, event):
        """ Process the log level change event """
        new_level = event.GetEventObject().GetLabelText(event.GetId()).upper()
        logging.info("Log Level Changed to {}".format(new_level))
        _set_log_level(new_level)

    @logged
    def _on_new(self, event):
        logging.warn("Command 'New' not yet implemented.")

    @logged
    def _on_open(self, event):
        self.close_files()
        self._open_file_dialog()

    @logged
    def _on_open_multiple(self, event):
        logging.warn("'Open Multiple' command not yet implemented.")

    @logged
    def _on_close(self, event):
        """ Delete all items in the tree and remove all file columns. """
        self.close_files()

    @logged
    def _on_expand_all(self, event):
        logging.info("Expanding all tree items.")
        self.panel.tree.ExpandAll(self.panel.root)

    @logged
    def _on_collapse_all(self, event):
        logging.info("Collapsing all tree items.")
        collapse_all(self.panel.tree)

    def _on_exit(self, event):
        """ Execute Exit actions """
        logging.info("Exiting app")
        self.Close(True)

    @logged
    def _open_file_dialog(self):
        """ Displayes the open file dialog """
        file_dialog_style = (wx.FD_OPEN
                             | wx.FD_FILE_MUST_EXIST
                             | wx.FD_MULTIPLE
                             )

        open_file_dialog = wx.FileDialog(self,
                                         "prompt",
                                         defaultDir=ROOT_PATH,
                                         defaultFile="",
                                         wildcard="XML Files (*.xml)|*.xml",
                                         style=file_dialog_style
                                         )

        if open_file_dialog.ShowModal() == wx.ID_CANCEL:
            # don't load
            logging.info("User canceled open dialog")
            return

        paths = open_file_dialog.GetPaths()
        for fp in paths:
            logging.info("  Chosen file: `{}`".format(fp))

        self.open_files(paths)



    @logged
    def open_files(self, paths):
        """ """
        # Reset the diff counter - don't want to double-count
        self.panel.edit_panel.diff_count = 0

        # make sure a root exists:
#        print(self.panel.tree.GetRootItem())
        try:
            self.panel.edit_panel.root = self.panel.edit_panel.tree.AddRoot("root")
        except AssertionError:
            # root already exists
            pass
        # process each file into soup.
        soups = []
        for _n, fp in enumerate(paths):
            with open(fp) as openf:
                _, fn = os.path.split(fp)
                logging.info("Processing `{}`".format(fn))
                soups.append(BeautifulSoup(openf, 'xml'))
                self.panel.edit_panel.tree.AddColumn(fn)
                self.panel.edit_panel.tree.SetColumnWidth(_n + 2, 160)
                self.panel.edit_panel.tree.SetColumnEditable(_n + 2)

        # TODO: get rid of the self.panel.edit_panel.tree.blah long accessor
        self.panel.edit_panel._build_element_tree_recursively(self.panel.edit_panel.root, soups)

        self.panel.edit_panel.tree.ExpandAll(self.panel.edit_panel.root)

        logging.info("Total {} differences found.".format(self.panel.edit_panel.diff_count))

    @logged
    def close_files(self):
        logging.info("Closing all files.")

        self.panel.edit_panel.tree.DeleteAllItems()
        for col in reversed(range(2, self.panel.edit_panel.tree.GetColumnCount())):
            self.panel.edit_panel.tree.RemoveColumn(col)


class MainPanel(wx.Panel):
    """
    Root Panel of the UI.

    Contains the EditPanel, where files are compared and edited, and the
    LogPanel.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self._init_ui()

    def _init_ui(self):

        self.edit_panel = EditPanel(self)
        self.log_panel = LogPanel(self)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.edit_panel, 4, wx.EXPAND)
        self.vbox.Add(self.log_panel, 1, wx.EXPAND)
        self.SetSizer(self.vbox)


class LogPanel(wx.Panel):
    """
    Logging window.

    Contains a read-only TextCtrl that displays logging messages.
    """
    def __init__(self, parent):
        """ Init the parent class and instance variables """
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self._init_ui()

    def _init_ui(self):
        """ Init the UI elements """
        log_style = (wx.TE_MULTILINE
                     | wx.TE_READONLY
                     | wx.HSCROLL
                     )
        self.log = wx.TextCtrl(self, wx.ID_ANY, style=log_style)
        monospace_font = wx.Font(10,
                                 family=wx.MODERN,
                                 style=wx.NORMAL,
                                 weight=wx.NORMAL,
                                 underline=False,
                                 face='Consolas',
                                 )
        self.log.SetFont(monospace_font)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.log, 1, wx.EXPAND)
        self.SetSizer(self.hbox)


class EditPanel(wx.Panel):
    """
    Primary Edit panel.

    Contains all of the logic for displaying and editing the XML files.
    """
    def __init__(self, parent):
        """ Init the parent class and instance variables """
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.diff_count = 0
        self.edit_col = -1

        self._init_ui()

        # must bind events *after* init because they rely on those ui elements
        self._bind_events()

    def _init_ui(self):
        """
        Init the UI elements
        """
        # A TreeListCtrl contains all of the XML
        tree_style = (wx.TR_DEFAULT_STYLE
                      | wx.TR_ROW_LINES
                      | wx.TR_COLUMN_LINES
                      | wx.TR_FULL_ROW_HIGHLIGHT
                      )
        self.tree = wxdv.TreeListCtrl(self,
                                      wx.ID_ANY,
                                      style=tree_style,
                                      )

        # Add the columns that always exist.
        self.tree.AddColumn("Item")
        self.tree.AddColumn("DataType")
        self.tree.SetMainColumn(0)          # contains the tree
        self.tree.SetColumnWidth(0, 325)
        self.tree.SetColumnWidth(1, 140)

        self.root = self.tree.AddRoot("root")

        # Expand some items by default
        self.tree.ExpandAll(self.root)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

    def _bind_events(self):
        """
        Bind various events for the Edit Panel
        """
        main_win = self.tree.GetMainWindow()
        main_win.Bind(wx.EVT_RIGHT_DCLICK, self._on_right_dclick)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_activate)
        self.tree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self._on_item_edit_start)
        self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self._on_item_edit_end)

    @logged
    def _on_right_dclick(self, event):
        """
        Placeholder for value propagation.
        """
        logging.info("Double-right click detected")
        pos = event.GetPosition()
        logging.info("  Pos: {}".format(pos))
        item, flags, col = self.tree.HitTest(pos)
        logging.info("  {} .. {} .. {}".format(item, flags, col))
        if item:
            item_text = self.tree.GetItemText(item)
            col_text = self.tree.GetItemText(item, col)
            log_str = "Item `{}: {}` propagated to all open files."
            log_str = log_str.format(item_text, col_text)
            logging.info(log_str)

    @logged
    def _on_activate(self, event):
        """
        Placeholder - logging only.
        """
        item_text = self.tree.GetItemText(event.GetItem())
        logging.info("item activated: {}".format(item_text))

    @logged
    def _on_item_edit_start(self, event):
        """
        Primary purpose: record which column is being edited (self.edit_col)
        """
        self.edit_col = event.GetInt()

        item_text = self.tree.GetItemText(event.GetItem())
        item_value = self.tree.GetItemText(event.GetItem(), self.edit_col)
        log_str = "Editing column {} for item `{}`"
        logging.info(log_str.format(self.edit_col, item_text))
        logging.info("  old value: `{}`".format(item_value))

    @logged
    def _on_item_edit_end(self, event):
        """
        http://docs.wxwidgets.org/trunk/classwx_tree_event.html
        """
        string = event.GetLabel()
        log_str = "Column {} changed to: `{}`"
        logging.info(log_str.format(self.edit_col, string))
        if event.IsEditCancelled():
            # I'm not sure when this would actually happen...
            #   It's not happening upon pressing ESC, so perhaps it only
            #   happens if EVT_TREE_BEGIN_LABEL_EDIT is vetoed?
            logging.info("Column edit canceled.")

    # TODO: move outside of the class?
    def _build_element_tree_recursively(self, parent, soups):
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
                self._build_element_tree_recursively(new_parent, childs)

    def _highlight_item_and_parents(self, item):
        """ highlights an item row and parents """
        self.diff_count += 1
        self.tree.SetItemBackgroundColour(item, HIGHLIGHT)
        for parent in get_parents(self.tree, item):
            self.tree.SetItemBackgroundColour(parent, HIGHLIGHT2)


@logged
def _set_log_level(level_str):
    """
    Sets the global logging level

    Parmeters:
    ----------
    level_str : string
        String representation of logging.level. Accpeted values are::

            DEBUG, INFO, WARN, WARNING, ERROR, CRITICAL

    Returns:
    --------
    None

    """
    # TODO: figure out a stdlib way to do this:
    levels = {50: "CRITICAL",
              40: "ERROR",
              30: "WARNING",
              20: "INFO",
              10: "DEBUG",
              }

    if level_str not in levels.values():
        raise ValueError("Invalid log level `{}`".format(level_str))

    # Get the Logger and the previous logging level
    logger = logging.getLogger()
    prev_level = logger.level
    new_level = getattr(logging, level_str)     # Get numeric value

    # Always record log level changes
    log_str = "Changing logging level from {} to {}."
    logging.log(99, log_str.format(levels[prev_level], levels[new_level]))

    # Set the logger and handler levels
    logger.setLevel(new_level)
    log_str = "Logging Handler `{}` set to {}."
    for handler in logger.handlers:
        handler.setLevel(new_level)
        logging.debug(log_str.format(handler.get_name(), level_str))
#    logging.info("Global Log level set to {}".format(level_str))


@logged
def get_parents(tree, item, retval=None):
    """
    Gets all the parents of a tree item, recursively.

    Parameters:
    -----------
    tree : wx.gizmos.TreeListCtrl object
        The tree to act on.

    item : wx._controls.TreeItemId
        The item to get the parent of.

    retval : list of wx._controls.TreeItemId
        Only used during recursion. A list containing all of the parents.

    Returns:
    --------
    retval : list of wx._controls.TreeItemId
        A list of all ancestors of `item`.

    """
    if retval is None:
        retval = []
    try:
        logging.debug("Getting parent of `{}`".format(tree.GetItemText(item)))
        parent = tree.GetItemParent(item)
        retval.append(parent)
        logging.debug("   Parent is: `{}`".format(tree.GetItemText(parent)))
        get_parents(tree, parent, retval)
    except AssertionError:
        # we're at the top, ignore the error and return.
        pass
    return retval[:-1]


@logged
def collapse_all(tree):
    """
    Collapse all items in a tree, recursively.

    Parameters:
    -----------
    tree : wx.gizmos.TreeListCtrl object
        The tree to act on.

    Returns:
    --------
    None

    """
    item = tree.GetRootItem()

    # get the first child, returning if no children exist.
    try:
        child = tree.GetFirstExpandedItem()
    except AssertionError:
        raise AssertionError("Root item has no children")
        return

    expanded_items = [item, child]
    while True:
        try:
            child = tree.GetNextExpanded(child)
        except:
            break
        expanded_items.append(child)

    for item in reversed(expanded_items):
        try:
            logging.debug("Collapsing `{}`".format(tree.GetItemText(item)))
            tree.Collapse(item)
        except:
            pass


@logged
def parse_dtype(string):
    """
    Parses a data type from an FTI value string.

    FTI value strings sometimes are of the form::

        &lt;Double&gt;6&lt;/Double&gt;

    which, after translating the HTML codes, becomes valid XML::

        <Double>6</Double>

    The tag name ``Double`` is the data type and the tag's value ``6`` is
    the value to return.

    Parmeters:
    ----------
    string : string
        The string to parse

    Returns:
    --------
    dtype : string
        The parsed data type

    value : string
        The parsed value

    """
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
