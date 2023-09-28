from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class NightOnTheMilkyWay(BaseLightCone):
    def __init__(self,
                uptime:float=0.25,
                **config):
        self.loadConeStats('Night on the Milky Way')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.percAtk += ( 0.075 + 0.0015 * self.superposition ) * char.numEnemies
            char.Dmg += ( 0.25 + 0.05 * self.superposition ) * self.uptime
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    NightOnTheMilkyWay(**Configuration).print()