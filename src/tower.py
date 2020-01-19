from defs import *
import behaviors
from math import sqrt, pow

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def run_tower(tower):
    if tower.isactive():

        ##### Search and destroy
        enemyCreeps = tower.room.find(FIND_HOSTILE_CREEPS)
        if len(enemyCreeps) > 0:
            closest = enemyCreeps[0]
            rangeToClosest = tower.room.pos.getRangeTo(closest)
            for creep in enemyCreeps:
                rangeToCreep = tower.room.pos.getRangeTo(closest)
                if rangeToCreep < rangeToClosest:
                    closest = creep
                    rangeToClosest = rangeToCreep
            tower.attack(closest)

        myCreeps = Game.creeps.filter(lambda s: s.room == tower.room)
