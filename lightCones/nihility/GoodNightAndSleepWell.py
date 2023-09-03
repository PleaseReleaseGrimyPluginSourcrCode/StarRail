from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class GoodNightAndSleepWell(BaseLightCone):
  def __init__(self,
               stacks:float=3.0,
               **config):
    self.loadConeStats('Good Night and Sleep Well')
    self.setSuperposition(config)
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.Dmg += ( 0.09 + 0.03 * self.superposition ) * self.stacks
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  GoodNightAndSleepWell(**Configuration).print()