from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class FlowingNightglow(BaseLightCone):
    def __init__(self,
                 stacks=4.0,
                 uptime=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Flowing Nightglow')
        self.setSuperposition(superposition,config)
        self.stacks = stacks
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ER',description=self.name,amount=0.36 + 0.12 * self.superposition, stacks=self.stacks)
            char.addStat('ATK.percent',description=self.name,amount=0.2 + 0.04 * self.superposition, uptime=self.uptime)
            
            def applyTeamBuff(team):
                for targetChar in team:
                    targetChar.addStat('DMG',description=f'{self.shortname} from {char.name}',
                                       amount=0.2 + 0.04 * self.superposition, 
                                       uptime=self.uptime)

                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    FlowingNightglow(**Configuration).print()