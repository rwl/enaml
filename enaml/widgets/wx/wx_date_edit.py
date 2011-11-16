#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import datetime

import wx

from .wx_bounded_date import WXBoundedDate

from ..date_edit import AbstractTkDateEdit


def to_wx_date(py_date):
    day = py_date.day
    month = py_date.month - 1 # wx peculiarity!
    year = py_date.year
    return wx.DateTimeFromDMY(day, month, year)


def from_wx_date(wx_date):
    if wx_date.IsValid():
        day = wx_date.GetDay()
        month = wx_date.GetMonth() + 1 # wx peculiarity!
        year = wx_date.GetYear()
        return datetime.date(year, month, day)


class WXDateEdit(WXBoundedDate, AbstractTkDateEdit):
    """ A WX implementation of DateEdit.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self):
        """ Creates the underlying wx.DatePickerCtrl.

        """
        self.widget = wx.DatePickerCtrl(self.parent_widget())

    def bind(self):
        """ Binds the event handlers for the date widget.

        """
        super(WXDateEdit, self).bind()
        self.widget.Bind(wx.EVT_DATE_CHANGED, self._on_date_changed)

    #--------------------------------------------------------------------------
    # Component attribute notifiers
    #--------------------------------------------------------------------------
    def shell_date_format_changed(self, date_format):
        """ The change handler for the 'format' attribute.

        .. note:: Changing the format on wx is not supported.
                  See http://trac.wxwidgets.org/ticket/10988

        """
        pass

    #--------------------------------------------------------------------------
    # Signal handlers
    #--------------------------------------------------------------------------
    def _on_date_changed(self, event):
        """ The event handler for the date's changed event.

        """
        shell = self.shell_obj
        new_date = from_wx_date(event.GetDate())
        shell.date = new_date
        shell.date_changed = new_date

    #--------------------------------------------------------------------------
    # Private methods
    #--------------------------------------------------------------------------
    def _set_date(self, date):
        """ Sets the date on the widget.

        """
        # wx will not fire an EVT_DATE_CHANGED event when the value is 
        # programmatically set, so the method fires the shell event 
        # manually after setting the value in the widget.
        self.widget.SetValue(to_wx_date(date))
        self.shell_obj.date_changed = date

    def _set_min_date(self, date):
        """ Sets the minimum date on the widget with the provided value.

        """
        widget = self.widget
        widget.SetRange(to_wx_date(date), widget.GetUpperLimit())

    def _set_max_date(self, date):
        """ Sets the maximum date on the widget with the provided value.

        """
        widget = self.widget
        widget.SetRange(widget.GetLowerLimit(), to_wx_date(date))

