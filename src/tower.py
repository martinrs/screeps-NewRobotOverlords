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
            closest = _.sample(enemyCreeps)
            print(closest)
            rangeToClosest = tower.pos.getRangeTo(closest)
            for creep in enemyCreeps:
                rangeToCreep = tower.pos.getRangeTo(closest)
                if rangeToCreep < rangeToClosest:
                    closest = creep
                    rangeToClosest = rangeToCreep
            tower.attack(closest)
        else:
            pass
            #myCreeps = Game.creeps.filter(lambda s: s.room == tower.room)
