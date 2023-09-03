from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class RiverFlowsInSpring(BaseLightCone):
  def __init__(self, 
               uptime:float = 1.0,
               **config):
    self.loadConeStats('River Flows in Spring')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'hunt':
      char.percSpd += ( 0.07 + 0.01 * self.superposition ) * self.uptime
      char.Dmg += ( 0.09 + 0.03 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  RiverFlowsInSpring(**Configuration).print()