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


def run_harvester(creep, distribution, structureDict):
    creep.memory.role = 'Harvester'
    #print(creep)
    if not creep.memory.state == 'Depositing':
        creep.memory.state = 'Harvesting'

    if creep.memory.state == 'Harvesting':
        behaviors.harvestEnergy(creep, distribution)
    elif creep.memory.state == 'Depositing':
        # If we have a saved target, use it
        if creep.memory.target:
            #print('{} keeping target'.format(creep))
            target = Game.getObjectById(creep.memory.target)
        else:
            ## Vælg target i prioriteret rækkefølge
            ## Spawns
            ## Extensions op til 350 energy
            ## Towers
            ## Controller eller extensions (hvis energi ikke er fuld)
            target = None
            for spawn in structureDict['spawns']:
                if spawn.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
                    target = spawn
            if not target and creep.room.energyAvailable < 350:
                for ext in structureDict['extensions']:
                    if ext.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
                        target = ext
            if not target:
                for tower in structureDict['towers']:
                    if tower.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
                        target = tower
            if not target:
                if creep.room.energyAvailable == creep.room.energyCapacityAvailable:
                    target = _.sample(structureDict['controllers'])
                else:
                    selection = _.sample([structureDict['controllers'], structureDict['extensions']])
                    target = _.sample(selection)

            creep.memory.target = target.id

        behaviors.depositEnergy(creep, target)
