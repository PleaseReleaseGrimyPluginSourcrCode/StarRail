from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Herta(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                hpThresholdUptime:float=0.5,
                frozenUptime:float=0.5,
                e2Stacks:float=5.0,
                e4Stacks:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Herta')
        self.hpThresholdUptime = hpThresholdUptime
        self.frozenUptime = frozenUptime
        self.e2Stacks = e2Stacks
        self.e4Stacks = e4Stacks
        self.ultBuff = False
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['basicE1'] = [BaseMV(type='basic',area='single', stat='atk', value=0.4)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='all', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.16)]
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=0.40, eidolonThreshold=5, eidolonBonus=0.03)]
        
        # Talents
        self.DmgType['ultimate'] += 0.20 * self.frozenUptime
        self.DmgType['skill'] += 0.45 * self.hpThresholdUptime
        self.DmgType['talent'] += 0.10 * self.e4Stacks
        self.CR += 0.03 * self.e2Stacks
        
        # Eidolons
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
        retval.damage = self.getTotalMotionValue('basic') + ( self.getTotalMotionValue('basicE1') if self.eidolon >= 1 else 0.0 )
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = 'skill'
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 * self.numEnemies ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = 'ultimate'
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        
        if not self.ultBuff:
            self.ultBuff = True
            self.percAtk += 0.25 if self.eidolon >= 6 else 0.0
        return retval

    def useTalent(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(['talent','followup'])
        retval.damage *= self.getTotalDmg(['talent','followup'])
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.getBreakEfficiency(type)
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = 0.0 - min(1.0,self.getTotalStat('AdvanceForward','talent'))
        return retval

    def endTurn(self):
        retval = BaseEffect()
        
        if self.ultBuff:
            self.ultBuff = False
            self.percAtk -= 0.25 if self.eidolon >= 6 else 0.0
        return retval