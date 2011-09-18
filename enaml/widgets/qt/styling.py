from traits.api import Instance, Dict
from .qt import QtCore, QtGui

from ...color import Color
from ...style_sheet import StyleSheet, StyleHandler, style, NO_STYLE
from ...style_converters import color_from_color_style

#-------------------------------------------------------------------------------
# Default wx style sheet definition
#-------------------------------------------------------------------------------
QT_STYLE_SHEET = StyleSheet(
    
    #---------------------------------------------------------------------------
    # Default style
    #---------------------------------------------------------------------------
    #style("*",
    #    size_policy = "expanding",
    #),

    #---------------------------------------------------------------------------
    # default type overrides
    #---------------------------------------------------------------------------
    #style("PushButton", "CheckBox", "SpinBox", "ComboBox",
    #    size_policy = "preferre",
    #),

    #style("SpinBox", "ComboBox", "Slider", "Panel", "LineEdit", "Field", "Label",
    #    stretch = 1,
    #),

    #style("Html", "Spacer",
    #    stretch = 2,
    #),

    #style("Group", "VGroup", "HGroup",
    #    spacing = 2,
    #),

    #---------------------------------------------------------------------------
    # Convienence style classes
    #---------------------------------------------------------------------------
    style(".error_colors",
        background_color = "error",
        color = "nocolor",
    ),

    style(".normal_colors",
        background_color = "nocolor",
        color = "nocolor",
    ),

    style(".fixed",
        size_policy = "minimum",
    ),

    style(".expanding",
        size_policy = "expanding",
    ),

    style(".no_stretch",
        stretch = 0,
    ),

    style(".stretch",
        stretch = 1,
    ),

    style(".x_stretch",
        stretch = 2,
    ),

    style(".xx_stretch",
        stretch = 3,
    ),

    style(".X_stretch",
        stretch = 4,
    ),

    style(".XX_stretch",
        stretch = 5,
    ),

    style(".no_padding",
        padding = 0,
    ),

    style(".padding",
        padding = 2,
    ),

    style(".x_padding",
        padding = 5,
    ),

    style(".xx_padding",
        padding = 10,
    ),

    style(".X_padding",
        padding = 20,
    ),

    style(".XX_padding",
        padding = 40,
    ),

)

#-------------------------------------------------------------------------------
# qt styling helper and conversion functions
#-------------------------------------------------------------------------------
Q_SIZE_POLICIES = {
    "fixed": QtGui.QSizePolicy.Fixed,
    "minimum": QtGui.QSizePolicy.Minimum,
    "maximum": QtGui.QSizePolicy.Maximum,
    "preferred": QtGui.QSizePolicy.Preferred,
    "expanding": QtGui.QSizePolicy.Expanding,
    "minimum_expanding": QtGui.QSizePolicy.MinimumExpanding,
    "ignored": QtGui.QSizePolicy.Ignored,
}


class QtStyleHandler(StyleHandler):
    """ StyleHandler subclass that understands how to set styles via Qt style sheets
    
    Attributes
    ----------
    
    widget : QWidget
        The underlying QWidget that we are interacting with.
    
    _qt_stylesheet_values : Dict
        A dictionary holding the current state.
    """

    widget = Instance(QtGui.QWidget)
    
    _qt_stylesheet_values = Dict

    def set_style_value(self, value, tag, converter):
        """Set the style given by the tag to the value in a generic way for Qt.
        
        This uses Qt's style sheet mechanism.
        
        Arguments
        ---------
        
        value : style_value
            The string representation of the style's value.
        
        tag : string
            The style tag that is being set.
        
        args : callable
            Callable that converts Enaml stylesheet value to Qt stylehseet
            values of the appropriate type for the tag.
        """
        qt_value = converter(value)
        key = tag.replace('_', '-')
        if qt_value is not None:
            self._qt_stylesheet_values[key] = qt_value
        else:
            self._qt_stylesheet_values.pop(key, None)
        stylesheet = generate_qt_stylesheet(self.widget.__class__.__name__,
                                            self._qt_stylesheet_values)         
        self.widget.setStyleSheet(stylesheet)

    def style_size_policy(self, size_policy):
        if size_policy is not NO_STYLE:
            widget = self.widget
            old = widget.sizePolicy()
            new = QtGui.QSizePolicy(old.horizontalPolicy(), 
                                    old.verticalPolicy())
            
            if isinstance(size_policy, (list, tuple)):
                hpolicy, vpolicy = size_policy
            else:
                hpolicy = vpolicy = size_policy
            
            hpolicy = Q_SIZE_POLICIES.get(hpolicy)
            vpolicy = Q_SIZE_POLICIES.get(vpolicy)
            
            if hpolicy is not None:
                new.setHorizontalPolicy(hpolicy)
            if vpolicy is not None:
                new.setVerticalPolicy(vpolicy)

            widget.setSizePolicy(new)


