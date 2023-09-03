from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MomentOfVictory(BaseLightCone):
  def __init__(self,
               uptime:float=1.0,
               **config):
    self.loadConeStats('Moment of Victory')
    self.setSuperposition(config)
    self.uptime=uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'preservation':
      char.percTaunt += 2.0
      char.percDef += 0.2 + 0.04 * self.superposition
      char.percDef += ( 0.2 + 0.04 * self.superposition ) * self.uptime
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  MomentOfVictory(**Configuration).print()