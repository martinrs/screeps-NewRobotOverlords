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

def run_builder(creep):
    creep.memory.role = 'Builder'
    #print('Builder {} assigned to {}'.format(creep.name, creep.memory.state))

    if creep.memory.state == 'Depositing':
        creep.memory.state = 'Building'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep)
    elif creep.memory.state == 'Building':
        # Select target
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = _.sample(creep.room.find(FIND_MY_CONSTRUCTION_SITES))
            creep.memory.target = target.id

        # Build or move closer
        if creep.pos.isNearTo(target):
            result = creep.build(target)
            if result == ERR_NOT_ENOUGH_RESOURCES:
                creep.memory.state = 'Harvesting'
            elif result != OK:
                creep.memory.state = 'Harvesting'
                del creep.memory.target
        else:
            creep.moveTo(target)
    else:
        creep.memory.state = 'Building'
