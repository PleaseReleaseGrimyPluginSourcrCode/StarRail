from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Asta import Asta
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.GrandDukeIncineratedToAshes import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingyuanTingyunAstaLuocha(config):
    #%% JingYuan Tingyun Asta Luocha Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                            substats = {'CD': 11, 'CR': 7, 'SPD.flat': 7, 'ATK.percent': 3}), # get to 140 speed before buffs, to just guarantee battalia crush
                            lightcone = GeniusesRepose(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=4.9,uptime=1.0), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            benedictionTarget=JingYuanCharacter,
                            **config)

    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'ATK.percent'],
                                    substats = {'CR': 8, 'CD': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = BrokenKeel(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)

    #%% JingYuan Tingyun Asta Luocha Team Buffs
    # Penacony Buff
    for character in [JingYuanCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Asta',amount=0.1)
    for character in [JingYuanCharacter, AstaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
        
    # Asta Buffs
    # assume full uptime on asta ultimate and talent with 2 turn rotation
    for character in [JingYuanCharacter, TingyunCharacter, AstaCharacter]:
        character.addStat('SPD.flat',description='Asta Ultimate',
                        amount=53 if AstaCharacter.eidolon >= 5 else 50,
                        uptime=2.0/2.5)
        character.addStat('ATK.percent',description='Asta Talent',
                        amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                        stacks=5)
        
    # Luocha's uptime is lower because he is very fast with the multiplication light cone
    LuochaCharacter.addStat('SPD.flat',description='Asta Ultimate',
                            amount=53 if AstaCharacter.eidolon >= 5 else 50, 
                            uptime=0.75)
    LuochaCharacter.addStat('ATK.percent',description='Asta Talent',
                            amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                            stacks=5, uptime=0.75)

    # Asta Messenger Buff
    JingYuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 2.5)
    TingyunCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 2.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3)
        
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [JingYuanCharacter, AstaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    JingYuanCharacter.addStat('SPD.percent',description='Tingyun E1',amount=0.20,uptime=1.0/3.0)
    JingYuanCharacter.addStat('ATK.percent',description='Benediction',
                            amount=0.55 if TingyunCharacter.eidolon >= 5 else 0.50)
    JingYuanCharacter.addStat('DMG',description='Tingyun Ult',amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6,
                            uptime=(2.0/3.0) * (TingyunCharacter.getTotalStat('SPD') / JingYuanCharacter.getTotalStat('SPD')))

    # Tingyun and Jing Yuan are going to be out of sync so we just need to try and math out an average rotation
    print('Jing Yuan Speed: ', JingYuanCharacter.getTotalStat('SPD'), ' Tingyun Speed: ', TingyunCharacter.getTotalStat('SPD'))
    jyShortRotation = 2 / JingYuanCharacter.getTotalStat('SPD')
    jyLongRotation = 4 / JingYuanCharacter.getTotalStat('SPD')
    tyRotation = 3 / TingyunCharacter.getTotalStat('SPD')

    longToShort = (tyRotation - jyShortRotation) / jyLongRotation
    print('LongToShort Ratio', longToShort)

    # Use long to short ratio to estimate Jing Yuan Buff
    JingYuanCharacter.addStat('DMG',description='Tingyun Ult',
                            amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6,
                            uptime=1.0 - longToShort / 2)

    #%% JingYuan Tingyun Asta Luocha Print Statements
    JingYuanCharacter.print()
    TingyunCharacter.print()
    AstaCharacter.print()
    LuochaCharacter.print()

    #%% JingYuan Tingyun Asta Luocha Rotations
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
        
    lordSpeed = 0.85 # close enough of an estimate

    numSkill = 2.0 + 2.0 * longToShort
    numUlt = 1.0
    numTalents = ( 3 * numSkill * lordSpeed / JingYuanCharacter.getTotalStat('SPD') )  + 2 * numSkill + 3
    JingYuanRotation = [
        JingYuanCharacter.useSkill() * numSkill,
        JingYuanCharacter.useUltimate() * numUlt,
        JingYuanCharacter.useTalent() * numTalents,
        TingyunCharacter.useBenediction(['skill']) * numSkill,
        TingyunCharacter.useBenediction(['ultimate']),
        TingyunCharacter.giveUltEnergy(),
    ]

    AstaRotation = [AstaCharacter.useBasic() * 1.5,
                    AstaCharacter.useSkill() * 1.5,
                    AstaCharacter.useUltimate() * 1,]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% JingYuan Tingyun Asta Luocha Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    AstaRotation = [x * JingYuanRotationDuration / AstaRotationDuration for x in AstaRotation]
    LuochaRotation = [x * JingYuanRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.1f} Tingyun S{TingyunCharacter.lightcone.superposition:.1f} {TingyunCharacter.lightcone.name}, 12 spd substats', [totalTingyunEffect], TingyunCharacter, config)
    AstaEstimate = DefaultEstimator(f'Asta: 1.5N 1.5E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([JingYuanEstimate,TingyunEstimate,AstaEstimate,LuochaEstimate])