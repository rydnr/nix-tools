from domain.event import Event

class EventEmitter:

    _receivers = []

    @classmethod
    def receivers(cls):
        return EventEmitter._receivers

    @classmethod
    def register_receiver(cls, receiver):
        if receiver not in EventEmitter._receivers:
            EventEmitter._receivers.append(receiver)

    @classmethod
    def emit(cls, event: Event):
        """
        Emits given event.
        """
        for receiver in EventEmitter._receivers:
            receiver.accept_event(event)
