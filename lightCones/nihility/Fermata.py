from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class Fermata(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Fermata')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.breakEffect += 0.12 + 0.04 * self.superposition
            char.Dmg += 0.12 + 0.04 * self.superposition
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Fermata(**Configuration).print()