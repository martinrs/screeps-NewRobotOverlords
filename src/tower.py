from defs import *
import behaviors

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

"""
Prioritet for tårn:
Search and destroy
Heal Creeps
Rep bygninger (ikke walls)
"""

def run_tower(tower):
    if tower.isActive():

        ##### Search and destroy
        enemyCreeps = tower.room.find(FIND_HOSTILE_CREEPS)
        if len(enemyCreeps) > 0:
            print('Tower angriber')
            closest = _.sample(enemyCreeps)
            rangeToClosest = tower.pos.getRangeTo(closest)
            for creep in enemyCreeps:
                rangeToCreep = tower.pos.getRangeTo(closest)
                if rangeToCreep < rangeToClosest:
                    closest = creep
                    rangeToClosest = rangeToCreep
            tower.attack(closest)
        else:
            ### Heal Creeps
            weakest = _.sample(Game.creeps)
            weakestHitPercent = weakest.hits/weakest.hitsMax
            for name in Object.keys(Game.creeps):
                creep = Game.creeps[name]
                if creep.hits / creep.hitsMax < weakestHitPercent:
                    weakest = creep
                    weakestHitPercent = weakest.hits/weakest.hitsMax
            if weakestHitPercent < 1:
                print('Tower healer')
                tower.heal(weakest)
            else:
                ### Reparation af bygninger
                structures = tower.room.find(FIND_STRUCTURES).filter(lambda s: (s.structureType!=STRUCTURE_WALL and s.structureType != STRUCTURE_CONTROLLER and s.structureType!=STRUCTURE_RAMPART))
                weakest = _.sample(structures)
                weakestHitPercent = weakest.hits/weakest.hitsMax
                for structure in structures:
                    if structure.hits / structure.hitsMax < weakestHitPercent:
                        weakest = structure
                        weakestHitPercent = weakest.hits/weakest.hitsMax
                if weakestHitPercent < 1:
                    tower.repair(weakest)
