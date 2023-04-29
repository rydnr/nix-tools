from domain.event import Event

from typing import List,Type

class EventListener:

    _listeners = {}

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes
        """
        raise NotImplementedError(
            "supported_events() must be implemented by subclasses"
        )

    @classmethod
    def listeners(cls):
        return EventListener._listeners

    @classmethod
    def listeners_for(cls, eventClass: Type[Event]) -> List[Type]:
        return EventListener._listeners.get(eventClass, [])

    @classmethod
    def listen(cls, listener: Type, eventClass: Type[Event]):
        eventListeners = EventListener.listeners_for(eventClass)
        eventListeners.append(listener)

    def accept(self, event: Event):
        EventListener.listeners_for(event.__class__)
        if len(_listeners) == 0:
            raise UnsupportedEvent(event)
        for listener in _listeners:
            methodName = f'listen{event.__class__}'
            method = getattr(self, methodName)
            method(event)
