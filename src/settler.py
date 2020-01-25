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
    print(targetRoom)
    if creep.room.id == targetRoom:
        print('in the room')
        if creep.pos.isNearTo(creep.room.controller):
            creep.claimController(creep.room.controller)
        else:
            moveto(creep.room.controller)
    else:
        print('going to room')
        if creep.memory.path:
            creep.moveTo(creep.pos.findClosestByRange(creep.memory.path[0].exit))
        else:
            creep.memory.path = Game.map.findRoute(creep.room, targetRoom)
