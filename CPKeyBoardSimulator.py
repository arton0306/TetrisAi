# CP: cross platform 
# using pyautogui lib to implement keyboard sender

import pyautogui
import time

# screenWidth, screenHeight = pyautogui.size()
# currentMouseX, currentMouseY = pyautogui.position()
# pyautogui.typewrite('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
# pyautogui.keyDown('shift')
# pyautogui.typewrite('under shift...', interval=0.25)
# pyautogui.typewrite(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.keyDown('a')
# time.sleep( 0.13 )
# pyautogui.keyUp('a')

class CPKeyBoardSimulator:
    def __init__( self, pressKeySec = None, gap2KeySec = None, doTimeStamp = True ):
        if pressKeySec is not None:
            self._pressKeySec = pressKeySec
        else:
            self._pressKeySec = 0.13

        if gap2KeySec is not None:
            self._gap2KeySec = gap2KeySec
        else:
            self._gap2KeySec = 0.11

        self.doTimeStamp = doTimeStamp

    def SendKey( self, aKey ):
        if self.doTimeStamp:
            print( "press %5s @ %15.3f" % (aKey, time.time()) )
        pyautogui.keyDown(aKey)
        if self.doTimeStamp:
            print( "press %5s @ %15.3f" % (aKey, time.time()) )
        time.sleep( self._pressKeySec )
        if self.doTimeStamp:
            print( "upkey %5s @ %15.3f" % (aKey, time.time()) )
        pyautogui.keyUp(aKey)
        if self.doTimeStamp:
            print( "upkey %5s @ %15.3f" % (aKey, time.time()) )
        time.sleep( self._gap2KeySec )

    def printKey( self, aKey ):
        keyList = ['x', 'z', 'c', 'space', 'right', 'left']
        keyName = [ "X", "Z", "C", "Space", "Right", "Left" ]
        print(keyName[keyList.index(aKey)])

    def RotateRight( self ):
        self.SendKey('x')

    def RotateLeft( self ):
        self.SendKey('z')

    def HoldBlock( self ):
        self.SendKey('c')

    def FallInstantly( self ):
        self.SendKey('space')

    def MoveRight( self ):
        self.SendKey('right')

    def MoveLeft( self ):
        self.SendKey('left')

    def MoveLeftMulti( self, count ):
        for i in range( count ):
            self.MoveLeft()

    def MoveRightMulti( self, count ):
        for i in range( count ):
            self.MoveRight()

    def RotateRightMulti( self, count ):
        if count < 3:
            for i in range( count ):
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

    keyBoard = CPKeyBoardSimulator(0,0)
    cmdOrder = [keyBoard.MoveLeft, keyBoard.MoveLeft, keyBoard.MoveLeft, keyBoard.FallInstantly]
    #cmdOrder = [ keyBoard.FallInstantly ]
    for i in range(20):
        #keyBoard.MoveLeftMulti(3)
        #keyBoard.RotateRightMulti(2)
        keyBoard.MoveRightMulti(4)
        keyBoard.FallInstantly()
        keyBoard.MoveLeftMulti(3)
        keyBoard.FallInstantly()

