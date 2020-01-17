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

def run_wall_e(creep, distribution):
    creep.memory.role = 'Wall-E'

    if creep.memory.state != 'Walling' and creep.memory.state != 'Harvesting':
        creep.memory.state = 'Walling'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep, distribution)
    elif creep.memory.state == 'Walling':
        if creep.memory.targetWall:
            print('Wall-E keeps target')
            target = Game.getObjectById(creep.memory.targetWall)
        else:
            print('Wall-E new target')
            walls = creep.room.find(FIND_STRUCTURES).filter(lambda s: (s.structureType==STRUCTURE_WALL))
            if len(walls) > 0:
                weakest = walls[0]
                for wall in walls:
                    if wall.hits < weakest.hits:
                        weakest = wall
                    creep.memory.targetWall = weakest.id
                    # Wall or move closer
            target = Game.getObjectById(creep.memory.targetWall)

        if creep.pos.inRangeTo(target, 3):
            print('Wall-E repairs target')
            result = creep.repair(target)
            if result == ERR_NOT_ENOUGH_RESOURCES:
                creep.memory.state = 'Harvesting'
            elif result != OK:
                creep.memory.state = 'Harvesting'
                del creep.memory.targetWall
        else:
            print('Wall-E moving to target')
            creep.moveTo(target)
