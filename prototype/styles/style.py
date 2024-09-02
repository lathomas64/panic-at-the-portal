import abc
class Style:
    def __init__(self, character):
        self.actor = character
    
    @abc.abstractmethod
    def on_equip(self): #when we switch to a stance using this style
        raise NotImplementedError("Need to specify what the style does on equip") 
    
    @abc.abstractmethod
    def on_unequip(self): #when we leave this stance
        raise NotImplementedError("Need to specify what the style does on unequip")