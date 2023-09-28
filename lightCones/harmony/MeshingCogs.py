from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class MeshingCogs(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Meshing Cogs')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.bonusEnergyAttack['basic'] += 3.0 + 1.0 * self.superposition
            char.bonusEnergyAttack['skill'] += 3.0 + 1.0 * self.superposition
            char.bonusEnergyAttack['ultimate'] += 3.0 + 1.0 * self.superposition
            char.bonusEnergyAttack['talent'] += 3.0 + 1.0 * self.superposition
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MeshingCogs(**Configuration).print()