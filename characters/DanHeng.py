from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from lightCones.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.SpaceSealingStation import SpaceSealingStation

class DanHeng(BaseCharacter):
  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               graphic:str = 'https://static.wikia.nocookie.net/houkai-star-rail/images/1/1a/Character_Dan_Heng_Icon.png',
               talentUptime:float = 0.25,
               slowUptime:float = 1.0,
               fasterThanLightUptime:float = 1.0,
               e1Uptime:float = 0.5,
               **config):
    super().__init__()
    self.lightcone = lightcone
    self.relicsetone = relicsetone
    self.relicsettwo = relicsettwo
    self.planarset = planarset
    self.relicstats = relicstats
    
    self.talentUptime = talentUptime
    self.slowUptime = slowUptime
    self.e1Uptime = e1Uptime
    self.fasterThanLightUptime = fasterThanLightUptime

    self.name = 'Dan Heng E{} {} S{}\n{} + {} + {}\nTalent Uptime: {}\nSlow Uptime: {}\n20% Spd Uptime: {}'.format(self.eidolon, self.lightcone.shortname, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,
                                                                                          self.talentUptime,
                                                                                          self.slowUptime,
                                                                                          self.fasterThanLightUptime)
    self.graphic = graphic
    self.config = config
    self.eidolon = config['fourstarEidolons']

    self.element = 'wind'

    # Base Stats

    self.baseAtk = 546.84
    self.baseDef = 396.90
    self.baseHP = 882.00
    self.baseSpd = 110
    self.maxEnergy = 100

    # Talents

    self.percAtk += 0.04 + 0.06 + 0.08 # Ascensions
    self.windDmg += 0.032 + 0.048 + 0.064 + 0.032 + 0.048# Ascensions
    self.percDef += 0.075 + 0.05# Ascensions
    self.percSpd += 0.20 * self.fasterThanLightUptime # Faster Than Light
    self.basicDmg += 0.40 * self.slowUptime # High Gale

    self.ultDmg += (1.296 if self.eidolon >= 5 else 1.2) * self.slowUptime # Ultimate

    self.CR += 0.12 * self.e1Uptime # The Higher You Fly, the Harder You Fall

    self.resPen += ( 0.396 if self.eidolon >= 5 else 0.36 ) * talentUptime

    self.equipGear()
    self.balanceCrit()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEff)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 2.86 if self.eidolon >= 3 else 2.6
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.skillDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.BreakEff)
    retval.energy = 30.0 * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 4.32 if self.eidolon >= 5 else 4.0
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.BreakEff)
    retval.energy = 5.0 * (1.0 + self.ER)
    retval.skillpoints = 0.0
    return retval
  
def DanHengRotation(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):
    playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
    enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100

    #I'm just gonna ballpark 4 procs of EagleOfTwilightLine 4 pc here
    playerTurns += 0.25 * 4

    totalEffect = BaseEffect()
    # assume we spam skill every single turn
    totalEffect += playerTurns * character.useSkill()
    # assume we apply break a number of times proportional to our gauge output and enemy toughness
    num_breaks = totalEffect.gauge / Configuration['enemyToughness']
    totalEffect += character.useBreak() * num_breaks
    # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
    num_dots = min(enemyTurns * Configuration['numEnemies'], num_breaks * 2)
    totalEffect += character.useBreakDot() * num_dots
    # assume we use an ult proportional to the amount of energy we gained. Ignoring rounding errors and energy from enemy attacks
    num_ults = ( totalEffect.energy - 5 * (1 + character.ER) ) / character.maxEnergy
    totalEffect += character.useUltimate() * num_ults
    print("Dan Heng Effects:")
    totalEffect.print()

    CharacterDict[character.name] = copy(character)
    EffectDict[character.name] = copy(totalEffect)