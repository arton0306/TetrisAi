from TetrixObject import *
from Util import *

class TetrixAi:
    def __init__( self ):
        pass

    # if there are not valid move, return None
    def getMovementByAi( self, containerOrigin, tetrixBlock ):
        maxScore = -1000000
        movement = BlockMovement( tetrixBlock )
        isValidMoveExsit = False
        for ( aDirection, aFallingBlock ) in enumerate( tetrixBlock.getAllDirectionPos() ):
            for hDelta in xrange( containerOrigin.getColumnCount() ):
                # aFixBlock has 4 point and can not move but fall down
                aFixBlock = [( row, col + hDelta ) for ( row, col ) in aFallingBlock]
                putState = containerOrigin.getStateOfFallingBlock( aFixBlock )
                if putState.isValid():
                    containerAfterPut = containerOrigin.getCopyContainer()
                    containerAfterPut.putBlockInContainer( putState.getPos() )
                    scoreAtThisPut = self.getScore_BaseAi( containerOrigin, containerAfterPut )
                    isValidMoveExsit = True
                    if scoreAtThisPut > maxScore:
                        movement.setRotationCount( aDirection )
                        movement.setHorizontalDelta( hDelta )
                        movement.setPutPos( putState.getPos() )
                        maxScore = scoreAtThisPut
        if isValidMoveExsit:
            return movement
        else:
            return None

    def getScore_BaseAi( self, containerOrigin, containerAfterPut ):
        score = 0

        # reverse for convenience
        topFilledGrid = [( containerAfterPut.getRowCount() - r ) for r in containerAfterPut.topFilledGridLine]

        # ai by gap
        sortedAbsGap = sorted( getGap( topFilledGrid ) )
        if sortedAbsGap[-2] >= 4 and sortedAbsGap[-1] >= 4:
            score -= 10
            score -= sum( sortedAbsGap[-2:] ) ** 1.1
        score -= getDeviation( topFilledGrid[:-2] ) * 0.35

        # ai by hole
        if containerAfterPut.holeCount >= 1:
            score -= 8
        if containerAfterPut.holeCount >= 2:
            score -= 4
        score -= containerAfterPut.holeCount ** 1.2 * 3

        # ai by blockade
        score -= containerAfterPut.blockadeCount ** 1.5 * 2

        # ai by clear line
        if containerAfterPut.holeCount > 1:
            score += containerAfterPut.lastLineClearCount * 2

        # ai by ready for combo
        if containerAfterPut.holeCount < 2:
            if sum( topFilledGrid[-2:] ) == 0:
                score += 5
            else:
                score -= sum( topFilledGrid[-2:] ) ** 1.3

        # ai by top check
        if max( topFilledGrid ) > 13 and containerAfterPut.holeCount != 0:
            score -= max( topFilledGrid ) * 0.7

        # ai by combo
        if containerAfterPut.filledGridCount > 60:
            score += 10 + containerAfterPut.combo ** 1.5 * 4

        return score

if __name__ == '__main__':
    tetrixContainer = TetrixContainer()
    tetrixContainer.printContainer()
    ai = TetrixAi()

    for i in xrange( 100 ):
        print("-------------------------")
        randBlock = TetrixBlock.getRandBlock()
        print(" Got Block: " + randBlock.getBlockName())
        blockMovement = ai.getMovementByAi( tetrixContainer, randBlock )
        if blockMovement != None:
            tetrixContainer.putBlockInContainer( blockMovement.getPutPos() )
            tetrixContainer.printContainer()
            tetrixContainer.printContainerState()
        else:
            print("------ Game Over ------")
            break
