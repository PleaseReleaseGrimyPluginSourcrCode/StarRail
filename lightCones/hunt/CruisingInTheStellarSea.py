from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class CruisingInTheStellarSea(BaseLightCone):
  def __init__(self,
               uptimeHP:float = 0.5,
               uptimeDefeat:float = 1.0,
               **config):
    self.loadConeStats('Cruising in the Stellar Sea')
    self.setSuperposition(config)
    self.uptimeHP = uptimeHP
    self.uptimeDefeat = uptimeDefeat

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'hunt':
      char.CR += 0.06 + 0.02 * self.superposition
      char.CR += (0.06 + 0.02 * self.superposition) * self.uptimeHP
      char.percAtk += (0.15 + 0.05 * self.superposition) * self.uptimeDefeat
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  CruisingInTheStellarSea(**Configuration).print()