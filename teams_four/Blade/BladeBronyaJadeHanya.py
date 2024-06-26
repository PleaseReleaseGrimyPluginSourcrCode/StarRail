from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.harmony.Hanya import Hanya
from characters.destruction.Blade import Blade
from characters.harmony.Bronya import Bronya
from characters.erudition.Jade import Jade
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.erudition.EternalCalculus import EternalCalculus
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def BladeBronyaJadeHanya(config):
    #%% Blade Bronya Jade Hanya Characters
    
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                        substats = {'CR': 8, 'CD': 12, 'HP.percent': 5, 'SPD.flat': 3}),
                        lightcone = ASecretVow(uptime=0.0,**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = DuranDynastyOfRunningWolves(),
                        hpLossTally=0.45,
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    JadeCharacter = Jade(RelicStats(mainstats = ['CR', 'DMG.quantum', 'ATK.percent', 'ATK.percent'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = TheSeriousnessOfBreakfast(**config),
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = DuranDynastyOfRunningWolves(),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = DanceDanceDance(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [BladeCharacter, BronyaCharacter, JadeCharacter, HanyaCharacter]

    #%% Blade Bronya Jade Hanya Team Buffs
    # Broken Keel Buff
    for character in [BladeCharacter, BronyaCharacter, JadeCharacter]:
        character.addStat('CD',description='Broken Keel Hanya',amount=0.10)
    for character in [BladeCharacter, JadeCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)

    # Bronya Planetary Rendezvous
    BladeCharacter.addStat('DMG.wind',description='Planetary Rendezvous',amount=0.09 + 0.03 * BronyaCharacter.lightcone.superposition)

    # Messenger 4 pc
    for character in [BladeCharacter, JadeCharacter, HanyaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Jade Buffs, 3 turn Jade rotation
    JadeCharacter.applySkillBuff(BladeCharacter)
            
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(BladeCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(BladeCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 blade attacks
    BronyaCharacter.applyUltBuff(JadeCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / JadeCharacter.getTotalStat('SPD'))
    BronyaCharacter.applyUltBuff(HanyaCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / HanyaCharacter.getTotalStat('SPD') / 0.8) # 0.8 for multiplication

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(JadeCharacter,uptime=1.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya Jade Hanya Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 bronya turns    
    numBasic = 3.0
    numUlt = 1.0

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasic / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasic, # 3 charges
                    BladeCharacter.useUltimate() * numUlt, # 1 charge
                    BronyaCharacter.useAdvanceForward() * numBasic / 2.0, # 1 advance forward every 2 basics
                ]

    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 4 + 4 + 4) # assume 3 average threat teammates
    numTalent = (0.75 + numBasic * 2 + numUlt * 2 + numHitsTaken) / 4.0 # minus 1 on numTalent because let's assume the talent also procs jade consume
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)

    numBasicJade = 2.0
    numSkillJade = 1.0
    JadeRotation = [JadeCharacter.useBasic() * numBasicJade,
                    JadeCharacter.useSkill() * numSkillJade,
                    JadeCharacter.useUltimate(),
                    JadeCharacter.useEnhancedTalent() * 2.0]

    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    #%% Blade Bronya Jade Hanya Rotation Math
    totalBladeEffect = sumEffects(BladeRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalJadeEffect = sumEffects(JadeRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    JadeRotationDuration = totalJadeEffect.actionvalue * 100.0 / JadeCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    
    num_adjacents = min( JadeCharacter.numEnemies - 1, 2 )
    numTalentJade = 0
    numSkillDamageJade = 0
    
    # apply blade attack stacks first
    numTalentJade += (numBasic + numUlt) * (1 + num_adjacents)
    numTalentJade += numTalent * BladeCharacter.numEnemies
    numTalentJade *= JadeRotationDuration / BladeRotationDuration
    numSkillDamageJade += numTalentJade

    # apply jade's own attack stacks
    numTalentJade += numBasicJade * (1 + num_adjacents)
    numTalentJade += 1.0 * JadeCharacter.numEnemies
    numTalentJade /= 8
    JadeRotation += [JadeCharacter.useTalent() * numTalentJade]
    JadeRotation += [JadeCharacter.useSkillDamage() * numSkillDamageJade]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(deepcopy(DanceDanceDanceEffect))
    totalHanyaEffect = sumEffects(HanyaRotation)
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * BladeRotationDuration / HanyaRotationDuration
    BladeCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    BladeRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * BronyaRotationDuration / HanyaRotationDuration
    BronyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    BronyaRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * JadeRotationDuration / HanyaRotationDuration
    JadeCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JadeRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalBladeEffect = sumEffects(BladeRotation)
    totalJadeEffect = sumEffects(JadeRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    JadeRotationDuration = totalJadeEffect.actionvalue * 100.0 / JadeCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('Blade: ',BladeRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Jade: ',JadeRotationDuration)
    print('Hanya: ',HanyaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BladeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    JadeRotation = [x * BladeRotationDuration / JadeRotationDuration for x in JadeRotation]
    HanyaRotation = [x * BladeRotationDuration / HanyaRotationDuration for x in HanyaRotation]

    BladeEstimate = DefaultEstimator(f'Blade: {numBasic:.1f}N {numTalent:.1f}T {numUlt:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    JadeEstimate = DefaultEstimator(f'Jade: {numBasicJade:.1f}N {numSkillJade:.1f}E {numTalentJade:.1f}T 1Q, S{JadeCharacter.lightcone.superposition:d} {JadeCharacter.lightcone.name}', 
                                    JadeRotation, JadeCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya: 3N 1E 1Q, S{:.0f} {}'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name),
                                    HanyaRotation, HanyaCharacter, config)

    return([BladeEstimate, BronyaEstimate, JadeEstimate, HanyaEstimate])
