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

def hasValidConstructionTarget(creep, sites):
    for site in sites:
        if site.id == creep.memory.constructing:
            return True
    return False

def run_builder(creep, distribution):
    creep.memory.role = 'Builder'
    #print('Builder {} assigned to {}'.format(creep.name, creep.memory.state))

    if creep.memory.state == 'Depositing':
        creep.memory.state = 'Building'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep, distribution)
    elif creep.memory.state == 'Building':
        sites = creep.room.find(FIND_MY_CONSTRUCTION_SITES)
        # Select target
        if hasValidConstructionTarget(creep, sites):
            creep.say('{} keeping target'.format(creep))
            target = Game.getObjectById(creep.memory.constructing)
        else:
            creep.say('{} getting new random target'.format(creep.name))
            target = _.sample(sites)
            #print(creep.room.find(FIND_MY_CONSTRUCTION_SITES))
            creep.memory.constructing = target.id

        # Build or move closer
        #print('{} building {} ({})'.format(creep, Game.getObjectById(creep.memory.target).structureType, target))
        if creep.pos.inRangeTo(target, 3):
            result = creep.build(target)
            print('{} built {} with result {}'.format(creep.name, target, result))
            if result == ERR_NOT_ENOUGH_RESOURCES:
                creep.memory.state = 'Harvesting'
            elif result != OK:
                print('Deleted target')
                del creep.memory.constructing
        else:
            print('Moving to {}'.format(target))
            creep.moveTo(target)
    else:
        creep.memory.state = 'Building'
