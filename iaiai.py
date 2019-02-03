# You need to import colorfight for all the APIs
import colorfight as cf
import random
from threading import Thread
from math import sqrt

class IAiAI():
    def __init__( self, name = "AI? More like 愛" ):
        # Initialize the Panda Colorfight Client
        self.game = cf.Game()
        self.targets = []
        self.adjacentGold = []
        self.adjacentEnergy = []
        self.emptyGold = []
        self.emptyEnergy = []
        self.started = False
        self.startCell = (-1, -1)
        self.blacklist = set()

        # Attempt to join the game
        if self.game.JoinGame( name ):
            self.game.Refresh()
            self.Alina()
            self.FetchInfo()
            self.playing = True
            self.refreshThread = Thread( target = self.Refresh )
            self.refreshThread.start()
            self.playThread = Thread( target = self.Play )
            self.playThread.start()
            self.baseThread = Thread( target = self.Base )
            self.baseThread.start()
            self.stopThread = Thread( target = self.Stop )
            self.stopThread.start()

    def Alina( self ):
        offset = ( 0, 0 )
        bottom = ( 0, 3 )
        heartTemplate = []
        heartTemplate.append( ( 0, -1 ) )
        heartTemplate.append( ( 0, 0 ) )
        heartTemplate.append( ( 0, 1 ) )
        heartTemplate.append( ( 0, 2 ) )
        heartTemplate.append( ( 0, 3 ) )
        heartTemplate.append( ( -1, -2 ) )
        heartTemplate.append( ( -1, -1 ) )
        heartTemplate.append( ( -1, 0 ) )
        heartTemplate.append( ( -1, 1 ) )
        heartTemplate.append( ( -1, 2 ) )
        heartTemplate.append( ( +1, -2 ) )
        heartTemplate.append( ( +1, -1 ) )
        heartTemplate.append( ( +1, 0 ) )
        heartTemplate.append( ( +1, 1 ) )
        heartTemplate.append( ( +1, 2 ) )
        heartTemplate.append( ( -2, -2 ) )
        heartTemplate.append( ( -2, -1 ) )
        heartTemplate.append( ( -2, 0 ) )
        heartTemplate.append( ( -2, 1 ) )
        heartTemplate.append( ( +2, -2 ) )
        heartTemplate.append( ( +2, -1 ) )
        heartTemplate.append( ( +2, 0 ) )
        heartTemplate.append( ( +2, 1 ) )
        heartTemplate.append( ( -3, 0 ) )
        heartTemplate.append( ( -3, -1 ) )
        heartTemplate.append( ( +3, 0 ) )
        heartTemplate.append( ( +3, -1 ) )
        self.heartCells = []
        if not self.started:
            for x in range( 0, 30 ):
                for y in range( 0, 30 ):
                    c = self.game.GetCell( x, y )
                    if c.owner == self.game.uid and c.isBase:
                        self.startCell = ( x, y )
        if self.startCell[ 0 ] > 26:
            offset = ( -2, 0 )
        elif self.startCell[ 0 ] < 3:
            offset = ( 2, 0 )
        elif self.startCell[ 1 ] > 25:
            offset = ( 0, -2 )
        elif self.startCell[ 1 ] < 2:
            offset = ( 0, 1 )
        for temp in heartTemplate:
            self.heartCells.append( ( self.startCell[ 0 ] + temp[ 0 ] + offset[ 0 ], self.startCell[ 1 ] + temp[ 1 ] + offset[ 1 ] ) )
        bottom = ( 0 + self.startCell[ 0 ] + offset[ 0 ], 3 + self.startCell[ 1 ] + offset[ 1 ] )
        for cell in self.heartCells:
            nw = ( cell[ 0 ] - 1, cell[ 1 ] - 1 )
            ne = ( cell[ 0 ] + 1, cell[ 1 ] - 1 )
            sw = ( cell[ 0 ] - 1, cell[ 1 ] + 1 )
            se  = ( cell[ 0 ] + 1, cell[ 1 ] + 1 )
            up = ( cell[ 0 ], cell[ 1 ] - 1 )
            right = ( cell[ 0 ] + 1, cell[ 1 ] )
            down = ( cell[ 0 ], cell[ 1 ] + 1 )
            left = ( cell[ 0 ] - 1, cell[ 1 ] )
            if not up in self.heartCells:
                self.blacklist.add( up )
            if not right in self.heartCells:
                self.blacklist.add( right )
            if not down in self.heartCells and not cell == bottom:
                self.blacklist.add( down )
            if not left in self.heartCells:
                self.blacklist.add( left )
            if not nw in self.heartCells:
                self.blacklist.add( nw )
            if not ne in self.heartCells:
                self.blacklist.add( ne )
            if not sw in self.heartCells and not cell == bottom:
                self.blacklist.add( sw )
            if not se in self.heartCells and not cell == bottom:
                self.blacklist.add( se )
        building = True
        while building:
            building = False
            for cell in self.heartCells:
                print( cell )
                c = self.game.GetCell( cell[ 0 ], cell[ 1 ] )
                if c != None and 0 < c.takeTime < 4 and c.owner != self.game.uid:
                    data = self.game.AttackCell( cell[ 0 ], cell[ 1 ] )
                    if data[ 0 ]:
                        self.game.Refresh()
                    building = True

    # Refreshes the Game State
    def Refresh( self ):
        while self.playing:
            self.game.Refresh()
            self.FetchInfo()

    # Runs all base related functions
    def Base( self ):
        while self.playing:
            if self.game.gold >= 60 and self.game.baseNum < 3:
                cell = random.choice( self.heartCells )
                self.game.BuildBase( cell[ 0 ], cell[ 1 ] )
            #self.FetchBases()
            #try:
            #    self.BuildLoop()
            #except:
            #    pass
            pass

    # Runs all the AI actions
    def Play( self ):
        while self.playing:
            self.GameLoop()

    # Allows for keyboard interrupt
    def Stop( self ):
        input()
        self.playing = False

    def GetAdjacent( self, cell ):
        up = self.game.GetCell( cell.x, cell.y - 1 )
        right = self.game.GetCell( cell.x + 1, cell.y )
        down = self.game.GetCell( cell.x, cell.y + 1 )
        left = self.game.GetCell( cell.x - 1, cell.y )
        return ( up, right, down, left )

    def CheckTarget( self, cell ):
        if not cell:
            return False
        if cell.cellType == "gold" and not ( cell.x, cell.y ) in self.blacklist :
            self.adjacentGold.append( cell )
        elif cell.cellType == "energy" and not ( cell.x, cell.y ) in self.blacklist:
            self.adjacentEnergy.append( cell )
        return not ( cell.x, cell.y ) in self.blacklist and cell.owner != self.game.uid and 0 < cell.takeTime < 4.0

    def FetchInfo( self ):
        self.targets.clear()
        self.adjacentGold.clear()
        self.adjacentEnergy.clear()
        self.emptyEnergy.clear()
        self.emptyGold.clear()
        for x in range(30):
            for y in range(30):
                c = self.game.GetCell(x,y)
                if c.cellType == "gold" and c.owner == 0:
                    self.emptyGold.append( c )
                elif c.cellType == "energy" and c.owner == 0:
                    self.emptyEnergy.append( c )
        for x in range(30):
            for y in range(30):
                # Get a cell
                c = self.game.GetCell(x,y)
                # If the cell I got is mine
                if c.owner == self.game.uid:
                    up, right, down, left = self.GetAdjacent( c )
                    if self.CheckTarget( up ):
                        self.targets.append( up )
                    if self.CheckTarget( right ):
                        self.targets.append( right )
                    if self.CheckTarget( down ):
                        self.targets.append( down )
                    if self.CheckTarget( left ):
                        self.targets.append( left ) 

    def Pursue( self, targets ):
        targetCells = []
        for target in targets:
            for adjacent in self.targets:
                targetCells.append( ( abs( adjacent.x - target.x ) + abs( adjacent.y - target.y ), adjacent ) )
        targetCells.sort( key = lambda tup: ( tup[ 0 ] ) )
        for target in targetCells:
            target = target[ 1 ]
            data = self.game.AttackCell( target.x, target.y )
            while data[ 1 ] == 3:
                data = self.game.AttackCell( target.x, target.y )
            if data[ 0 ]:
                return

    def GameLoop( self ):
        for target in self.adjacentGold:
            data = self.game.AttackCell( target.x, target.y )
            while data[ 1 ] == 3:
                data = self.game.AttackCell( target.x, target.y )
            if data[ 0 ]:
                return
        for target in self.adjacentEnergy:
            data = self.game.AttackCell( target.x, target.y )
            while data[ 1 ] == 3:
                data = self.game.AttackCell( target.x, target.y )
            if data[ 0 ]:
                return
        if len( self.emptyEnergy ) > 0 and self.game.energyCellNum < 1:
            self.Pursue( self.emptyEnergy )
        elif len( self.emptyGold ) > 0:
            self.Pursue( self.emptyGold )
        else:
            for target in self.targets:
                data = self.game.AttackCell( target.x, target.y )
                while data[ 1 ] == 3:
                    data = self.game.AttackCell( target.x, target.y )
                if data[ 0 ]:
                    return

bot = IAiAI()
