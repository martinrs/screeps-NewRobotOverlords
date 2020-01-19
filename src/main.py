import harvester, builder, wall_e, tower
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

def countHarvesterDistribution(room):
    distribution = {}
    for source in room.find(FIND_SOURCES):
        if not source.id in Object.keys(distribution):
            distribution[source.id] = 0
        for name in Object.keys(Game.creeps):
            creep = Game.creeps[name]
            if creep.room == room and creep.memory.source == source.id:
                distribution[source.id] += 1
    return distribution

def countStuff():
    global actualHarvesters, actualBuilders, actualWallEs
    actualHarvesters = _.sum(Game.creeps, lambda h: h.memory.role == 'Harvester')
    actualBuilders = _.sum(Game.creeps, lambda b: b.memory.role == 'Builder')
    actualWallEs = _.sum(Game.creeps, lambda b: b.memory.role == 'Wall-E')

def main():
    global actualHarvesters, actualBuilders, actualWallEs
    countStuff()
############ Strategic planning section
    desiredBuilders = 0
    desiredWallEs = 0
    if len(Game.creeps) > 0:
        aCreep = _.sample(Game.creeps)
        numberOfConstructionSites = len(aCreep.room.find(FIND_MY_CONSTRUCTION_SITES))
        if numberOfConstructionSites > 0:
            desiredBuilders = int(numberOfConstructionSites / len(Game.creeps))
            if desiredBuilders < 1:
                desiredBuilders = 1

        weakwalls = len(aCreep.room.find(FIND_STRUCTURES).filter(lambda s: (s.structureType==STRUCTURE_WALL and s.hits < wall_e.weakWallLimit)))
        if weakwalls > 0:
            desiredWallEs = 1

########### Tower work allocation
        for tower in aCreep.room.find(FIND_STRUCTURES).filter(lambda s: s.structureType == STRUCTURE_TOWER):
            tower.run_tower(tower)

########### Creep memory management
    # Clear dead ones
    for name in Object.keys(Memory.creeps):
        if not Game.creeps[name]:
            del Memory.creeps[name]

########### Creep work allocation
    for name in Object.keys(Game.creeps).reverse():
        creep = Game.creeps[name]
        harvesterDistribution = countHarvesterDistribution(creep.room)
        if creep.memory.role == 'Builder':
            if actualBuilders <= desiredBuilders:
                creep.memory.target = ''
                builder.run_builder(creep, harvesterDistribution)
            elif actualBuilders > desiredBuilders:
                creep.memory.constructing = ''
                harvester.run_harvester(creep, harvesterDistribution)
        elif actualBuilders < desiredBuilders:
            creep.memory.target = ''
            builder.run_builder(creep, harvesterDistribution)

        elif creep.memory.role == 'Wall-E':
            if actualWallEs <= desiredWallEs:
                wall_e.run_wall_e(creep, harvesterDistribution)
            elif actualWallEs > desiredWallEs:
                harvester.run_harvester(creep, harvesterDistribution)
        elif actualWallEs < desiredWallEs:
            creep.memory.target = ''
            wall_e.run_wall_e(creep, harvesterDistribution)
        else:
            harvester.run_harvester(creep, harvesterDistribution)
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
            if num_creeps <= 5 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])
            # If there are less than 10 creeps but at least one, wait until all spawns and extensions are full before
            # spawning.
            elif num_creeps < 15 and spawn.room.energyAvailable >= spawn.room.energyCapacityAvailable:
                # If we have more energy, spawn a bigger creep.
                if spawn.room.energyCapacityAvailable >= 350:
                    spawn.createCreep([WORK, CARRY, CARRY, MOVE, MOVE, MOVE])
            elif num_creeps == 0:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])

module.exports.loop = main
