from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ResolutionShinesAsPearlsOfSweat(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Resolution Shines As Pearls of Sweat', shortname='Resolution')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        # implement def shred in the team
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ResolutionShinesAsPearlsOfSweat(**Configuration).print()