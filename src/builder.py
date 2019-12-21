from defs import *
import harvester

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
    #print('{} assigned to build'.format(creep.name))
    if creep.memory.state == 'Depositing':
        creep.memory.state = 'Building'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep)
    else:
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = _.sample(creep.room.find(FIND_MY_CONSTRUCTION_SITES))
            creep.memory.target = target.id

        if creep.memory.target:
            if creep.pos.isNearTo(target):
                result = creep.build(target)
                if result != OK:
                    del creep.memory.target
            else:
                creep.moveTo(target)
