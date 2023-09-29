from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Jingliu(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                transmigrationPercAtk:float=1.8,
                e2Uptime:float=0.5,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Jingliu')
        self.e2Uptime = e2Uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.2)]
        
        self.motionValueDict['enhancedSkill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.5, eidolonThreshold=5, eidolonBonus=0.25),
                                                BaseMV(type='skill',area='adjacent', stat='atk', value=1.25, eidolonThreshold=5, eidolonBonus=0.125)]
        
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.0, eidolonThreshold=3, eidolonBonus=0.24),
                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.12)]
        
        # Talents
        self.transmigrationPercAtk = min(1.98 if self.eidolon >= 3 else 1.8,transmigrationPercAtk) + (0.3 if self.eidolon >= 4 else 0.0)
        self.addStat('ATK',description='talent',type='transmigration',amount=self.transmigrationPercAtk)
        self.addStat('CR',description='talent',type='transmigration',amount=0.5)
        self.addStat('DMG',description='trace',type='ultimate',amount=0.2)
        self.addStat('AdvanceForward',description='trace',type='skill',amount=0.1)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CD',description='e1',type='transmigration',amount=0.24)
        if self.eidolon >= 2:
            self.addStat('DMG',description='e2',type='enhancedSkill',amount=0.8,uptime=self.e2Uptime)
        if self.eidolon >= 6:
            self.addStat('CD',description='e6',type='transmigration',amount=0.50)

        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
        retval.damage = self.getTotalMotionValue('basic')
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
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval
    
    def extraTurn(self):
        retval = BaseEffect()
        retval.actionvalue = -1.0
        return retval        

    def useEnhancedSkill(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['skill','enhancedSkill','transmigration']
        retval.damage = self.getTotalMotionValue('enhancedSkill')
        if self.eidolon >=1 and self.numEnemies == 1:
            retval.damage *= 1.5
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        blastEnemies = min(3,self.numEnemies)
        retval = BaseEffect()
        type = ['ultimate','transmigration']
        retval.damage = self.getTotalMotionValue('ultimate')
        if self.eidolon >=1 and self.numEnemies == 1:
            retval.damage *= 1.5
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * blastEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        return retval