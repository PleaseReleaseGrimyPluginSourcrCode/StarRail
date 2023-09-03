from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseMV import BaseMV

class ThisIsMe(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('This Is Me!')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'preservation':
      char.percDef += 0.12 + 0.04 * self.superposition
      
      # the area of this MV should equate to the area of the ultimate
      areas = [x.area for x in char.motionValueDict['ultimate']]
      area = 'single'
      if 'all' in areas:
        area = 'all'
      elif 'single' in areas and 'adjacent' in areas:
        area = 'blast'
      elif 'blast' in areas:
        area = 'blast'

      char.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area=area, stat='def', value=0.45+0.15*self.superposition)] + char.motionValueDict['ultimate'] if 'ultimate' in char.motionValueDict else []
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  ThisIsMe(**Configuration).print()