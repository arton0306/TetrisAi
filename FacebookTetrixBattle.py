import time
from BlockFetcher import *
from TetrixObject import *
from TetrixAi import *
from TetrixAiMultiBlock import *
from CPKeyBoardSimulator import *

class FacebookTetrixBattle:
    # the column index(from 0) of the most left grid of the block
    hDelta = {}
    hDelta["O"] = ( 4, )
    hDelta["I"] = ( 3, 5 )
    hDelta["N"] = ( 3, 4 )
    hDelta["S"] = ( 3, 4 )
    hDelta["T"] = ( 3, 4, 3, 3 )
    hDelta["J"] = ( 3, 4, 3, 3 )
    hDelta["L"] = ( 3, 4, 3, 3 )

    sKeyBoardSimulator = CPKeyBoardSimulator()

    def __init__( self ):
        pass

    @staticmethod
    def toString():
        print(FacebookTetrixBattle.hDelta)

    @staticmethod
    def fetchBlock():
        block = BlockFetcher().getBlockName()
        if block is None:
            block = TetrixBlock.getRandBlock().getBlockName()
            print("!"*30, "block fetch error! use a rand pseudo block! [%s]" % block)
        return block

    @staticmethod
    def playWithAi():
        tetrixContainer = TetrixContainer()
        tetrixContainer.printContainer()
        ai = TetrixAi()
        blockfetch = FacebookTetrixBattle.fetchBlock()

        time.sleep(1)

        print("-------- Start --------")
        blockGotName = FacebookTetrixBattle.fetchBlock()
        print(" Got Block: " + blockGotName)
        CPKeyBoardSimulator().HoldBlock()
        while ( True ):
            blockMovement = ai.getMovementByAi( tetrixContainer, TetrixBlock( blockGotName ) )
            #blockMovement = ai.getMovementByAi( tetrixContainer, TetrixBlock( "O" ) )
            tetrixContainer.putBlockInContainer( blockMovement.getPutPos() )
            #tetrixContainer.printContainer()
            blockGotName = FacebookTetrixBattle.fetchBlock()
            FacebookTetrixBattle.sendMoveCmd( blockMovement )
            print("-------------------------")
            FacebookTetrixBattle.delayNextBlock( tetrixContainer )
            print(" Got Block: " + blockGotName)

    @staticmethod
    def playWithMultiBlockAi():
        tetrixContainer = TetrixContainer()
        tetrixContainer.printContainer()
        ai = TetrixAiMultiBlock()

        time.sleep(3)
        curBlockName = FacebookTetrixBattle.fetchBlock()
        CPKeyBoardSimulator().HoldBlock()
        print("-------- Start --------")
        while ( True ):
            nextBlockName = FacebookTetrixBattle.fetchBlock()
            print(" Current Block: " + curBlockName + "\tNext Block: " + nextBlockName)
            (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrixContainer, [TetrixBlock( curBlockName ), TetrixBlock( nextBlockName )] )
            tetrixContainer.putBlockInContainer( blockMovement[0].getPutPos() )
            tetrixContainer.printContainer()
            FacebookTetrixBattle.sendMoveCmd( blockMovement[0] )
            curBlockName = nextBlockName
            time.sleep( 0.03 )
            print("-------------------------")

    @staticmethod
    def delayNextBlock( container ):
        if container.lastLineClearCount != 0:
            time.sleep( 0.11 )
        else:
            time.sleep( 0.02 )

    @staticmethod
    def sendMoveCmd( blockMovement ):
        blockName = blockMovement._tetrixBlock.getBlockName()
        fb_block_hDeltaList = FacebookTetrixBattle.hDelta[blockName]
        fb_block_hDelta = fb_block_hDeltaList[blockMovement._rotationCount]

        # in facebook tetrix_battle, the rotation should be first to avoid shift erroneously near border
        # send rotate cmd
        FacebookTetrixBattle.sKeyBoardSimulator.RotateRightMulti( blockMovement._rotationCount )

        # send horizontal shift cmd
        leftMoveCount = fb_block_hDelta - blockMovement._hDelta
        rightMoveCount = -leftMoveCount
        if leftMoveCount >= 0:
            FacebookTetrixBattle.sKeyBoardSimulator.MoveLeftMulti( leftMoveCount )
        else:
            FacebookTetrixBattle.sKeyBoardSimulator.MoveRightMulti( rightMoveCount )

        # debug
        print("leftMoveCount=" + str( leftMoveCount ) + " rotationCount=" + str( blockMovement._rotationCount ))

          # send fall down cmd
        FacebookTetrixBattle.sKeyBoardSimulator.FallInstantly()

if __name__ == '__main__':
    print("The column index(from 0) of the most left grid of the block.")
    for key, value in FacebookTetrixBattle.hDelta.items():
        print(key, value)

    #FacebookTetrixBattle.playWithAi()
    FacebookTetrixBattle.playWithMultiBlockAi()

