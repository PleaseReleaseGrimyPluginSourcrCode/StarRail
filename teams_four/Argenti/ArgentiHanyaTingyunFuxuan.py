from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.erudition.Argenti import Argenti
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def ArgentiHanyaTingyunFuxuan(config):
    #%% Argenti Hanya Tingyun Fuxuan Characters
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                        substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone =  GeniusesRepose(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=ArgentiCharacter,
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ArgentiCharacter, HanyaCharacter, TingyunCharacter, FuxuanCharacter]

    #%% Argenti Hanya Tingyun Fuxuan Team Buffs

    # Broken Keel & Penacony Buff
    for character in [ArgentiCharacter, HanyaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel Fuxuan',amount=0.10)
    for character in [ArgentiCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('DMG.physical',description='Penacony Hanya',amount=0.10)
    for character in team:
        character.addStat('DMG.physical',description='Planetary Rendezvous',amount=0.24)

    # Hanya Messenger 4 pc
    for character in [ArgentiCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger 4 pc
    for character in [ArgentiCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(ArgentiCharacter,uptime=1.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ArgentiCharacter)
    TingyunCharacter.applyUltBuff(ArgentiCharacter)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Argenti Hanya Tingyun Fuxuan Rotations
    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    # Argenti & Tingyun Rotation
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 3.0
    numSkill = (180.0 - 5.0 - 3.0 * ArgentiCharacter.numEnemies) / (30.0 + TingyunEnergyPerTurn + 3 * ArgentiCharacter.numEnemies)
    numUlt = 1

    ArgentiRotation = [ArgentiCharacter.useSkill() * numSkill,
                        ArgentiCharacter.useEnhancedUltimate() * numUlt,]

    ArgentiRotation.append(TingyunCharacter.useBenediction(['skill']) * numSkill * ArgentiCharacter.numEnemies)
    ArgentiRotation.append(TingyunCharacter.useBenediction(['ultimate','enhancedUltimate']) * numUlt * ArgentiCharacter.numEnemies)

    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
            TingyunCharacter.useUltimate(),
    ]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Argenti Hanya Tingyun Fuxuan Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    ArgentiRotation.append(TingyunCharacter.giveUltEnergy() * ArgentiRotationDuration / FuxuanRotationDuration)

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * ArgentiRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    TingyunRotation = [x * ArgentiRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    FuxuanRotation = [x * ArgentiRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    ArgentiEstimate = DefaultEstimator(f'Argenti: {numSkill:.1f}E {numUlt:.1f}EnhQ', 
                                            ArgentiRotation, ArgentiCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([ArgentiEstimate, HanyaEstimate, TingyunEstimate, FuxuanEstimate])