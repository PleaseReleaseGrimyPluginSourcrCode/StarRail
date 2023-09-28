import os
from copy import copy
import pandas as pd
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BuffEffect import BuffEffect

EMPTY_STATS = {  # character stats
                'ATK':[], 'DEF':[], 'HP':[],
                'DMG':[], 'CR':[], 'CD':[],
                # defensive stats
                'DmgReduction':[], 'AllRes':[],
                'Shield':[], 'Heal':[],
                'Taunt':[],
                # offensive stats
                'Vulnerability':[],
                'DefShred':[],
                'ResPen':[],
                # energy stats
                'ER':[], 'BonusEnergyAttack':[],
                # action stats
                'SPD':[], 'AdvanceForward':[],
                # effect stats
                'EHR':[], 'BreakEffect':[], 'BreakEfficiency':[],
                }

STATS_FILEPATH = 'settings\CharacterStats.csv'
if os.name == 'posix':
    STATS_FILEPATH = STATS_FILEPATH.replace('\\','/')

class BaseCharacter(object):
    stats:dict
    tempStats:dict

    graphic:str
    initialEnergy:float
    maxEnergy:float
    path:str
    element:str
    name:str

    # define information we would pull from the configuration dictionary and might use
    # helps with autocomplete in vs code
    numEnemies:int
    numRounds:float
    enemyLevel:int
    enemySpeed:float
    enemyType:str    
    bonusEnergyFlat:float
    bonusEnergyPerEnemyAttack:float
    numberEnemyAttacksPerTurn:float
    enemyMaxHP:float
    enemyToughness:float
    breakLevelMultiplier:float
    enemyRes:float
    weaknessBrokenUptime:float

    def __init__(self, relicstats, lightcone=None, relicsetone=None, relicsettwo=None, planarset=None, **config):
        self.__dict__.update(config)
        self.stats = copy(EMPTY_STATS)
        self.tempStats = copy(EMPTY_STATS)
        
        self.lightcone = lightcone
        self.relicsetone = relicsetone
        self.relicsettwo = relicsettwo
        self.planarset = planarset
        self.relicstats = relicstats
        
        self.motionValueDict = {}
        
    def loadCharacterStats(self, name:str):
        df = pd.read_csv(STATS_FILEPATH)
        rows = df.iloc[:, 0]
        for column in df.columns:
            split_column = column.split('.')
            data = df.loc[rows[rows == name].index,column].values[0]
            if len(split_column) > 1:
                column_key, column_type = split_column[0], split_column[1]
                if column_type in ['base','percent','flat']:
                    effect = BuffEffect(column_key,'Character Stats',data,mathType=column_type)
                else:
                    effect = BuffEffect(column_key,'Character Stats',data,type=column_type)
                self.stats[column_key].append(effect)
            else:
                self.__dict__[column] = data
                
        self.initialEnergy = self.maxEnergy * 0.5
        self.eidolon = self.fourstarEidolons if self.rarity == 4 else self.fivestarEidolons
        
        self.longName = '{} E{} {} S{}\n{}{}{}'.format(self.name, self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                        "" if self.relicsetone is None else self.relicsetone.shortname, 
                                                        "" if self.relicsettwo is None else (" + " + self.relicsettwo.shortname), 
                                                        "" if self.planarset is None else (" + " + self.planarset.shortname))

    def addStat(self, name:str, description:str, amount:float, type:str=None, stacks:float=1.0, uptime:float=1.0, mathType:str='base'):
        self.stats[name].append(name=name, description=description, amount=amount, type=type, stacks=stacks, uptime=uptime, mathType=mathType)

    def equipGear(self):
        if self.relicstats is not None: self.relicstats.equipTo(self)
        if self.lightcone is not None: self.lightcone.equipTo(self)
        if self.relicsetone is not None: self.relicsetone.equipTo(self)
        if self.relicsettwo is not None: self.relicsettwo.equipTo(self)
        if self.planarset is not None: self.planarset.equipTo(self)
    
    def getTotalStat(self, stat:str, type:[str,list]=None):
        typeTotal = {'base': 0.0,
                     'percent':0.0,
                     'flat':0.0,}
        for entry in self.stats[stat]:
            entry:BuffEffect
            if type is None or (isinstance(type,str) and entry.type == type) or (isinstance(type,list) and entry.type in type):
                typeTotal[entry.mathType] += entry.amount * entry.stacks * entry.uptime
            
        return typeTotal['base'] * (1.0 + typeTotal['percent']) + typeTotal['flat']
    
    def getTotalCrit(self, type=None):
        if isinstance(type, list):
            crBonuses = sum([(self.CRType[x] if x in self.CRType else 0.0) for x in type])
            cdBonuses = sum([(self.CDType[x] if x in self.CDType else 0.0) for x in type])
            return 1.0 + min(1.0, self.CR + crBonuses) * (self.CD + cdBonuses)
        elif type is None:
            return 1.0 + min(1.0, self.CR) * self.CD
        else:
            return 1.0 + min(1.0, self.CR + self.CRType[type]) * (self.CD + self.CDType[type])
    
    def getTotalMotionValue(self, type:str):
        total = 0.0
        for key, value in self.motionValueDict.items():
            if key == type:
                if isinstance(value, list):
                    total += sum(x.calculate(self) for x in value)
                else:
                    total += value.calculate(self)
        return total

    def useBasic(self):
        retval = BaseEffect()
        retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
        retval.energy = 20.0 * (1.0 + self.ER)
        retval.skillpoints = 1.0
        return retval

    def useSkill(self):
        retval = BaseEffect()
        retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
        retval.energy = 30.0 * (1.0 + self.ER)
        retval.skillpoints = -1.0
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        retval.energy = 5.0 * (1.0 + self.ER)
        return retval

    def useTalent(self):
        return BaseEffect()

    def useEnhancedBasic(self):
        return BaseEffect()

    def useDot(self):
        return BaseEffect()

    def useBreak(self):
        retval = BaseEffect()

        breakMultipliers = {
            'physical': 2.0,
            'fire': 2.0,
            'ice': 1.0,
            'lightning': 1.0,
            'wind': 1.5,
            'quantum': 0.5,
            'imaginary': 0.5,
        }

        baseDotDamage = self.breakLevelMultiplier
        baseDotDamage *= 0.5 + self.enemyToughness / 120
        baseDotDamage *= breakMultipliers[self.element]
        baseDotDamage *= 1.0 + self.breakEffect
        baseDotDamage *= self.getVulnerabilityType()
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

        retval.damage = baseDotDamage
        return retval

    def useBreakDot(self):
        retval = BaseEffect()
        baseDotDamage = 0.0

        if self.element == 'physical':
            baseDotDamage = 2.0 *self.breakLevelMultiplier
            baseDotDamage *= 0.5 + self.enemyToughness / 120
            if self.enemyType == 'elite':
                bleedDamage = 0.07 * self.enemyMaxHP
            else:
                bleedDamage = 0.16 * self.enemyMaxHP
            baseDotDamage = min(baseDotDamage, bleedDamage)
        elif self.element == 'fire':
            baseDotDamage = self.breakLevelMultiplier
        elif self.element == 'ice':
            baseDotDamage = self.breakLevelMultiplier
        elif self.element == 'lightning':
            baseDotDamage = 2.0 * self.breakLevelMultiplier
        elif self.element == 'wind': #assume 3 stacks to elites, 1 stack otherwise
            baseDotDamage = (3.0 if self.enemyType == 'elite' else 1.0) * self.breakLevelMultiplier
        elif self.element == 'quantum': #assume 3 stacks
            baseDotDamage = 0.6 * 3 * self.breakLevelMultiplier
            baseDotDamage *= 0.5 + self.enemyToughness / 120

        baseDotDamage *= 1.0 + self.breakEffect
        baseDotDamage *= self.getVulnerabilityType('dot')
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

        retval.damage = baseDotDamage
        return retval

    def applyDamageMultipliers(self, baseDamage:float) -> float:
        damage = baseDamage
        damage *= (80 + 20 ) / ( ( self.enemyLevel + 20 ) * ( 1 - self.defShred ) + 80 + 20 )
        damage *= max(min(1 - self.enemyRes + self.resPen, 2.0), 0.1)
        damage *= 0.9 + 0.1 * self.weaknessBrokenUptime
        return damage
