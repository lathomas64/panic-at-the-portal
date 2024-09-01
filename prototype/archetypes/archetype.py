import abc
class Archetype:
    def __init__(self, character):
        self.on_add(character)
        self.actor = character
    
    @abc.abstractmethod
    def on_add(self, character):
        raise NotImplementedError("Need to specify what the archetype does on add")