from traits.api import implements

from ...constructors import IToolkitConstructor, BaseToolkitCtor


#-------------------------------------------------------------------------------
# Constructor helper mixins
#-------------------------------------------------------------------------------
class WrapWindowMixin(object):
    """ A mixin that wraps a constructor in a CocoaWindowCtor

    """
    def __call__(self, **ctxt_objs):
        # A container is not directly viewable, 
        # it must first be wrapped in a window.
        window_ctor = CocoaWindowCtor(
            children=[
                self,
            ],
        )
        return window_ctor(**ctxt_objs)


class WrapWindowVGroupMixin(WrapWindowMixin):
    """ A mixin that wraps a constructor in a CocoaWindowCtor with
    a CocoaVGroupCtor as its container.

    """
    def __call__(self, **ctxt_objs):
        # An element is not directly viewable, it must 
        # first be wrapped in a window and container.
        window_ctor = CocoaWindowCtor(
            children=[
                CocoaVGroupCtor(
                    children=[
                        self,
                    ],
                ),
            ],
        )
        return window_ctor(**ctxt_objs)


#-------------------------------------------------------------------------------
# Base Constructors
#-------------------------------------------------------------------------------
class CocoaBaseWindowCtor(BaseToolkitCtor):
    pass


class CocoaBasePanelCtor(BaseToolkitCtor, WrapWindowVGroupMixin):
    pass


class CocoaBaseContainerCtor(BaseToolkitCtor, WrapWindowMixin):
    
    def construct(self):
        # Replace any toplevel windows with panel constructors.
        # This facilitates composing other toplevel windows into 
        # another window. Also, the IPanel interface has no 
        # attributes, so we don't need (or want) to copy over
        # the exprs from then window constuctor, just the metas
        # and the children.
        children = self.children
        for idx, child in enumerate(children):
            if isinstance(child, CocoaBaseWindowCtor):
                window_children = child.children
                window_metas = child.metas
                children[idx] = CocoaPanelCtor(children=window_children,
                                            metas=window_metas)
        super(CocoaBaseContainerCtor, self).construct()


class CocoaBaseComponentCtor(BaseToolkitCtor, WrapWindowVGroupMixin):
    pass


#-------------------------------------------------------------------------------
# Window constructors
#-------------------------------------------------------------------------------
class CocoaWindowCtor(CocoaBaseWindowCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..window import Window
        from .cocoa_window import CocoaWindow
        window = Window(toolkit_impl=CocoaWindow())
        return window


class CocoaDialogCtor(CocoaBaseWindowCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..dialog import Dialog
        from .cocoa_dialog import CocoaDialog
        dialog = Dialog(toolkit_impl=CocoaDialog())
        return dialog


#-------------------------------------------------------------------------------
# Panel Constructors
#-------------------------------------------------------------------------------
class CocoaPanelCtor(CocoaBasePanelCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..panel import Panel
        from .cocoa_panel import CocoaPanel
        panel = Panel(toolkit_impl=CocoaPanel())
        return panel


#-------------------------------------------------------------------------------
# Container Constructors
#-------------------------------------------------------------------------------
class CocoaFormCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..form import Form
        from .cocoa_form import CocoaForm
        form = Form(_impl=CocoaForm())
        return form


class CocoaGroupCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..group import Group
        from .cocoa_group import CocoaGroup
        group = Group(toolkit_impl=CocoaGroup())
        return group


class CocoaVGroupCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..vgroup import VGroup
        from .cocoa_vgroup import CocoaVGroup
        vgroup = VGroup(toolkit_impl=CocoaVGroup())
        return vgroup


class CocoaHGroupCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..hgroup import HGroup
        from .cocoa_hgroup import CocoaHGroup
        hgroup = HGroup(toolkit_impl=CocoaHGroup())
        return hgroup


class CocoaStackedGroupCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..stacked_group import StackedGroup
        from .cocoa_stacked_group import CocoaStackedGroup
        stacked_group = StackedGroup(toolkit_impl=CocoaStackedGroup())
        return stacked_group


class CocoaTabGroupCtor(CocoaBaseContainerCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..tab_group import TabGroup
        from .cocoa_tab_group import CocoaTabGroup
        tab_group = TabGroup(toolkit_impl=CocoaTabGroup())
        return tab_group


#-------------------------------------------------------------------------------
# Element Constructors
#-------------------------------------------------------------------------------
class CocoaGroupBoxCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..group_box import GroupBox
        from .cocoa_group_box import CocoaGroupBox
        group_box = GroupBox(toolkit_impl=CocoaGroupBox())
        return group_box


class CocoaCalendarCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..calendar import Calendar
        from .cocoa_calendar import CocoaCalendar
        calendar = Calendar(toolkit_impl=CocoaCalendar())
        return calendar


class CocoaCheckBoxCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..check_box import CheckBox
        from .cocoa_check_box import CocoaCheckBox
        check_box = CheckBox(toolkit_impl=CocoaCheckBox())
        return check_box


class CocoaComboBoxCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..combo_box import ComboBox
        from .cocoa_combo_box import CocoaComboBox
        combo_box = ComboBox(toolkit_impl=CocoaComboBox())
        return combo_box


class CocoaFieldCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..field import Field
        from .cocoa_field import CocoaField
        field = Field(toolkit_impl=CocoaField())
        return field


class CocoaHtmlCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..html import Html
        from .cocoa_html import CocoaHtml
        html = Html(toolkit_impl=CocoaHtml())
        return html


class CocoaImageCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..image import Image
        from .cocoa_image import CocoaImage
        image = Image(toolkit_impl=CocoaImage())
        return image


class CocoaLabelCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..label import Label
        from .cocoa_label import CocoaLabel
        label = Label(toolkit_impl=CocoaLabel())
        return label


class CocoaLineEditCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..line_edit import LineEdit
        from .cocoa_line_edit import CocoaLineEdit
        line_edit = LineEdit(toolkit_impl=CocoaLineEdit())
        return line_edit


class CocoaPushButtonCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..push_button import PushButton
        from .cocoa_push_button import CocoaPushButton
        push_button = PushButton(toolkit_impl=CocoaPushButton())
        return push_button


class CocoaRadioButtonCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..radio_button import RadioButton
        from .cocoa_radio_button import CocoaRadioButton
        radio_button = RadioButton(toolkit_impl=CocoaRadioButton())
        return radio_button


class CocoaSliderCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..slider import Slider
        from .cocoa_slider import CocoaSlider
        slider = Slider(toolkit_impl=CocoaSlider())
        return slider


class CocoaSpinBoxCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..spin_box import SpinBox
        from .cocoa_spin_box import CocoaSpinBox
        spin_box = SpinBox(toolkit_impl=CocoaSpinBox())
        return spin_box
        
        
class CocoaTraitsUIItemCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..traitsui_item import TraitsUIItem
        from .cocoa_traitsui_item import CocoaTraitsUIItem
        traitsui_item = TraitsUIItem(toolkit_impl=CocoaTraitsUIItem())
        return traitsui_item
        
        
class CocoaEnableCanvasCtor(CocoaBaseComponentCtor):

    implements(IToolkitConstructor)

    def component(self):
        from ..enable_canvas import EnableCanvas
        from .cocoa_enable_canvas import CocoaEnableCanvas
        canvas = EnableCanvas(toolkit_impl=CocoaEnableCanvas())
        return canvas
