'''
module for handling forms
'''
import abc
class Form():
    '''
    class representing an individual form
    '''
    def __init__(self, character):
        self.actor = character

    @abc.abstractmethod
    def on_equip(self):
        '''
        when we switch to a stance using this style do these things
        '''
        raise NotImplementedError("Need to specify what the style does on equip")

    @abc.abstractmethod
    def on_unequip(self):
        '''
        cleanup for when we leave the stance including this style
        '''
        raise NotImplementedError("Need to specify what the style does on unequip")
