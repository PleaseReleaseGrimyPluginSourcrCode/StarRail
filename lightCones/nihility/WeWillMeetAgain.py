from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseMV import BaseMV

class WeWillMeetAgain(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('We Will Meet Again')
        self.setSuperposition(superposition,config)
        
    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            if 'basic' in char.motionValueDict:
                char.motionValueDict['basic'] += [BaseMV(area='single', stat='atk', value=0.36+0.12*self.superposition)]
            if 'skill' in char.motionValueDict:
                char.motionValueDict['skill'] += [BaseMV(area='single', stat='atk', value=0.36+0.12*self.superposition)]
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    WeWillMeetAgain(**Configuration).print()