import random
from TetrixObject import *
from Util import *

class TetrixAiMultiBlock:
    def __init__( self ):
        self.defaultPara = [-75.7014380917982, -61.313501642047925, 11.280082197976206, 70, -150.72589775573758, 120.66828636891036, -186.52951417386484, -154.82119481161956]
        #self.defaultPara = [-10, -3, 10, 80, -0.1, 10, -3, 0]
        self.userPara = None
        pass

    # this function will return ( movement, score )
    # where movement is a list of BlockMovement
    # where score is the score of the movement and it is the highest among all possible move
    def getBlockQueueMovementAndScore( self, containerOrigin, tetrixBlockQueue ):
        returnScore = 0

        maxScore = -1000000
        isValidMoveExsit = False

        if len( tetrixBlockQueue ) == 0:
            return ( [], None )
        else:
            returnMove = []
            firstBlockMove = BlockMovement( tetrixBlockQueue[0] )
            for ( aDirection, aFallingBlock ) in enumerate( tetrixBlockQueue[0].getAllDirectionPos() ):
                for hDelta in xrange( containerOrigin.getColumnCount() ):
                    # aFixBlock has 4 point and can not move but fall down
                    aFixBlock = [( row, col + hDelta ) for ( row, col ) in aFallingBlock]
                    putState = containerOrigin.getStateOfFallingBlock( aFixBlock )
                    if putState.isValid():
                        isValidMoveExsit = True
                        containerAfterPut = containerOrigin.getCopyContainer()
                        containerAfterPut.putBlockInContainer( putState.getPos() )
                        ( restMove, restScore ) = self.getBlockQueueMovementAndScore( containerAfterPut, tetrixBlockQueue[1:] )
                        if restScore == None:
                            scoreAtThisPut = self.getScore( containerOrigin, containerAfterPut, True )
                        elif len( tetrixBlockQueue[1:] ) == 0:
                            scoreAtThisPut = self.getScore( containerOrigin, containerAfterPut, True ) + restScore
                        else:
                            scoreAtThisPut = self.getScore( containerOrigin, containerAfterPut, False ) + restScore
                        if scoreAtThisPut > maxScore:
                            firstBlockMove.setRotationCount( aDirection )
                            firstBlockMove.setHorizontalDelta( hDelta )
                            firstBlockMove.setPutPos( putState.getPos() )
                            maxScore = scoreAtThisPut
                            returnMove = [firstBlockMove] + restMove
            if isValidMoveExsit:
                return ( returnMove, maxScore )
            else:
                return ( [], None )

    # the score return is always >= 0
    def getScore( self, containerOrigin, containerAfterPut, isLastBlock ):
        if ( self.userPara == None ):
            para = self.defaultPara
        else:
            para = self.userPara

        # make sure result score >= 0
        score = 1000000000

        # reverse for convenience
        topFilledGrid = [( containerAfterPut.getRowCount() - r ) for r in containerAfterPut.topFilledGridLine]

        # hole
        score += containerAfterPut.holeCount ** 2 * para[0]

        # blockade
        score += containerAfterPut.blockadeCount ** 2 * para[1]

        # clear line
        score += containerAfterPut.lastLineClearCount * para[2]

        # prepare for combo
        score += ( ( sum( topFilledGrid ) - containerAfterPut.holeCount - para[3] ) / 10.0 ) ** 2 * para[4]

        # combo
        score += containerAfterPut.combo ** 4 * para[5]

        # gap
        score += sum( sorted( getGap( topFilledGrid ) )[:-1] ) ** 2 * para[6]

        # last block's combo
        if isLastBlock:
            score += containerAfterPut.combo ** 2 * para[7]

        assert score >= 0

        return score

class Fitness:
    def __init__( self, blockCount, combo ):
        self.blockCount = blockCount
        self.combo = combo

