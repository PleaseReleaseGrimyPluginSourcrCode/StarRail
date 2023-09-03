from copy import copy
from baseClasses.RelicStats import RelicStats
from characters.erudition.Serval import Serval, ServalEstimationV1
from characters.destruction.Blade import Blade, BladeEstimationsV1
from characters.hunt.DanHeng import DanHeng, DanHengEstimationV1
from characters.hunt.Yanqing import Yanqing, YanqingEstimationV1
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from settings.BaseConfiguration import Configuration
from visualizer.visualizer import visualize

if __name__ == '__main__':
    CharacterDict = {} # store character information here
    EffectDict = {} # store dps metrics here
    
    config = copy(Configuration)
    
    ServalCharacter = Serval(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = TheSeriousnessOfBreakfast(stacks=3,**config),
                relicsetone = ThiefOfShootingMeteor2pc(),
                relicsettwo = ThiefOfShootingMeteor4pc(),
                planarset = SpaceSealingStation(),
                **config)
    
    ServalEstimationV1(ServalCharacter, config, CharacterDict, EffectDict)
    
    DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.5, uptimeDefeat=1.0, **config),
                relicsetone = EagleOfTwilightLine2pc(),
                planarset = SpaceSealingStation(),
                talentUptime = 0.0,
                slowUptime = 1.0,
                fasterThanLightUptime = 1.0,
                **config)
    
    DanHengEstimationV1(DanHengCharacter, config, CharacterDict, EffectDict)
    
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'percAtk': 8, 'CD': 12}),
                    lightcone = CruisingInTheStellarSea(uptimeHP=0.5, uptimeDefeat=1.0, **config),
                    relicsetone = HunterOfGlacialForest2pc(),
                    relicsettwo = HunterOfGlacialForest4pc(),
                    planarset = SpaceSealingStation(),
                    soulsteelUptime = 1.0,
                    searingStingUptime = 1.0,
                    rainingBlissUptime = 0.25,
                    **config)
    
    YanqingEstimationV1(YanqingCharacter, config, CharacterDict, EffectDict)

    bladeCharacter = Blade(RelicStats(mainstats = ['percHP', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 7, 'CD': 7, 'flatSpd': 6}),
                lightcone = ASecretVow(uptime = 0.5, **config),
                relicsetone = LongevousDisciple2pc(),
                relicsettwo = LongevousDisciple4pc(),
                planarset = InertSalsotto(),
                hpLossTally=0.5,
                **config)
        
    BladeEstimationsV1(bladeCharacter, config, CharacterDict, EffectDict)

    visualize(CharacterDict, EffectDict, **config)