def generate_qt_stylesheet(class_name, values):
    """ Generate a Qt stylesheet string
    
    Arguments
    ---------
    
    class_name : string
        The name of the Qt class that is having its stylesheet set.
    
    values : dictionary
        A dictionary whose keys are Qt stylesheet property names and
        whose values are the corresponding string values to be used in
        the stylesheet.
    """
    templ = '%s { %s }'
    items = '; '.join(key+': '+value for key, value in values.items())
    return templ % (class_name, items)


ALIGN_MAP = {
    'top': QtCore.Qt.AlignTop,
    'right': QtCore.Qt.AlignRight,
    'bottom': QtCore.Qt.AlignBottom,
    'left': QtCore.Qt.AlignLeft,
    'hcenter': QtCore.Qt.AlignHCenter,
    'vcenter': QtCore.Qt.AlignVCenter,
    'center': QtCore.Qt.AlignCenter,
}


def qt_color_from_color(color):
    """ Converts an enaml.color.Color into a qt stylesheet color.

    """
    if color == Color.no_color:
        res = None
    else:
        res = 'rgb(%s, %s, %s, %s)' % (color.r, color.g, color.b, color.a)
    return res

def QColor_form_color(color):
    """ Converts an enaml.color.Color into a qt stylesheet color.

    """
    if color == Color.no_color:
        res = None
    else:
        res = QtGui.QColor(color.r, color.g, color.b, color.a)
    return res

def qt_color(color_style):
    color = color_from_color_style(color_style)
    return qt_color_from_color(color)

def qt_length(length_style):
    if length_style is NO_STYLE:
        return None
    return '%spx' % length_style

def qt_box_lengths(box_lengths):
    if box_lengths is NO_STYLE:
        return None
    if isinstance(box_lengths, (tuple, list)):
        return ' '.join(qt_length(x) for x in box_lengths)
    else:
        return qt_length(box_lengths)


#-------------------------------------------------------------------------------
# Standard property style models
#-------------------------------------------------------------------------------

qt_background_model = {
    'background_color': qt_color
}

qt_box_model = qt_background_model.copy()
qt_box_model.update({
    'padding': qt_box_lengths,
    'padding_top': qt_length,
    'padding_bottom': qt_length,
    'padding_left': qt_length,
    'padding_right': qt_length,    

    'margin': qt_box_lengths,
    'margin_top': qt_length,
    'margin_bottom': qt_length,
    'margin_left': qt_length,
    'margin_right': qt_length,    

    'border_width': qt_box_lengths,
    'border_top_width': qt_length,
    'border_bottom_width': qt_length,
    'border_left_width': qt_length,
    'border_right_width': qt_length,    
})

'''
def compute_sizer_flags(style):
    """ Computes wx sizer flags given a style node.

    """
    get_property = style.get_property
    padding_style = PaddingStyle.from_style_node(style)
    order = [wx.TOP, wx.RIGHT, wx.BOTTOM, wx.LEFT]
    border_flags = 0
    border_amt = -1

    for amt, flag in zip(padding_style.padding, order):
        if amt >= 0:
            border_amt = max(border_amt, amt)
            border_flags |= flag

    sizer_flags = wx.SizerFlags()
    
    if border_amt >= 0:
        sizer_flags.Border(border_flags, amt)

    align = get_property("align")
    if isinstance(align, basestring):
        align_spec = align.split()
        align_flags = 0
        for align in align_spec:
            align_flags |= ALIGN_MAP.get(align, 0)
        if align_flags != 0:
            sizer_flags.Align(align_flags)
    
    size_policy = get_property("size_policy")
    if isinstance(size_policy, basestring):
        size_policy_spec = size_policy.strip()
        if size_policy_spec == 'expanding':
            sizer_flags.Expand()

    stretch = get_property("stretch")
    if isinstance(stretch, int) and stretch >= 0:
        sizer_flags.Proportion(stretch)

    return sizer_flags

'''