class GeneAlgo:
    def __init__( self, population, aStartGenerationNum = 1, aChoromosomePool = [] ):
        self.generationNum = aStartGenerationNum
        self.population = population # should be 4x
        self.geneCount = len( TetrixAiMultiBlock().defaultPara )
        self.randScopeMin = [ 0,  0,  0, 30,  0,  0,  0,  0]
        self.randScopeMax = [10, 10, 10, 70, 10, 10, 10, 10]
        if aChoromosomePool == []:
            self.currentChromosome = [ [random.uniform( self.randScopeMin[i], self.randScopeMax[i] ) for i in xrange(self.geneCount)] for j in xrange(self.population) ]
            for aChromosome in self.currentChromosome:
                self.fitPhysicalRange( aChromosome )
        else:
            self.currentChromosome = aChoromosomePool

        # for print
        self.fitnessCount = 0

    def fitness( self, aChromosome ):
        self.fitnessCount += 1
        print str( self.fitnessCount ) + " calc fitness of [ ",
        for gene in aChromosome:
            print "%7.3f, " % (float(gene)),
        print " ]"
        blockCount = 2001
        tetrixContainer = TetrixContainer()
        ai = TetrixAiMultiBlock()
        ai.userPara = aChromosome

        # produce block sequence
        inputBlock = []
        for i in xrange( blockCount ):
            inputBlock.append( TetrixBlock.getRandBlock() )

        # play!
        totalCombo = 0
        for i in xrange( blockCount - 1 ):
            (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrixContainer, inputBlock[i:i+2] )
            if score != None:
                tetrixContainer.putBlockInContainer( blockMovement[0].getPutPos() )
                totalCombo += tetrixContainer.combo
            else:
                break

        print "#block:%5d totalcombo:%5d ratio:%5.3f" % ( i, totalCombo, float(totalCombo) / i )
        return Fitness( i, totalCombo )

    def run( self, generationCount ):
        for generationIdx in xrange( generationCount ):
            # fitness: 1st element is blockCount, 2nd is combo
            self.geneFitness = [ self.fitness( self.currentChromosome[i] ) for i in xrange(self.population) ]
            self.outputFitness()
            winnerChromosome = self.selection( self.currentChromosome, self.geneFitness )
            self.produceNextGeneration( winnerChromosome )
            self.generationNum += 1
        self.geneFitness = [ self.fitness( self.currentChromosome[i] ) for i in xrange(self.population) ]
        outputFitness()

    def selection( self, players, fitness ):
        winnerChromosome = []
        for i in xrange( 0, len( players ), 2 ):
            fitness1 = fitness[i]
            fitness2 = fitness[i + 1]
            if fitness1.combo > fitness2.combo:
                winnerChromosome.append( players[i] )
            elif fitness2.combo > fitness1.combo:
                winnerChromosome.append( players[i + 1] )
            elif fitness1.blockCount > fitness2.blockCount:
                winnerChromosome.append( players[i] )
            else:
                winnerChromosome.append( players[i + 1] )
        return winnerChromosome

    def produceNextGeneration( self, winnerChromosome ):
        nextGeneration = []

        random.shuffle( winnerChromosome )
        # clossover
        for i in xrange( 0, len( winnerChromosome ), 2 ):
            # father = winnerChromosome[i]
            # mother = winnerChromosome[i + 1]
            childCount = 2
            for childIdx in xrange( childCount ):
                child = [ winnerChromosome[i + random.randint(0,1)][geneIdx] for geneIdx in xrange( self.geneCount ) ]
                # mutation
                while ( random.random() < 0.65 ):
                    randomGeneIdx = random.randint( 0, self.geneCount - 1 )
                    phase1range = ( self.randScopeMax[randomGeneIdx] - self.randScopeMin[randomGeneIdx] ) / 20.0
                    assert phase1range >= 0
                    child[randomGeneIdx] += random.uniform( -phase1range, phase1range )
                while ( random.random() < 0.30 ):
                    randomGeneIdx = random.randint( 0, self.geneCount - 1 )
                    child[randomGeneIdx] = random.uniform( self.randScopeMin[randomGeneIdx], self.randScopeMax[randomGeneIdx] )
                # fit to physical range
                self.fitPhysicalRange( child )
                nextGeneration.append( child )

        self.currentChromosome = nextGeneration + winnerChromosome
        random.shuffle( self.currentChromosome )

    def outputFitness( self ):
        f = open( "generation_" + str( self.generationNum ) + ".txt", "w" )
        cn = 0
        for chromosome in self.currentChromosome:
            f.write( "[" )
            for gene in chromosome:
                f.write( "%9.3f," % gene )
            f.write( "]    #combo:%5d #block:%5d ratio:%5.3f" % ( self.geneFitness[cn].combo, self.geneFitness[cn].blockCount, float(self.geneFitness[cn].combo)/self.geneFitness[cn].blockCount ) )
            f.write( "\n" )
            cn += 1
        f.close()

    def fitPhysicalRange(self, aChromosome):
        aChromosome[0] = -abs( aChromosome[0] )
        aChromosome[1] = -abs( aChromosome[1] )
        aChromosome[3] = abs( aChromosome[3] )
        aChromosome[3] = max( 30, aChromosome[3] )
        aChromosome[4] = -abs( aChromosome[4] )
        aChromosome[5] = abs( aChromosome[5] )
        aChromosome[6] = -abs( aChromosome[6] )
        aChromosome[7] = abs( aChromosome[7] )

def test():
    tetrixContainer = TetrixContainer()
    tetrixContainer.printContainer()
    ai = TetrixAiMultiBlock()

    # produce block sequence
    inputBlock = []
    for i in xrange( 12000 ):
        inputBlock.append( TetrixBlock.getRandBlock() )

    # play!
    totalCombo = 0
    for i in xrange( 11999 ):
        print "-------------------------"
        print " Got Block: " + inputBlock[i].getBlockName() + "\t Next Block: " + inputBlock[i + 1].getBlockName()
        (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrixContainer, inputBlock[i:i+2] )
        if score != None:
            tetrixContainer.putBlockInContainer( blockMovement[0].getPutPos() )
            tetrixContainer.printContainer()
            tetrixContainer.printContainerState()
            totalCombo += tetrixContainer.combo
        else:
            break
    print "------ Game Over ------"
    print "Combo:" + str(totalCombo)

if __name__ == '__main__':
    isRunGA = True
    if isRunGA:
        algo = GeneAlgo( 48 )
        algo.run( 10000 )
    else:
        test()
