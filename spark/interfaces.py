#!/usr/bin/env python
"""
Spark interfaces definition.
"""

from zope.interface import Interface, Attribute


class IEvent(Interface):
    """
    Represents data, user or system events.

    Events may represent various event types (user interaction, system, ui,
    and so on) and have to be published in an event bus.

    Subscribers on this bus will be called a callback which argument is the
    event object.

    Specialized event classes have to implement the IEvent interface to be
    published on the bus.

    Events have a source (the object that published the event), and may
    present an arbutrary number oh additional attributes.
    """

    source = Attribute(u'The instance that emitted the event')


class IEventBroker(Interface):
    """
    A class that publishes events through an event bus.
    """

    def get_event_bus():
        """
        Returns an event bus on which IEvents are published.
        """


class IPresentationAgent(IEventBroker):
    """
    A class representing an application abstraction.
    """


class IControlAgent(Interface):
    """
    Control Agent interface
    """

    def is_readonly():
        """
        Returns component's read only state flag
        """

    def set_readonly(flag):
        """
        Sets component's read only state flag

        @param flag:    The flag representing the read-only state (may be True
                        or False)
        """

    def set_presentation_agent(agent):
        """
        Sets presentation agent instance

        @param agent:   The presentation agent instance to bind.
        """

    def get_presentation_agent():
        """
        Sets presentation agent instance
        """

    def set_abstraction_agent(agent):
        """
        Sets abstraction agent instance

        @param agent:   The presentation agent instance to bind.
        """

    def get_abstraction_agent():
        """
        Sets abstraction agent instance
        """

    def get_value(name):
        """
        Returns attribute value identified by name

        @param name:    The name identifying the attribute to get value from.
        """

    def set_value(name, value):
        """
        Sets attribute value identified by name

        @param name:    The name identifying the attribute to set value to.
        @param value:   The value to set.
        """

    def destroy():
        """
        Cleanly destroyes all components
        """


class IPresentationAgent(IEventBroker):
    """
    Presentation agent interface definition
    """

    def get_control_agent():
        """
        Returns control agent instance.
        """

    def get_toplevel():
        """
        Returns toplevel component
        """

    def attach_slave(name, container_name, slave):
        """
        Attach a sub (slave) presentation agent view.

        @param name:            The slave name
        @param container_name:  The contianer widget name to pack slave into.
        @param slave:           The slave presentation instance to attach.
        """

    def enable(name):
        """
        Enables a widget (set it resopnsive to user actions).

        @param name:    The name identifying the widget to enable.
        """

    def disable(name):
        """
        Disables a widget (set it inresopnsive to user actions).

        @param name:    The name identifying the widget to disable.
        """

    def get_value(name):
        """
        Reads a widget value or state.

        @param name:    The name identifying the widget to read value from.
        """

    def set_value(name, value):
        """
        Sets a control value or state.

        @param name:    The name identifying the widget to set value to.
        """

    def set_isems(name, items):
        """
        Sets a list of available (selectable) items on list widgets.

        @param name:    The name identifying the widget to set value to.
        @param items:   A list containing the values to set.
        """

    def set_error(name, state, mesg=""):
        """
        Sets a widget in a state showing than an incorrect value has been set,
        or set it back in normal state.

        @param name:    The name identifying the widget to set error state.
        @param state:   The error state to set (may be True or False)
        @param mesg:    The error message to set in case of error.
        """

    def show():
        """
        Shows the top level window.
        """

    def hide():
        """
        Shows the top level window.
        """

    def destroy():
        """
        Cleanly destroyes component.
        """
