from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def harvestEnergy(creep, distribution):
    #def harvestEnergy(creep, distribution):

    # If we're full, stop filling up and remove the saved source
    if creep.memory.state == 'Harvesting' and _.sum(creep.carry) >= creep.carryCapacity:
        creep.memory.state = 'Depositing'
        del creep.memory.source
    # If we're empty, start filling again and remove the saved target
    elif not creep.memory.state == 'Harvesting' and creep.carry.energy <= 0:
        creep.memory.state = 'Harvesting'
        del creep.memory.target

    if creep.memory.state == 'Harvesting':
        # If we have a saved source, use it
        if not creep.memory.source:
            source = _.sample(Object.keys(distribution))
            for s in Object.keys(distribution):
                if distribution[s] < distribution[source]:
                    source = s
            creep.memory.source = source
        source = Game.getObjectById(creep.memory.source)

        creep.memory.source = source.id

        # If we're near the source, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(source):
            result = creep.harvest(source)
            if result != OK:
                print("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        else:
            creep.moveTo(source)

def depositEnergy(creep, target):
    creep.memory.state = 'Depositing'
    # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
    if target.energyCapacity:
        is_close = creep.pos.isNearTo(target)
    else:
        is_close = creep.pos.inRangeTo(target, 3)

    if is_close:
        # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
        if target.store:
            result = creep.transfer(target, RESOURCE_ENERGY)
            if result == ERR_NOT_ENOUGH_RESOURCES:
                del creep.memory.target
                creep.memory.state = 'Harvesting'
            elif result == ERR_FULL:
                del creep.memory.target
            else:
                print("[{}] Unknown result from creep.transfer({}, {}): {}".format(
                    creep.name, target, RESOURCE_ENERGY, result))
        else:
            result = creep.upgradeController(target)
        if result != OK:
            print("[{}] Unknown result from creep.upgradeController({}): {}".format(creep.name, target, result))
            del creep.memory.target
    else:
        creep.moveTo(target)
