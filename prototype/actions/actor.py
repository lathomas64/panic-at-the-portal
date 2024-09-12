'''
interface for Actor
'''
import abc
class Actor(metaclass=abc.ABCMeta):
    '''
    class defining the actor interface
    it should have a range attribute, and a is_active_turn method
    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'range') and
                hasattr(subclass, 'is_active_turn') and
                callable(subclass.is_active_turn))
