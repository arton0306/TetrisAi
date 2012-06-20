import time
import win32api
import win32con

class KeyBoardSimulator:
    def __init__( self ):
        self._keyPressedSec = 0.13
        self._between2KeySec = 0.11

    def SendKey( self, aKey ):
        self.printKey( aKey )
        win32api.keybd_event( aKey, 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
        time.sleep( self._keyPressedSec )
        win32api.keybd_event( aKey, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
        time.sleep( self._between2KeySec )

    def printKey( self, aKey ):
        keyList = [ord('X'), ord('Z'), ord('C'), 0x20, 0x27, 0x25]
        keyName = [ "X", "Z", "C", "Space", "Right", "Left" ]
        print keyName[keyList.index(aKey)]

    def RotateRight( self ):
        self.SendKey( ord('X') )

    def RotateLeft( self ):
        self.SendKey( ord('Z') )

    def HoldBlock( self ):
        self.SendKey( ord('C') )

    def FallInstantly( self ):
        self.SendKey( 0x20 )

    def MoveRight( self ):
        self.SendKey( 0x27 )

    def MoveLeft( self ):
        self.SendKey( 0x25 )

    def MoveLeftMulti( self, count ):
        for i in xrange( count ):
            self.MoveLeft()

    def MoveRightMulti( self, count ):
        for i in xrange( count ):
            self.MoveRight()

    def RotateRightMulti( self, count ):
        if count < 3:
            for i in xrange( count ):
                self.RotateRight()
        else: # count == 3
            self.RotateLeft()

if __name__ == '__main__':
    time.sleep(3)
    """
    "X CZC"
    keyBoard = KeyBoardSimulator()
    keyBoard.RotateRight()
    keyBoard.SendKey( 0x20 )
    keyBoard.RotateLeft()
    keyBoard.MoveLeft()
    keyBoard.HoldBlock()
    keyBoard.MoveRight()
    keyBoard.HoldBlock()
    """

    keyBoard = KeyBoardSimulator()
    cmdOrder = [keyBoard.MoveLeft, keyBoard.MoveLeft, keyBoard.MoveLeft, keyBoard.FallInstantly]
    #cmdOrder = [ keyBoard.FallInstantly ]
    for i in range(100):
        keyBoard.MoveLeftMulti(3)
        keyBoard.FallInstantly()
