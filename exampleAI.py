# You need to import colorfight for all the APIs
import colorfight
import random
from threading import Thread
from math import sqrt

class IAiAI():
    def __init__( self ):
        # Initialize the Panda Colorfight Client
        self.game = cf.Game()
        self.targets = []

        # Attempt to join the game
        if self.game.JoinGame( name ):
            self.game.Refresh()
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

    # Refreshes the Game State
    def Refresh( self ):
        while self.playing:
            self.game.Refresh()
            self.FetchInfo()

    # Runs all base related functions
    def Base( self ):
        while self.playing:
            self.FetchBases()
            try:
                self.BuildLoop()
            except:
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
        return cell.owner != self.game.uid and 0 < cell.takeTime < 4.0

    def FetchInfo( self ):
        self.targets.clear()
        for x in range(30):
            for y in range(30):
                # Get a cell
                c = self.game.GetCell(x,y)
                # If the cell I got is mine
                if c.owner == g.uid:
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

if __name__ == '__main__':
    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit. 
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    while g.currTime < g.planStartTime:
        g.Refresh()
    if g.JoinGame('MyAI'):
        # Put you logic in a while True loop so it will run forever until you 
        # manually stop the game
        while True:
            # Use a nested for loop to iterate through the cells on the map
            
    else:
        print("Failed to join the game!")
