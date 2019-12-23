import harvester, builder, wall_e
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

actualHarvesters, actualBuilders, actualWallEs = 0

def updateHarvesterDistribution(room):
    distribution = {}

    for source in room.find(FIND_SOURCES):
        if not source.id in distribution:
            distribution[source.id] = 0
        for creep in Object.keys(Game.creeps):
            if creep.pos.room == room and creep.memory.target == source.id:
                distribution[source.id] += 1
    print(distribution)
    return distribution

def countStuff():
    global actualHarvesters, actualBuilders, actualWallEs
    actualHarvesters = _.sum(Game.creeps, lambda h: h.memory.role == 'Harvester')
    actualBuilders = _.sum(Game.creeps, lambda b: b.memory.role == 'Builder')
    actualWallEs = _.sum(Game.creeps, lambda b: b.memory.role == 'Wall-E')

    #harvesterDistribution = updateHarvesterDistribution(Game.creeps[0].pos.room)

def main():
    global actualHarvesters, actualBuilders, actualWallEs
    countStuff()
############ Strategic planning section
    desiredBuilders = 3
    desiredWallEs = 0

############ Report to console


########### Creep memory management
    # Clear dead ones
    for name in Object.keys(Memory.creeps):
        if not Game.creeps[name]:
            del Memory.creeps[name]

########### Work allocation
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]

        if actualBuilders < desiredBuilders:
            #builder.run_builder(creep, harvesterDistribution)
            builder.run_builder(creep)
            #harvesterDistribution = updateHarvesterDistribution()
        elif actualWallEs < desiredWallEs:
            wall_e.run_wall_e(creep)
        else:
            harvester.run_harvester(creep)
        countStuff()

############ Report to console
    actualHarvesters = _.sum(Game.creeps, lambda h: h.memory.role == 'Harvester')
    actualBuilders = _.sum(Game.creeps, lambda b: b.memory.role == 'Builder')
    actualWallEs = _.sum(Game.creeps, lambda b: b.memory.role == 'Wall-E')
    print('{} Creeps\t{}/{} Builders\t{} Wall-Es\t{} Harvesters'.format(len(Game.creeps), actualBuilders,desiredBuilders, actualWallEs, actualHarvesters))

########### Spawn instructions
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            # Get the number of our creeps in the room.
            num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)
            # If there are no creeps, spawn a creep once energy is at 250 or more
            if num_creeps < 0 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])
            # If there are less than 10 creeps but at least one, wait until all spawns and extensions are full before
            # spawning.
            elif num_creeps < 10 and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
                # If we have more energy, spawn a bigger creep.
                if spawn.room.energyCapacityAvailable >= 350:
                    spawn.createCreep([WORK, CARRY, CARRY, MOVE, MOVE, MOVE])
                else:
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE])

module.exports.loop = main
