#------------------------------------------------------------------------------
# Copyright (C) 2011 Enthought, Inc.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

""" Subclasses of standard IComponents that add a `resized` signal that will
pass on notifications of resize events to Enaml.

"""

from abc import ABCMeta


class MResizingWidget(object):
    """ An abstract base class for testing if a IComponent subclass exposes
    a `resized` signal.

    """
    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, C):
        """ Check if a class is an IComponent that has the `resized` signal.

        """
        if issubclass(C, IComponent):
            if any(isinstance(getattr(B, "resized", None), QtCore.Signal) for B in C.__mro__):
                return True
        return NotImplemented


MixinBaseClass = object


class ResizingMixin(MixinBaseClass):
    """ Add a `resized` signal to the widget and a `resizeEvent()` method that
    emits the signal.

    """

    resized = None

    def resizeEvent(self, event):
        super(ResizingMixin, self).resizeEvent(event)
        self.resized.emit()


class LayoutDebugMixin(MixinBaseClass):
    """ A mixin that can be added to a container widget to draw the positions of
    its children.

    """

    def paintEvent(self, event):
        super(LayoutDebugMixin, self).paintEvent(event)
        qp = QtGui.QPainter()
        qp.begin(self)
        try:
            qp.setPen(QtGui.QColor(0, 0, 0))
            for child in self.children():
                layout_item = QtGui.QWidgetItem(child)
                geom = layout_item.geometry()
                qp.drawRect(geom)
        finally:
            qp.end()


class MResizingFrame(ResizingMixin, Panel):
    """ A Panel subclass that passes its resize events back to Enaml.

    """

class MResizingDialog(ResizingMixin, Window):
    """ A Window subclass that passes its resize events back to Enaml.

    """


class MResizingGroupBox(ResizingMixin, VerticalLayout):
    """ A VerticalLayout subclass that passes its resize events back to Enaml.

    """


class QResizingStackedWidget(ResizingMixin, QtGui.QStackedWidget):
    """ A QStackedWidget subclass that passes its resize events back to Enaml through
    a Qt signal.

    """


class QResizingScrollArea(ResizingMixin, QtGui.QScrollArea):
    """ A QScrollArea subclass that passes its resize events back to Enaml through
    a Qt signal.

    """


class QResizingTabWidget(ResizingMixin, QtGui.QTabWidget):
    """ A QTabWidget subclass that passes its resize events back to Enaml
    through a Qt signal.

    """


class QResizingSplitter(ResizingMixin, QtGui.QSplitter):
    """ A QSplitter subclass that passes its resize events back to Enaml through
    a Qt signal.

    """

