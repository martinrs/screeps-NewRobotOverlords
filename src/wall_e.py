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

def run_wall_e(creep):
    creep.memory.role = 'Wall-E'

    if creep.memory.state != 'Walling' and creep.memory.state != 'Harvesting':
        creep.memory.state = 'Walling'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep)
    elif creep.memory.state == 'Walling':
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            walls = creep.room.find(FIND_STRUCTURES).filter(lambda s: (s.structureType(STRUCTURE_WALL)))
            if len(walls) > 0:
                weakest = walls[0]
                for wall in walls:
                    if wall.hits < weakest.hits:
                        weakest = wall
                if weakest.hits < 10000:
                    creep.memory.target = weakest.id
                    # Wall or move closer
                    if creep.pos.isNearTo(weakest, 3):
                        result = creep.repair(weakest)
                        if result == ERR_NOT_ENOUGH_RESOURCES:
                            creep.memory.state = 'Harvesting'
                        elif result != OK:
                            creep.memory.state = 'Harvesting'
                            del creep.memory.target
                    else:
                        creep.moveTo(target)

            creep.memory.target = target.id
