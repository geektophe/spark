#!/usr/bin/env python
"""
Event bus related classes.

An event bus dispatches events to subscribers. Each subscriber is called a
callback function which is passed the event that is dispatched.

Subscribers subscribe to event types, as for exceptions.

A bus may dispatch several events of different types. A subscriber that
subsrcibed to an event type will be notified only if that particular event
type is dispatched.

An event bus may also be connected to an other event bus (as subscriber), and
dispatch events from connected bus to its own subscribers.

Any subscribed client may also be unsubscribed.

Note that it is not possible to tell in which order subscribers will be called
in a bus when an event is dispatched. A code using an EventBus should never
rely on execution order in the bus.
"""

from spark.interfaces import IEvent
from zope.interface import implements


class BaseEvent(object):
    """
    Base event class.

    Event classes may represent various event types (user interaction, system,
    ui, and so on) and have to be published in an event bus.

    Subscribers on this bus will be called a callback which argument is the
    event object.

    Specialized event classes have to subclass this base class to be published
    on the bus.

    An event is represented by its type (class), its source (mandatory
    parameter), and may be specified optional parameters in the contructor
    that are mapped into instance variables.

    For enstance :

    >>> event = BaseEvent(__name__, parm1=1, parm2=2)
    >>> event.source == __name__
    True
    >>> event.parm1
    1
    >>> event.parm2
    2
    """

    implements(IEvent)

    def __init__(self, source, **kwargs):
        """
        Object initialization.

        @param source       The instance that generated the event.
        @param kwargs       A ditctionnary containing optional parameters to be
                            mapped as instance variables.
        """
        self.source = source

        for key, value in kwargs.items():
            setattr(self, key, value)


class BusError(Exception):
    """
    Error risen when an error occured in a bus routine.
    """


class EventBus(object):
    """
    Standard (local) event bus.

    A bus is empty at initialization

    Let's declare a test subscriber class

    >>> class TestSubscriber(object):
    ...     notified = 0
    ...     def notify(self, event):
    ...         self.notified += 1
    ...     def clear(self):
    ...         self.notified = 0

    And two test event classes

    >>> from sitebuilder.event.events import BaseEvent

    >>> class TestEvent1(BaseEvent):
    ...     implements(IEvent)

    >>> class TestEvent2(BaseEvent):
    ...     implements(IEvent)

    Let's instantiate a bus

    >>> bus = EventBus()

    And a subscriber

    >>> subscr = TestSubscriber()
    >>> subscr.notified
    0

    Let's subscribe the subscriber to the bus for TestEvent2 events

    >>> bus.subscribe(TestEvent2, subscr.notify)

    If we dispatch a TestEvent1 event, subscriber should not have been
    notified.

    >>> bus.publish( TestEvent1(__name__) )
    >>> subscr.notified
    0

    If we dispatch a TestEvent2 event, it have been notified

    >>> bus.publish( TestEvent2(__name__) )
    >>> subscr.notified
    1

    If we subsrcibe the subscriber to both events, it should be notified both.

    >>> bus.subscribe(TestEvent1, subscr.notify)
    >>> subscr.clear()
    >>> bus.publish( TestEvent1(__name__) )
    >>> bus.publish( TestEvent2(__name__) )
    >>> subscr.notified
    2

    If we unsubscribe to subsrcriber from TestEvent2, it should be notified
    only once.

    >>> bus.unsubscribe(TestEvent2, subscr.notify)
    >>> subscr.clear()
    >>> bus.publish( TestEvent1(__name__) )
    >>> bus.publish( TestEvent2(__name__) )
    >>> subscr.notified
    1

    If we clear all subscribers, no the subscriber should not be notified
    anymore.

    >>> bus.unsubscribe_all()
    >>> subscr.clear()
    >>> bus.publish( TestEvent1(__name__) )
    >>> bus.publish( TestEvent2(__name__) )
    >>> subscr.notified
    0

    Let's create a second subscriber, and a second bus

    >>> bus2 = EventBus()
    >>> subscr2 = TestSubscriber()

    And let's connect bus2 to bus

    >>> bus.connect(bus2)

    Let's subscribe subscr2 to bus2

    >>> bus2.subscribe(TestEvent1, subscr2.notify)

    If we dispatch a TestEvent1 on bus, it should be redispatched on bus2, and
    subscr2 should be notified.

    >>> bus.publish( TestEvent1(__name__) )
    >>> subscr2.notified
    1

    If we disconnect bus2 from bus, evenst should not be redispatched anymore.

    >>> bus.disconnect(bus2)
    >>> subscr2.clear()
    >>> bus.publish( TestEvent1(__name__) )
    >>> subscr2.notified
    0
    """

    def __init__(self):
        """
        Bus initialization.
        """
        self.subscribers = {}
        self.followers = []

    def subscribe(self, klass, callback):
        """
        Subscribe a callable to an event type (class).

        An already subscribed callback is ignored.

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        if not IEvent.implementedBy(klass):
            raise BusError('Invalid subscription, klass should implenent IEvent')

        if klass not in self.subscribers:
            self.subscribers[klass] = []

        if not callback in self.subscribers[klass]:
            self.subscribers[klass].append(callback)

    def unsubscribe(self, klass, callback):
        """
        Unsubscribe a callable from an event type (class).

        An already subscribed callback is ignored.

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        if not IEvent.implementedBy(klass):
            raise BusError('Invalid unsubscription, klass should implenent IEvent')

        if klass in self.subscribers:
            # Removes subscriber callback
            if callback in self.subscribers[klass]:
                self.subscribers[klass].remove(callback)

            # Cleans subscriber disctionnary
            if not len(self.subscribers[klass]):
                del self.subscribers[klass]

    def unsubscribe_all(self):
        """
        Unsubscribes all subscribers
        """
        del self.subscribers
        self.subscribers = {}

    def has_subscribed(self, klass, callback):
        """
        Tells if a callback has already subscribed to a scpecific event type
        (class).

        @param klass    The event type to subscribe to
        @param callback The callable object to pass event when an event is
                        dispatched.
        """
        return klass in self.subscribers and callback in self.subscribers[klass]

    def connect(self, bus):
        """
        Connects an external bus. All dispatched events are re-dispatched on
        connected buses.
        """
        self.followers.append(bus)

    def disconnect(self, bus):
        """
        Disconnects an external bus. No furter events will follow.
        """
        self.followers.remove(bus)

    def is_connected(self, bus):
        """
        Tells if an external bus is connected.
        """
        return bus in self.followers

    def disconnect_all(self):
        """
        Disconnects all followers.
        """
        del self.followers
        self.followers = []

    def clear(self):
        """
        Totally clears a bus.
        """
        self.unsubscribe_all()
        self.disconnect_all()

    def publish(self, event):
        """
        Publishes an event to subscribers.
        """
        if not IEvent.providedBy(event):
            raise BusError('Invalid dispatching, event should provide IEvent')

        # Dispatches event to subscribers
        if type(event) in self.subscribers:
            for subscriber in self.subscribers[type(event)]:
                subscriber(event)

        # Publishes event on connected buses
        for follower in self.followers:
            follower.publish(event)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
