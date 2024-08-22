import abc
class Actor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'range') and 
                hasattr(subclass, 'is_active_turn') and 
                callable(subclass.is_active_turn))