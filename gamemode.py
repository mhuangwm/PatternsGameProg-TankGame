import pygame
from gamestate import *
from layer import *
from command import *

class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()

class MessageGameMode(GameMode):
    def __init__(self, ui, message):        
        self.ui = ui
        self.font = pygame.font.Font("BD_Cartoon_Shout.ttf", 36)
        self.message = message

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ui.quitGame()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_SPACE \
                or event.key == pygame.K_RETURN:
                    self.ui.showMenu()
                    
    def update(self):
        pass
        
    def render(self, window):
        surface = self.font.render(self.message, True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        y = (window.get_height() - surface.get_height()) // 2
        window.blit(surface, (x, y))

class MenuGameMode(GameMode):
    def __init__(self, ui):        
        self.ui = ui
        
        # Font
        self.titleFont = pygame.font.Font("BD_Cartoon_Shout.ttf", 72)
        self.itemFont = pygame.font.Font("BD_Cartoon_Shout.ttf", 48)
        
        # Menu items
        self.menuItems = [
            {
                'title': 'Level 1',
                'action': lambda: self.ui.loadLevel("level1.tmx")
            },
            {
                'title': 'Level 2',
                'action': lambda: self.ui.loadLevel("level2.tmx")
            },
            {
                'title': 'Level 3',
                'action': lambda: self.ui.loadLevel("level3.tmx")
            },
            {
                'title': 'Quit',
                'action': lambda: self.ui.quitGame()
            }
        ]        

        # Compute menu width
        self.menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item['title'], True, (200, 0, 0))
            self.menuWidth = max(self.menuWidth, surface.get_width())
            item['surface'] = surface        
        
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("cursor.png")        

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ui.quitGame()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ui.showGame()
                elif event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem['action']()
                    except Exception as ex:
                        print(ex)
                    
    def update(self):
        pass
        
    def render(self, window):
        # Initial y
        y = 50
        
        # Title
        surface = self.titleFont.render("TANK BATTLEGROUNDS !!", True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100
        
        # Draw menu items
        x = (window.get_width() - self.menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item['surface']
            window.blit(surface, (x, y))
            
            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                window.blit(self.menuCursor, (cursorX, cursorY))
            
            y += (120 * surface.get_height()) // 100           
            

class PlayGameMode(GameMode):
    def __init__(self, ui):
        self.ui = ui
        
        # Game state
        self.gameState = GameState()
        
        # Rendering properties
        self.cellSize = Vector2(64,64)        

        # Layers
        self.layers = [
            ArrayLayer(self.cellSize,"ground.png",self.gameState,self.gameState.ground,0),
            ArrayLayer(self.cellSize,"walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self.cellSize,"units.png",self.gameState,self.gameState.units),
            BulletsLayer(self.cellSize,"explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.cellSize,"explosions.png"),
            SoundLayer("170274__knova__rifle-fire-synthetic.wav","110115__ryansnook__small-explosion.wav")
        ]
        
        # All layers listen to game state events
        for layer in self.layers:
            self.gameState.addObserver(layer)

        # Controls
        self.playerUnit = self.gameState.units[0]
        self.gameOver = False
        self.commands = [ ]
        
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        # Pygame events (close, keyboard and mouse click)
        moveVector = Vector2()
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ui.quitGame()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ui.showMenu()
                    break
                elif event.key == pygame.K_RIGHT:
                    moveVector.x = 1
                elif event.key == pygame.K_LEFT:
                    moveVector.x = -1
                elif event.key == pygame.K_DOWN:
                    moveVector.y = 1
                elif event.key == pygame.K_UP:
                    moveVector.y = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClicked = True

        # If the game is over, all commands creations are disabled
        if self.gameOver:
            return
                    
        # Keyboard controls the moves of the player's unit
        if moveVector.x != 0 or moveVector.y != 0:
            self.commands.append(
                MoveCommand(self.gameState,self.playerUnit,moveVector)
            )
                    
        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()                    
        targetCell = Vector2()
        targetCell.x = mousePos[0] / self.cellWidth - 0.5
        targetCell.y = mousePos[1] / self.cellHeight - 0.5
        command = TargetCommand(self.gameState,self.playerUnit,targetCell)
        self.commands.append(command)

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(self.gameState,self.playerUnit)
            )
            self.gameState.notifyBulletFired(self.playerUnit)
                
        # Other units always target the player's unit and shoot if close enough
        for unit in self.gameState.units:
            if unit != self.playerUnit:
                self.commands.append(
                    TargetCommand(self.gameState,unit,self.playerUnit.position)
                )
                if unit.position.distance_to(self.playerUnit.position) <= self.gameState.bulletRange:
                    self.commands.append(
                        ShootCommand(self.gameState,unit)
                    )
                
        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(
                MoveBulletCommand(self.gameState,bullet)
            )
            
        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(self.gameState.bullets)
        )
                    
    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1
        
        # Check game over
        if self.playerUnit.status != "alive":
            self.gameOver = True
            self.ui.showMessage("GAME OVER")
        else:
            oneEnemyStillLives = False
            for unit in self.gameState.units:
                if unit == self.playerUnit:
                    continue
                if unit.status == "alive":
                    oneEnemyStillLives = True
                    break
            if not oneEnemyStillLives:
                self.gameOver = True
                self.ui.showMessage("Victory !")
        
    def render(self, window):
        for layer in self.layers:
            layer.render(window)