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

def run_settler(creep, targetRoom):
    if creep.memory.path:
        if creep.room.name == targetRoom:
            target = Game.rooms[targetRoom].controller
            if creep.pos.isNearTo(target):
                creep.claimController(target)
            else:
                creep.moveTo(target)
        else:
            creep.moveTo(creep.pos.findClosestByRange(creep.memory.path[0].exit))
    else:
        creep.memory.path = Game.map.findRoute(creep.room, targetRoom)
