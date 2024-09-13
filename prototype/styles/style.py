'''
generic style module other styles should inherit this
'''
import abc
class Style:
    '''
    class representing a generic style basically an interface
    '''
    def __init__(self, character):
        self.actor = character

    @abc.abstractmethod
    def on_equip(self):
        '''
        when we switch to a stance using this style
        do these things
        '''
        raise NotImplementedError("Need to specify what the style does on equip")

    @abc.abstractmethod
    def on_unequip(self):
        '''
        when we leave a stance using this style
        cleanup here
        '''
        raise NotImplementedError("Need to specify what the style does on unequip")
