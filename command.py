import pygame
from pygame.math import Vector2
from unit import Unit, Bullet
import tmx
import os


class Command():
    def run(self):
        raise NotImplementedError()
        
class MoveCommand(Command):
    """
    This command moves a unit in a given direction
    """
    def __init__(self,state,unit,moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
    def run(self):
        unit = self.unit
        
        # Destroyed units can't move
        if unit.status != "alive":
            return

        # Update unit orientation
        if self.moveVector.x < 0: 
            unit.orientation = 90
        elif self.moveVector.x > 0: 
            unit.orientation = -90
        if self.moveVector.y < 0: 
            unit.orientation = 0
        elif self.moveVector.y > 0: 
            unit.orientation = 180
        
        # Compute new tank position
        newPos = unit.position + self.moveVector

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow other unit positions 
        unitIndex = self.state.findUnit(newPos)
        if not unitIndex is None:
                return

        unit.position = newPos
        
class TargetCommand(Command):
    def __init__(self,state,unit,target):
        self.state = state
        self.unit = unit
        self.target = target
    def run(self):
        self.unit.weaponTarget = self.target
        
class ShootCommand(Command):
    def __init__(self,state,unit):
        self.state = state
        self.unit = unit
    def run(self):
        if self.unit.status != "alive":
            return
        if self.state.epoch-self.unit.lastBulletEpoch < self.state.bulletDelay:
            return
        self.unit.lastBulletEpoch = self.state.epoch
        self.state.bullets.append(Bullet(self.state,self.unit))
        
class MoveBulletCommand(Command):
    def __init__(self,state,bullet):
        self.state = state
        self.bullet = bullet
    def run(self):
        direction = (self.bullet.endPosition - self.bullet.startPosition).normalize()
        newPos = self.bullet.position + self.state.bulletSpeed * direction
        newCenterPos = newPos + Vector2(0.5,0.5)
        # If the bullet goes outside the world, destroy it
        if not self.state.isInside(newPos):
            self.bullet.status = "destroyed"
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction.x >= 0 and newPos.x >= self.bullet.endPosition.x) \
        or (direction.x < 0 and newPos.x <= self.bullet.endPosition.x)) \
        and ((direction.y >= 0 and newPos.y >= self.bullet.endPosition.y) \
        or (direction.y < 0 and newPos.y <= self.bullet.endPosition.y)):
            self.bullet.status = "destroyed"
            return
        # If the bullet is outside the allowed range, destroy it
        if newPos.distance_to(self.bullet.startPosition) >= self.state.bulletRange:  
            self.bullet.status = "destroyed"
            return
        # If the bullet hits a unit, destroy the bullet and the unit 
        unit = self.state.findLiveUnit(newCenterPos)
        if not unit is None and unit != self.bullet.unit:
            self.bullet.status = "destroyed"
            unit.status = "destroyed"
            self.state.notifyUnitDestroyed(unit)
            return
        # Nothing happends, continue bullet trajectory
        self.bullet.position = newPos
        
class DeleteDestroyedCommand(Command):
    def __init__(self,itemList):
        self.itemList = itemList
    def run(self):
        newList = [ item for item in self.itemList if item.status == "alive" ]
        self.itemList[:] = newList
        
        
class LoadLevelCommand(Command):
    def __init__(self,ui,fileName):
        self.ui = ui
        self.fileName = fileName
        
    def decodeLayer(self,tileMap,layer):
        """
        Decode layer and check layer properties
        
        Returns the corresponding tileset
        """
        if not isinstance(layer,tmx.Layer):
            raise RuntimeError("Error in {}: invalid layer type".format(self.fileName))
        if len(layer.tiles) != tileMap.width * tileMap.height:
            raise RuntimeError("Error in {}: invalid tiles count".format(self.fileName))
        
        # Guess which tileset is used by this layer
        gid = None
        for tile in layer.tiles:
            if tile.gid != 0:
                gid = tile.gid
                break
        if gid is None:
            if len(tileMap.tilesets) == 0:
                raise RuntimeError("Error in {}: no tilesets".format(self.fileName))
            tileset = tileMap.tilesets[0]
        else:
            tileset = None
            for t in tileMap.tilesets:
                if gid >= t.firstgid and gid < t.firstgid+t.tilecount:
                    tileset = t
                    break
            if tileset is None:
                raise RuntimeError("Error in {}: no corresponding tileset".format(self.fileName))
            
        # Check the tileset
        if tileset.columns <= 0:
            raise RuntimeError("Error in {}: invalid columns count".format(self.fileName))
        if tileset.image.data is not None:
            raise RuntimeError("Error in {}: embedded tileset image is not supported".format(self.fileName))
            
        return tileset
        
    def decodeArrayLayer(self,tileMap,layer):
        """
        Create an array from a tileMap layer
        """        
        tileset = self.decodeLayer(tileMap,layer)
        
        array = [ None ] * tileMap.height
        for y in range(tileMap.height):
            array[y] = [ None ] * tileMap.width
            for x in range(tileMap.width):
                tile = layer.tiles[x + y*tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array[y][x] = Vector2(tileX,tileY)

        return tileset, array
    
    def decodeUnitsLayer(self,state,tileMap,layer):
        """
        Create a list from a tileMap layer
        """        
        tileset = self.decodeLayer(tileMap,layer)

        units = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y*tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                unit = Unit(state,Vector2(x,y),Vector2(tileX,tileY))
                units.append(unit)

        return tileset, units
        
        
    def run(self):
        # Load map
        if not os.path.exists(self.fileName):
            raise RuntimeError("No file {}".format(self.fileName))
        tileMap = tmx.TileMap.load(self.fileName)
        
        # Check main properties
        if tileMap.orientation != "orthogonal":
            raise RuntimeError("Error in {}: invalid orientation".format(self.fileName))
            
        if len(tileMap.layers) != 5:
            raise RuntimeError("Error in {}: 5 layers are expected".format(self.fileName))

        # World size
        state = self.ui.gameState
        state.worldSize = Vector2(tileMap.width,tileMap.height)    

        # Ground layer
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[0])
        cellSize = Vector2(tileset.tilewidth,tileset.tileheight)
        state.ground[:] = array
        imageFile = tileset.image.source
        self.ui.layers[0].setTileset(cellSize,imageFile)

        # Walls layer
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[1])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.walls[:] = array
        imageFile = tileset.image.source
        self.ui.layers[1].setTileset(cellSize,imageFile)

        # Units layer
        tanksTileset, tanks = self.decodeUnitsLayer(state,tileMap,tileMap.layers[2])
        towersTileset, towers = self.decodeUnitsLayer(state,tileMap,tileMap.layers[3])
        if tanksTileset != towersTileset:
            raise RuntimeError("Error in {}: tanks and towers tilesets must be the same".format(self.fileName))
        if tanksTileset.tilewidth != cellSize.x or tanksTileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.units[:] = tanks + towers
        cellSize = Vector2(tanksTileset.tilewidth,tanksTileset.tileheight)
        imageFile = tanksTileset.image.source
        self.ui.layers[2].setTileset(cellSize,imageFile)

        # Player units
        self.ui.playerUnit = tanks[0]      
        
        # Explosions layers
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[4])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.bullets.clear()
        imageFile = tileset.image.source
        self.ui.layers[3].setTileset(cellSize,imageFile)
        
        # Window
        windowSize = state.worldSize.elementwise() * cellSize
        self.ui.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))