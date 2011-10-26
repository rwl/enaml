#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import TraitError

from .enaml_test_case import EnamlTestCase, required_method
from enaml.enums import TickPosition
from enaml.util.enum import Enum

class TestEvents(Enum):
    """ Events required by the testcase. """

    #: The left button is pressed
    PRESSED = 0x0

    #: The left button is released
    RELEASED = 0x1

    #: The thumb is moved one step up
    STEP_UP = 0x2

    #: The thumb is moved one step down
    STEP_DOWN = 0x3

    #: The thumb is moved one page up
    PAGE_UP = 0x4

    #: The thumb is moved one page down
    PAGE_DOWN = 0x5

    #: The thumb is moved to home
    HOME = 0x6

    #: The thumb is moved to the end
    END = 0x7


class TestSlider(EnamlTestCase):
    """ Logic for testing sliders.


    Tooklit testcases need to provide the following methods

    Abstract Methods
    ----------------
    get_value(self, widget)
        Get the Slider's value.

    get_tick_interval(self, widget)
        Get the Slider's tick_interval value.

    get_tick_position(self, widget)
        Get the Slider's tick position style.

    get_orientation(self, widget)
        Get the Slider's orientation.

    get_single_step(self, widget)
        Get the Slider's single step value.

    get_page_step(self, widget)
        Get the Slider's page step value.

    get_tracking(self, widget)
        Get the Slider's tracking status.

    send_event(self, widget, event)
        Send an event to the Slider programmatically.

    """

    def setUp(self):
        """ Set up before the spin box tests.

        """

        enaml = """
defn MainWindow(events):
    Window:
        Slider -> slider:
            moved >> events.append(('moved', args.new))
            pressed >> events.append('pressed')
            released >> events.append('released')
"""

        self.events = []
        self.view = self.parse_and_create(enaml, events=self.events)
        self.component = self.component_by_name(self.view, 'slider')
        self.widget = self.component.toolkit_widget

    def test_initial_attributes(self):
        """ Compare the Enaml Slider's attributes with its toolkit widget.

        """
        component = self.component

        self.assertFalse(component.error)
        self.assertIsNone(component.exception)

        self.assertEnamlInSync(component, 'value', 0)
        self.assertEnamlInSync(component, 'minimum', 0)
        self.assertEnamlInSync(component, 'maximum', 100)
        self.assertEnamlInSync(component, 'tick_interval', 10)
        # while the initial value of the tick position is DEFAULT inside the
        # enaml object is converted to NO_TICKS
        self.assertEnamlInSync(component, 'tick_position', TickPosition.NO_TICKS)
        self.assertEnamlInSync(component, 'orientation', 'vertical')
        self.assertEnamlInSync(component, 'single_step', 1)
        self.assertEnamlInSync(component, 'page_step', 10)
        self.assertEqual(self.events, [])


    def test_tracking_attribute(self):
        """ Test accesing tracking attribute.

        """
        component = self.component

        self.assertEnamlInSync(component, 'tracking', True)

        component.tracking = False
        self.assertEnamlInSync(component, 'tracking', False)
        self.assertEqual(self.events, [])


    def test_change_maximum(self):
        """ Test changing the maximum range of the slider.

        """
        component = self.component
        component.maximum = 200
        self.assertEnamlInSync(component, 'maximum', 200)

    def test_change_minimum(self):
        """ Test changing the minimum range of the slider.

        """
        component = self.component
        component.value = 70
        component.minimum = 50
        self.assertEnamlInSync(component, 'minimum', 50)
        self.assertEqual(self.events, [('moved',70)])

    def test_change_maximum_invalid(self):
        """ Test attempting to set an invalid value to the maximum range of the slider.

        """
        component = self.component
        with self.assertRaises(TraitError):
            component.maximum = -23
        component.minimum = 50
        with self.assertRaises(TraitError):
            component.maximum = 23
        self.assertEqual(self.events, [('moved',50)])

    def test_change_minimum_invalid(self):
        """ Test attempting to set an invalid value to the minimum range of the slider.

        """
        component = self.component
        with self.assertRaises(TraitError):
            component.minimum = -13
        with self.assertRaises(TraitError):
            component.minimum = 135
        self.assertEqual(self.events, [])

    def test_change_maximum_and_value(self):
        """ Test setting maximum while the value is out of range.

        """
        component = self.component
        component.value = 70
        self.assertEnamlInSync(component, 'value', 70)
        component.maximum = 50
        self.assertEnamlInSync(component, 'value', 50)
        self.assertEqual(self.events, [('moved',70), ('moved',50)])

    def test_change_minimum_and_value(self):
        """ Test setting minimum while the value is out of range.

        """
        component = self.component
        component.value = 30
        component.minimum = 50
        self.assertEnamlInSync(component, 'value', 50)
        self.assertEqual(self.events, [('moved',30), ('moved',50)])


    def test_value_change(self):
        """Test changing the value programmaticaly.

        """
        component = self.component
        component.value = 1
        self.assertEnamlInSync(component, 'value', 1)
        component.value = 34
        self.assertEnamlInSync(component, 'value', 34)
        self.assertEqual(self.events, [('moved',1), ('moved',34)])

    def test_invalid_value_change(self):
        """ Test changing the position with the an invalid value

        when invalid, check that it has not changed the values and the
        errors are updated.
        """
        component = self.component

        with self.assertRaises(TraitError):
            component.value = -2
        with self.assertRaises(TraitError):
            component.value = 120

    def test_orientation_setting(self):
        """ Test changing the widget orientation

        """
        component = self.component

        self.component.orientation = 'vertical'
        self.assertEnamlInSync(component, 'orientation', 'vertical')

        self.component.orientation = 'horizontal'
        self.assertEnamlInSync(component, 'orientation', 'horizontal')

    def test_tick_position_setting(self):
        """ Test changing the widget tickposition

        """
        component = self.component

        component.tick_position = TickPosition.BOTTOM
        self.assertEnamlInSync(component, 'tick_position', TickPosition.BOTTOM)

        component.tick_position = TickPosition.TOP
        self.assertEnamlInSync(component, 'tick_position', TickPosition.TOP)

        component.tick_position = TickPosition.BOTH
        self.assertEnamlInSync(component, 'tick_position', TickPosition.BOTH)

        self.component.orientation = 'vertical'

        component.tick_position = TickPosition.LEFT
        self.assertEnamlInSync(component, 'tick_position', TickPosition.LEFT)

        component.tick_position = TickPosition.RIGHT
        self.assertEnamlInSync(component, 'tick_position', TickPosition.RIGHT)

        component.tick_position = TickPosition.BOTH
        self.assertEnamlInSync(component, 'tick_position', TickPosition.BOTH)

        component.tick_position = TickPosition.NO_TICKS
        self.assertEnamlInSync(component, 'tick_position', TickPosition.NO_TICKS)

    def test_incompatible_tick_position(self):
        """ Test that changing tick position is addapted if the orientation
        is not compatible.

        This is in sync with how the QSlider behaves.

        """

        component = self.component

        component.tick_position = TickPosition.LEFT
        self.assertEnamlInSync(component, 'tick_position', TickPosition.TOP)

        component.tick_position = TickPosition.RIGHT
        self.assertEnamlInSync(component, 'tick_position', TickPosition.BOTTOM)

        self.component.orientation = 'vertical'

        component.tick_position = TickPosition.BOTTOM
        self.assertEnamlInSync(component, 'tick_position', TickPosition.RIGHT)

        component.tick_position = TickPosition.TOP
        self.assertEnamlInSync(component, 'tick_position', TickPosition.LEFT)


    def test_changing_orientaion_tick_policy(self):
        """ Test that the ticks follow the orientation changes

        """
        component = self.component

        component.tick_position = TickPosition.BOTTOM
        self.component.orientation = 'vertical'
        self.assertEnamlInSync(component, 'tick_position', TickPosition.RIGHT)
        component.tick_position = TickPosition.LEFT
        self.component.orientation = 'horizontal'
        self.assertEnamlInSync(component, 'tick_position', TickPosition.TOP)


    def test_pressing_the_thumb(self):
        """ Test firing events when the thumb is pressed down.

        """
        events = self.events
        component = self.component
        component.value = 50
        self.send_event(self.widget, TestEvents.PRESSED)
        self.assertEqual([('moved', 50),'pressed'], events)

    def test_releasing_the_thumb(self):
        """ Test firing events when the thumb is released.

        """
        events = self.events
        component = self.component
        component.value = 50

        self.send_event(self.widget, TestEvents.RELEASED)
        self.assertEqual([('moved', 50)], events)

        self.send_event(self.widget, TestEvents.PRESSED)
        self.send_event(self.widget, TestEvents.RELEASED)
        self.assertEqual([('moved', 50), 'pressed', 'released'], events)

    def test_moving_the_thumb_programmaticaly(self):
        """ Test firing events when the thumb is moved (programmatically).

        """
        component = self.component
        events = self.events

        component.value = 30
        self.assertEqual(events, [('moved', 30)])
        self.assertEnamlInSync(component, 'value', 30)

    def test_move_to_home(self):
        """ Test firing events and value when the thumb is moved to home.

        """
        component = self.component
        events = self.events
        component.value = 50
        self.send_event(self.widget, TestEvents.HOME)
        self.assertEnamlInSync(component, 'value', 0)
        self.assertEqual(events, [('moved', 50), ('moved', 0)])

    def test_move_to_end(self):
        """ Test firing events and value when the thumb is moved to end.

        """
        component = self.component
        events = self.events
        self.send_event(self.widget, TestEvents.END)
        self.assertEnamlInSync(component, 'value', 100)
        self.assertEqual(events, [('moved', 100)])

    def test_move_down_by_one_step(self):
        """ Test firing events and value when the thumb is moved by one step down.

        """
        component = self.component
        events = self.events
        component.value = 50
        self.send_event(self.widget, TestEvents.STEP_DOWN)
        self.assertEnamlInSync(component, 'value', 49)
        self.assertEqual(events, [('moved', 50), ('moved', 49)])

    def test_move_up_by_one_step(self):
        """ Test firing events and value when the thumb is moved by one step up.

        """
        component = self.component
        events = self.events
        component.value = 50
        self.send_event(self.widget, TestEvents.STEP_UP)
        self.assertEnamlInSync(component, 'value', 51)
        self.assertEqual(events, [('moved', 50), ('moved', 51)])

    def test_move_down_by_one_page(self):
        """ Test firing events and value when the thumb is moved by one page down.

        """
        component = self.component
        events = self.events
        component.value = 50
        self.send_event(self.widget, TestEvents.PAGE_DOWN)
        self.assertEnamlInSync(component, 'value', 40)
        self.assertEqual(events, [('moved', 50), ('moved', 40)])

    def test_move_up_by_one_page(self):
        """ Test firing events and value when the thumb is moved by one page up.

        """
        component = self.component
        events = self.events
        component.value = 50
        self.send_event(self.widget, TestEvents.PAGE_UP)
        self.assertEnamlInSync(component, 'value', 60)
        self.assertEqual(events, [('moved', 50), ('moved', 60)])

    #--------------------------------------------------------------------------
    # absrtact methods
    #--------------------------------------------------------------------------

    @required_method
    def get_value(self, widget):
        """ Get the Slider's value.

        """
        pass

    @required_method
    def get_minimum(self, widget):
        """ Get the Slider's minimum value.

        """
        pass

    @required_method
    def get_maximum(self, widget):
        """ Get the Slider's maximum value.

        """
        pass

    @required_method
    def get_tick_interval(self, widget):
        """ Get the Slider's tick_interval value.

        """
        pass

    @required_method
    def get_tick_position(self, widget):
        """ Get the Slider's tick position style.

        """
        pass

    @required_method
    def get_orientation(self, widget):
        """ Get the Slider's orientation.

        """
        pass

    @required_method
    def get_single_step(self, widget):
        """ Get the Slider's single step value.

        """
        pass

    @required_method
    def get_page_step(self, widget):
        """ Get the Slider's page step value.

        """
        pass

    @required_method
    def get_tracking(self, widget):
        """ Get the Slider's tracking status.

        """
        pass

    @required_method
    def send_event(self, widget, event):
        """ Send an event to the Slider programmatically.

        Arguments
        ---------
        widget :
            The widget to send the event to.

        event :
            The desired event to be proccessed.

        """
        pass
