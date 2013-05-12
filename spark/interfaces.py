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
        """

    def set_presentation_agent(presentation_agent):
        """
        Sets presentation agent instance
        """

    def get_presentation_agent():
        """
        Sets presentation agent instance
        """

    def set_abstraction_agent(presentation_agent):
        """
        Sets abstraction agent instance
        """

    def get_abstraction_agent():
        """
        Sets abstraction agent instance
        """

    def get_value(name):
        """
        Returns attribute value identified by name
        """

    def set_value(name, value):
        """
        Sets attribute value identified by name
        """

    def destroy():
        """
        Cleanly destroyes all components
        """
