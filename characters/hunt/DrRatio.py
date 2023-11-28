from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class DrRatio(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                debuffStacks:float=4.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Dr Ratio')
        self.debuffStacks = debuffStacks
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.15)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=2.7, eidolonThreshold=3, eidolonBonus=0.27)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=2.4, eidolonThreshold=5, eidolonBonus=0.192)]
        self.motionValueDict['e2Stacks'] = [BaseMV(area='single', stat='atk', value=0.0, eidolonThreshold=2, eidolonBonus=0.20*min(4.0,self.debuffStacks))]

        # Talents
        self.addStat('CR',description='talent',
                     amount=0.025,
                     stacks=6.0)
        self.addStat('CD',description='talent',
                     amount=0.05,
                     stacks=6.0)

        # Eidolons
        if self.eidolon >= 4:
            self.addStat('BonusEnergyAttack',description='e4',amount=15.0,type=['talent'])
        
        # Gear
        self.equipGear()
        
    def applyTalentBuff(self, team:list, uptime:float=1.0):
        for character in team:
            character:BaseCharacter
            character.addStat('DMG',description='Dr Ratio Trace',amount=min(0.50,0.10*self.debuffStacks), uptime=uptime)
        
    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + ( (0.88 if self.eidolon >= 3 else 0.8) if self.getTempBuffDuration('Resurgence') is None else 0.0 )
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type) # too lazy to implement DrRatio e6, who cares
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['talent','followup']
        retval.damage = self.getTotalMotionValue('talent',type) + self.getTotalMotionValue('e2Stacks',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)    
        self.addDebugInfo(retval,type)    
        return retval