from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class GeniusesRepose(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Geniuses\' Repose')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.12 + 0.04 * self.superposition)
            char.addStat('CD',description=self.name,
                                    amount=0.18 + 0.06 * self. superposition,
                                    uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    GeniusesRepose(**Configuration).print()