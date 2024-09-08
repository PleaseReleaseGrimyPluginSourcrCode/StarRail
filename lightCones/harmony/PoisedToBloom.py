from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PoisedToBloom(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Poised to Bloom', shortname='Poised')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,amount=0.12 + 0.04 * self.superposition)
            
            def applyTeamBuff(team):
                for targetChar in team:
                    numPath = len([targetChar.path for ally in team if targetChar.path == ally.path])
                    if numPath >= 2:
                        targetChar.addStat('CD',
                                    description=f'{self.shortname} from {char.name}',
                                    amount=0.12 + 0.04 * self.superposition,)
                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PoisedToBloom(**Configuration).print()