import time
from BlockFetcher import *
from TetrisObject import *
from TetrisAi import *
from TetrisAiMultiBlock import *
from CPKeyBoardSimulator import *

class FacebookTetrisBattle:
    # the column index(from 0) of the most left grid of the block
    hDelta = {}
    hDelta["O"] = ( 4, )
    hDelta["I"] = ( 3, 5 )
    hDelta["N"] = ( 3, 4 )
    hDelta["S"] = ( 3, 4 )
    hDelta["T"] = ( 3, 4, 3, 3 )
    hDelta["J"] = ( 3, 4, 3, 3 )
    hDelta["L"] = ( 3, 4, 3, 3 )

    sKeyBoardSimulator = CPKeyBoardSimulator(pressKeySec = 0.0, gap2KeySec = 0.01)

    def __init__( self ):
        pass

    @staticmethod
    def toString():
        print(FacebookTetrisBattle.hDelta)

    @staticmethod
    def fetchBlock():
        block = BlockFetcher().getBlockName()
        if block is None:
            block = TetrisBlock.getRandBlock().getBlockName()
            print("!"*30, "block fetch error! use a rand pseudo block! [%s]" % block)
        return block

    @staticmethod
    def holdBlock():
        print("hold block, not use it instantly")
        FacebookTetrisBattle.sKeyBoardSimulator.HoldBlock()

    @staticmethod
    def playWithAi():
        tetrisContainer = TetrisContainer()
        tetrisContainer.printContainer()
        ai = TetrisAi()
        blockfetch = FacebookTetrisBattle.fetchBlock()

        time.sleep(3)

        print("-------- Start --------")
        blockGotName = FacebookTetrisBattle.fetchBlock()
        print(" Got Block: " + blockGotName)
        FacebookTetrisBattle.holdBlock()
        while ( True ):
            blockMovement = ai.getMovementByAi( tetrisContainer, TetrisBlock( blockGotName ) )
            #blockMovement = ai.getMovementByAi( tetrisContainer, TetrisBlock( "O" ) )
            tetrisContainer.putBlockInContainer( blockMovement.getPutPos() )
            #tetrisContainer.printContainer()
            blockGotName = FacebookTetrisBattle.fetchBlock()
            FacebookTetrisBattle.sendMoveCmd( blockMovement )
            print("-------------------------")
            FacebookTetrisBattle.delayNextBlock( tetrisContainer )
            print(" Got Block: " + blockGotName)

    @staticmethod
    def playWithMultiBlockAi():
        tetrisContainer = TetrisContainer()
        tetrisContainer.printContainer()
        ai = TetrisAiMultiBlock()

        time.sleep(3)
        curBlockName = FacebookTetrisBattle.fetchBlock()
        FacebookTetrisBattle.holdBlock()
        print("-------- Start --------")
        while ( True ):
            nextBlockName = FacebookTetrisBattle.fetchBlock()
            print(" Current Block: " + curBlockName + "\tNext Block: " + nextBlockName)
            aiTimeBeg = time.time()
            (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrisContainer, [TetrisBlock( curBlockName ), TetrisBlock( nextBlockName )] )
            print(" Ai compute time: %f" % (time.time() - aiTimeBeg))
            tetrisContainer.putBlockInContainer( blockMovement[0].getPutPos() )
            tetrisContainer.printContainer()
            FacebookTetrisBattle.sendMoveCmd( blockMovement[0] )
            curBlockName = nextBlockName
            FacebookTetrisBattle.delayNextBlock( tetrisContainer )
            print("-------------------------")

    @staticmethod
    def delayNextBlock( container ):
        if container.lastLineClearCount != 0:
            print("%d lines cleared!" % container.lastLineClearCount)
            time.sleep( 0.5 )
        else:
            time.sleep( 0.00 )

    @staticmethod
    def sendMoveCmd( blockMovement ):
        blockName = blockMovement._tetrisBlock.getBlockName()
        fb_block_hDeltaList = FacebookTetrisBattle.hDelta[blockName]
        fb_block_hDelta = fb_block_hDeltaList[blockMovement._rotationCount]

        # in facebook tetris_battle, the rotation should be first to avoid shift erroneously near border
        # send rotate cmd
        FacebookTetrisBattle.sKeyBoardSimulator.RotateRightMulti( blockMovement._rotationCount )

        # send horizontal shift cmd
        leftMoveCount = fb_block_hDelta - blockMovement._hDelta
        rightMoveCount = -leftMoveCount
        if leftMoveCount >= 0:
            FacebookTetrisBattle.sKeyBoardSimulator.MoveLeftMulti( leftMoveCount )
        else:
            FacebookTetrisBattle.sKeyBoardSimulator.MoveRightMulti( rightMoveCount )

        # debug
        print("leftMoveCount=" + str( leftMoveCount ) + " rotationCount=" + str( blockMovement._rotationCount ))

          # send fall down cmd
        FacebookTetrisBattle.sKeyBoardSimulator.FallInstantly()

if __name__ == '__main__':
    print("The column index(from 0) of the most left grid of the block.")
    for key, value in FacebookTetrisBattle.hDelta.items():
        print(key, value)

    #FacebookTetrisBattle.playWithAi()
    FacebookTetrisBattle.playWithMultiBlockAi()

