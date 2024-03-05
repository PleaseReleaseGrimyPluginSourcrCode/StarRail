from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.destruction.Xueyi import Xueyi
from characters.harmony.Hanabi import Hanabi
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def XueyiHanabiPelaFuxuan(config, breakRatio:float=0.5):
    #%% Xueyi Hanabi Pela Fuxuan Characters
    XueyiCharacter = Xueyi(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'BreakEffect'],
                            substats = {'CR': 12, 'CD': 8, 'BreakEffect': 5, 'ATK.percent': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime=1.0,**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = InertSalsotto(),
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = PlanetaryRendezvous(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [XueyiCharacter, HanabiCharacter, PelaCharacter, FuxuanCharacter]

    #%% Xueyi Hanabi Pela Fuxuan Team Buffs
    # Broken Keel Buffs
    for character in [XueyiCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)
    for character in [XueyiCharacter, HanabiCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
    for character in [XueyiCharacter, HanabiCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
        
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=XueyiCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    
    # Planetary Rendezvous
    for character in team:
        character.addStat('DMG.quantum',description='Planetary Rendezvous',amount=0.24)
        
    # Hanabi Messenger 4 pc
    for character in [XueyiCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Pela Debuffs, 2 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in team:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Xueyi Hanabi Pela Fuxuan Rotations
    numSkillXueyi = 3.0
    numUltXueyi = 1.0
    numBlast = min(3,XueyiCharacter.numEnemies)
    numAllyAttacks = numSkillXueyi * 4.0 / 3.0 # 2 ish hits from Pela, 2 ish hits from fu xuan
    numTalentXueyi = numSkillXueyi * (1 + numBlast) + 4 * numUltXueyi + numAllyAttacks
    numTalentXueyi *= 3.0 / (6.0 if XueyiCharacter.eidolon >= 6 else 8.0)
    numTalentXueyi *= breakRatio # balance this with the weakness broken uptime
    XueyiRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                XueyiCharacter.useSkill() * numSkillXueyi,
                XueyiCharacter.useUltimate() * numUltXueyi,
                XueyiCharacter.useTalent() * numTalentXueyi,
                HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - XueyiCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkillXueyi,
    ]
    
    PelaRotation = [ 
        PelaCharacter.useBasic() * 1,
        PelaCharacter.useSkill() * 1, 
        PelaCharacter.useUltimate(),
    ]
    
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Xueyi Hanabi Pela Fuxuan Rotation Math
    totalXueyiEffect = sumEffects(XueyiRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    XueyiRotationDuration = totalXueyiEffect.actionvalue * 100.0 / XueyiCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    # scale other character's rotation
    HanabiRotation = [x * XueyiRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    PelaRotation = [x * XueyiRotationDuration / PelaRotationDuration for x in PelaRotation]
    FuxuanRotation = [x * XueyiRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    XueyiEstimate = DefaultEstimator(f'Xueyi: {numSkillXueyi:.1f}E {numUltXueyi:.0f}Q {numTalentXueyi:.1f}T with {breakRatio*100.0:.0f}% of hits depleting toughness', XueyiRotation, XueyiCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 1N 1E 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([XueyiEstimate,HanabiEstimate,PelaEstimate,FuxuanEstimate])