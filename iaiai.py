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
        self.started = False
        self.startCell = (-1, -1)

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
        self.startCell = ( -1, -1 )
        offset = ( 0, 0 )
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
        for x in range( 0, 30 ):
            for y in range( 0, 30 ):
                c = self.game.GetCell( x, y )
                if c.owner == self.game.uid and c.isBase:
                    self.startCell = ( x, y )
        if self.startCell[ 0 ] > 26:
            offset[ 0 ] = ( -2, 0 )
        elif self.startCell[ 0 ] < 3:
            offset[ 0 ] = ( 2, 0 )
        elif self.startCell[ 1 ] > 26:
            offset[ 1 ] = ( 0, -2 )
        elif self.startCell[ 1 ] < 2:
            offset[ 1 ] = ( 0, 1 )
        for temp in heartTemplate:
            self.heartCells.append( ( temp[ 0 ] + offset[ 0 ], temp[ 1 ] + offset[ 1 ] ) )
        building = True
        while building:
            building = False
            for cell in self.heartCells:
                c = self.game.GetCell( cell[ 0 ], cell[ 1 ] )
                if c != None and 0 < c.takeTime < 4 and c.owner != self.game.uid:
                    print( self.game.AttackCell( cell[ 0 ], cell[ 1 ] ) )
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
            #self.FetchBases()
            #try:
            #    self.BuildLoop()
            #except:
            #    pass
            pass

    # Runs all the AI actions
    def Play( self ):
        while self.playing:
            #self.GameLoop()
            print( "game!" )

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
        return cell.owner != self.game.uid and 0 < cell.takeTime < 4.0

    def FetchInfo( self ):
        self.targets.clear()
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

    def GameLoop( self ):
        for target in self.targets:
            data = self.game.AttackCell( target.x, target.y )
            while data[ 1 ] == 3:
                data = self.game.AttackCell( target.x, target.y )

bot = IAiAI()
