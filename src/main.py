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

def countStuff(room):
    creeps = room.find(FIND_MY_CREEPS)
    actualHarvesters = _.sum(creeps, lambda h: h.memory.role == 'Harvester')
    actualBuilders = _.sum(creeps, lambda b: b.memory.role == 'Builder')
    actualWallEs = _.sum(creeps, lambda b: b.memory.role == 'Wall-E')
    return {'actualHarvesters': actualHarvesters, 'actualBuilders': actualBuilders, 'actualWallEs': actualWallEs}

def makeStructureDict(room):
    spawns = room.find(FIND_MY_SPAWNS)
    towers = []
    extensions = []
    controllers = []

    structures = room.find(FIND_MY_STRUCTURES)
    for structure in room.find(FIND_STRUCTURES):
        if structure.structureType == STRUCTURE_TOWER:
            towers.append(structure)
        elif structure.structureType == STRUCTURE_EXTENSION:
            extensions.append(structure)
        elif structure.structureType == STRUCTURE_CONTROLLER:
            controllers.append(structure)

    return {'spawns': spawns, 'towers': towers, 'extensions': extensions, 'controllers': controllers}


def main():
    ########### Creep memory management - Multiroom safe
    # Clear dead ones
    for name in Object.keys(Memory.creeps):
        if not Game.creeps[name]:
            del Memory.creeps[name]

    ########### Spawn instructions - Multiroom safe
    controlledRooms = []
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        # Find de rum, jeg kontrollerer
        if not spawn.room.id in controlledRooms:
            controlledRooms.append(spawn.room)
        if not spawn.spawning:
            num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)
            if num_creeps < 10 and spawn.room.energyAvailable >= 800:
                spawn.createCreep([WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE])
            elif num_creeps < 10 and spawn.room.energyAvailable >= 400:
                spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE])
            elif num_creeps <= 5 and spawn.room.energyAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])

    ############ Strategic planning section - Multiroom safe
    strategyData = {}
    structureDict = {}
    workerDistribution = {}
    for room in controlledRooms:
        if room not in Object.keys(strategyData):
            strategyData[room] = {}
        creepsInRoom = room.find(FIND_MY_CREEPS)

        strategyData[room]['desiredBuilders'] = 0
        strategyData[room]['desiredWallEs'] = 0

        structureDict[room] = makeStructureDict(room)

        if len(creepsInRoom) > 0:
            numberOfConstructionSites = len(room.find(FIND_MY_CONSTRUCTION_SITES))
            if numberOfConstructionSites > 0:
                strategyData[room]['desiredBuilders'] = int(numberOfConstructionSites / len(creepsInRoom))
                if strategyData[room]['desiredBuilders'] < 2:
                    strategyData[room]['desiredBuilders'] = 2

            weakwalls = len(room.find(FIND_STRUCTURES).filter(lambda s: (s.structureType==STRUCTURE_WALL and s.hits < wall_e.weakWallLimit)))
            if weakwalls > 0:
                strategyData[room]['desiredWallEs'] = 1

        ########### Tower work allocation - Multiroom safe
        for aTower in room.find(FIND_MY_STRUCTURES).filter(lambda s: s.structureType == STRUCTURE_TOWER):
            tower.run_tower(aTower)

        ########### Creep work allocation  - Multiroom safe
        enemyCreeps = room.find(FIND_HOSTILE_CREEPS)
        creepsInRoom = room.find(FIND_MY_CREEPS)
        workerDistribution[room] = countStuff(room)

        for name in Object.keys(creepsInRoom).reverse():
            creep = creepsInRoom[name]
            harvesterDistribution = countHarvesterDistribution(room)
            if len(enemyCreeps) > 0:
                wall_e.run_wall_e(creep, harvesterDistribution)
            else:
                if creep.memory.role == 'Builder':
                    if workerDistribution[room]['actualBuilders'] <= strategyData[room]['desiredBuilders']:
                        creep.memory.target = ''
                        builder.run_builder(creep, harvesterDistribution)
                    elif workerDistribution[room]['actualBuilders'] > strategyData[room]['desiredBuilders']:
                        creep.memory.constructing = ''
                        harvester.run_harvester(creep, harvesterDistribution, structureDict[room])
                elif workerDistribution[room]['actualBuilders'] < strategyData[room]['desiredBuilders']:
                    creep.memory.target = ''
                    builder.run_builder(creep, harvesterDistribution)

                elif creep.memory.role == 'Wall-E':
                    if workerDistribution[room]['actualWallEs'] <= strategyData[room]['desiredWallEs']:
                        wall_e.run_wall_e(creep, harvesterDistribution)
                    elif workerDistribution[room]['actualWallEs'] > strategyData[room]['desiredWallEs']:
                        harvester.run_harvester(creep, harvesterDistribution, structureDict[room])
                elif workerDistribution[room]['actualWallEs'] < strategyData[room]['desiredWallEs']:
                    creep.memory.target = ''
                    wall_e.run_wall_e(creep, harvesterDistribution)
                else:
                    harvester.run_harvester(creep, harvesterDistribution, structureDict[room])

            workerDistribution[room] = countStuff(room)

    ############ Report to console  - Multiroom safe
    for room in Object.keys(workerDistribution):
        print('{}: {} Creeps\t{}/{} Builders\t{} Wall-Es\t{} Harvesters'.format(room, len(creepsInRoom), workerDistribution[room]['actualBuilders'],strategyData[room]['desiredBuilders'], workerDistribution[room]['actualWallEs'], workerDistribution[room]['actualHarvesters']))

module.exports.loop = main
