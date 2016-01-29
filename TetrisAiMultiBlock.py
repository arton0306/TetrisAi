import random
from TetrisObject import *
from Util import *

class TetrisAiMultiBlock:
    def __init__( self ):
        # self.defaultPara = [   -0.903,   -0.027,   93.369,   -3.898,    4.681,  -12.310,    9.983,]

        # from gen100 combo:  683 #block: 1000 ratio:0.683
        self.defaultPara = [   -1.425,    0.035,   73.637,   -5.299,    9.393,  -11.501,    8.674,]
        self.userPara = None

    # this function will return ( movement, score )
    # where movement is a list of BlockMovement
    # where score is the score of the movement and it is the highest among all possible move
    def getBlockQueueMovementAndScore( self, containerOrigin, tetrisBlockQueue ):
        returnScore = 0

        maxScore = -1000000
        isValidMoveExsit = False

        if len( tetrisBlockQueue ) == 0:
            return ( [], None )
        else:
            returnMove = []
            firstBlockMove = BlockMovement( tetrisBlockQueue[0] )
            for ( aDirection, aFallingBlock ) in enumerate( tetrisBlockQueue[0].getAllDirectionPos() ):
                for hDelta in range( containerOrigin.getColumnCount() ):
                    # aFixBlock has 4 point and can not move but fall down
                    aFixBlock = [( row, col + hDelta ) for ( row, col ) in aFallingBlock]
                    putState = containerOrigin.getStateOfFallingBlock( aFixBlock )
                    if putState.isValid():
                        isValidMoveExsit = True
                        containerAfterPut = containerOrigin.getCopyContainer()
                        containerAfterPut.putBlockInContainer( putState.getPos() )
                        ( restMove, restScore ) = self.getBlockQueueMovementAndScore( containerAfterPut, tetrisBlockQueue[1:] )
                        if restScore == None:
                            scoreAtThisPut = self.getScore( containerOrigin, containerAfterPut, True )
                        elif len( tetrisBlockQueue[1:] ) == 0:
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

        # prepare for combo
        score += ( ( sum( topFilledGrid ) - containerAfterPut.holeCount - para[2] ) / 10.0 ) ** 2 * para[3]

        # combo
        score += containerAfterPut.combo ** 4 * para[4]

        # gap
        score += ( sum( getGap( topFilledGrid ) ) * 0.111 ) ** 2 * para[5]

        # last block's combo
        if isLastBlock:
            score += containerAfterPut.combo ** 2 * para[6]

        assert score >= 0

        return score

class Fitness:
    def __init__( self, blockCount, combo ):
        self.blockCount = blockCount
        self.combo = combo

class GeneAlgo:
    def __init__( self, population, aStartGenerationNum = 1, aChoromosomePool = [] ):
        assert population % 4 == 0
        assert len(aChoromosomePool) <= population
        self.generationNum = aStartGenerationNum
        self.population = population # should be 4x
        self.geneCount = len( TetrisAiMultiBlock().defaultPara )
        self.randScopeMin = [-5, -1, 30,-10,  0,-20,  0]
        self.randScopeMax = [ 5,0.4, 99,  0, 20,  0, 20]

        # 1st generation ancestor
        if aChoromosomePool == []:
            self.currentChromosome = [ [random.uniform( self.randScopeMin[i], self.randScopeMax[i] ) for i in range(self.geneCount)] for j in range(self.population) ]
        else:
            self.currentChromosome = aChoromosomePool + [ [random.uniform( self.randScopeMin[i], self.randScopeMax[i] ) for i in range(self.geneCount)] for j in range( population - len( aChoromosomePool ) ) ]

        # for print
        self.fitnessCount = 0

    def fitness( self, aChromosome ):
        self.fitnessCount += 1
        print(str( self.fitnessCount ) + " calc fitness of [ ", end="")
        for gene in aChromosome:
            print("%7.3f, " % (float(gene)), end="")
        print(" ]")
        blockCount = 1002
        tetrisContainer = TetrisContainer()
        ai = TetrisAiMultiBlock()
        ai.userPara = aChromosome

        # produce block sequence
        inputBlock = []
        for i in range( blockCount ):
            inputBlock.append( TetrisBlock.getRandBlock() )

        # play!
        totalCombo = 0
        for i in range( blockCount - 1 ):
            (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrisContainer, inputBlock[i:i+2] )
            if score != None:
                tetrisContainer.putBlockInContainer( blockMovement[0].getPutPos() )
                totalCombo += tetrisContainer.combo
            else:
                break

        print("#block:%5d totalcombo:%5d ratio:%5.3f" % ( i, totalCombo, float(totalCombo) / i ))
        return Fitness( i, totalCombo )

    def run( self, generationCount ):
        for generationIdx in range( generationCount ):
            # fitness: 1st element is blockCount, 2nd is combo
            self.geneFitness = [ self.fitness( self.currentChromosome[i] ) for i in range(self.population) ]
            self.outputFitness()
            winnerChromosome = self.selection( self.currentChromosome, self.geneFitness )
            self.produceNextGeneration( winnerChromosome )
            self.generationNum += 1
        self.geneFitness = [ self.fitness( self.currentChromosome[i] ) for i in range(self.population) ]
        outputFitness()

    def selection( self, players, fitness ):
        winnerChromosome = []
        for i in range( 0, len( players ), 2 ):
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
        for i in range( 0, len( winnerChromosome ), 2 ):
            # father = winnerChromosome[i]
            # mother = winnerChromosome[i + 1]
            childCount = 2
            for childIdx in range( childCount ):
                child = [ winnerChromosome[i + random.randint(0,1)][geneIdx] for geneIdx in range( self.geneCount ) ]
                # mutation
                while ( random.random() < 0.65 ):
                    randomGeneIdx = random.randint( 0, self.geneCount - 1 )
                    phase1range = ( self.randScopeMax[randomGeneIdx] - self.randScopeMin[randomGeneIdx] ) / 20.0
                    assert phase1range >= 0
                    child[randomGeneIdx] += random.uniform( -phase1range, phase1range )
                while ( random.random() < 0.30 ):
                    randomGeneIdx = random.randint( 0, self.geneCount - 1 )
                    child[randomGeneIdx] = random.uniform( self.randScopeMin[randomGeneIdx], self.randScopeMax[randomGeneIdx] )
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

def play():
    tetrisContainer = TetrisContainer()
    tetrisContainer.printContainer()
    ai = TetrisAiMultiBlock()

    # produce block sequence
    inputBlock = []
    for i in range( 2000 ):
        inputBlock.append( TetrisBlock.getRandBlock() )

    # play!
    totalCombo = 0
    for i in range( 1999 ):
        print("-------------------------")
        print(" Got Block: " + inputBlock[i].getBlockName() + "\t Next Block: " + inputBlock[i + 1].getBlockName())
        (blockMovement, score) = ai.getBlockQueueMovementAndScore( tetrisContainer, inputBlock[i:i+2] )
        if score != None:
            tetrisContainer.putBlockInContainer( blockMovement[0].getPutPos() )
            tetrisContainer.printContainer()
            tetrisContainer.printContainerState()
            totalCombo += tetrisContainer.combo
        else:
            break
    print("------ Game Over ------")
    print("Combo:" + str(totalCombo))

if __name__ == '__main__':
    do_train = False
    if not do_train:
        play()
    else:
        g41 = [ [   -1.776,   -0.029,   63.771,   -1.229,    5.137,   -9.339,    9.704,],
                [   -0.948,   -0.029,   64.941,   -3.534,    9.294,  -10.068,    9.695,],
                [   -1.283,   -0.041,   65.158,   -3.534,    5.742,   -9.459,   10.221,],
                [   -1.068,   -0.077,   66.167,   -1.200,    5.029,   -9.776,    9.146,],
                [   -1.043,   -0.041,   64.183,   -3.643,    9.294,   -9.339,    9.704,],
                [   -0.948,   -0.391,   65.299,   -3.788,    9.273,   -9.762,    9.371,],
                [   -1.173,   -0.011,   65.158,   -5.220,    1.407,   -9.389,    9.062,],
                [   -0.948,   -0.029,   54.603,   -3.534,    2.839,   -9.964,    8.910,],
                [   -1.068,   -0.035,   65.158,   -3.534,    9.715,  -10.227,    9.695,],
                [   -0.679,   -7.611,   65.158,   -5.736,    1.407,   -8.145,    9.901,],
                [   -1.043,   -0.029,   64.941,   -3.534,    9.294,  -10.068,    9.695,],
                [   -1.776,   -0.029,   54.603,   -1.229,    5.137,   -9.770,    9.676,],
                [   -1.213,   -0.041,   54.603,   -3.534,    5.571,   -9.770,    9.704,],
                [   -1.776,   -0.319,   64.183,   -1.200,    5.293,   -9.339,    8.875,],
                [   -0.948,   -0.029,   65.659,   -3.534,    5.794,   -9.770,    9.676,],
                [   -1.043,   -0.041,   64.183,   -3.643,    9.294,   -9.339,    9.704,],
                [   -1.067,   -0.086,   65.055,   -3.711,    5.449,   -9.788,    9.704,],
                [   -1.068,   -0.035,   65.158,   -6.285,    9.715,   -9.551,    9.704,],
                [   -1.213,   -0.011,   64.941,   -3.534,    9.423,   -9.770,    9.588,],
                [   -1.043,   -0.041,   54.603,   -3.534,    9.294,   -9.770,    9.810,],
                [   -1.043,   -0.035,   64.941,   -6.213,    9.418,   -9.551,    9.062,],
                [   -0.450,   -0.173,   64.202,   -4.044,    9.605,   -9.551,   10.004,],
                [   -0.450,   -0.009,   65.158,   -3.707,    9.294,   -9.770,   10.217,],
                [   -1.173,   -0.035,   64.941,   -6.213,    1.407,   -9.389,    9.062,],
                [   -1.403,   -0.011,   54.603,   -3.534,    2.392,   -9.770,    9.676,],
                [   -1.043,   -0.029,   64.941,   -3.534,    9.294,  -10.068,    9.695,],
                [   -1.068,   -0.173,   65.158,   -3.707,    9.605,   -9.551,    9.676,],
                [   -2.014,   -0.041,   67.284,   -3.643,    9.294,   -7.555,    7.795,],
                [   -1.283,   -0.160,   64.183,   -3.643,    5.742,   -9.762,    9.704,],
                [   -1.067,   -0.029,   64.941,   -3.534,    5.137,  -10.227,    9.695,],
                [   -1.173,   -0.011,   65.158,   -4.448,    5.449,   -9.389,    9.062,],
                [   -1.776,   -0.041,   64.183,   -3.643,    9.294,   -9.762,    9.704,],
                [   -5.683,   -0.107,   64.941,   -6.213,    9.418,   -9.389,    9.062,],
                [   -1.066,   -0.011,   53.446,   -3.951,    9.423,  -10.325,    9.676,],
                [   -1.173,   -0.035,   35.108,   -6.213,    1.407,   -4.629,    9.062,],
                [   -1.776,   -0.029,   54.603,   -3.534,    2.392,   -9.770,    9.704,],
                [   -2.517,   -0.035,   64.941,   -6.285,    5.137,  -10.227,    9.695,],
                [   -2.014,   -0.011,   67.284,   -3.936,    9.605,   -7.555,    9.676,],
                [   -1.360,   -0.011,   64.941,   -3.951,    9.423,  -10.165,    9.588,],
                [   -1.776,   -0.041,   65.299,   -3.643,    9.294,   -9.762,    9.704,],
                [   -1.068,   -0.035,   65.158,   -6.213,    5.029,   -9.551,    8.875,],
                [   -1.776,   -0.041,   65.158,   -3.643,    9.294,   -9.762,    9.704,],
                [   -1.213,   -0.041,   53.446,   -3.534,    5.742,   -9.770,    9.676,],
                [   -1.043,   -0.041,   54.603,   -3.534,    5.571,   -9.770,    9.704,],
                [   -0.450,   -0.009,   64.202,   -3.707,    9.294,   -9.770,   10.217,],
                [   -0.948,   -0.029,   54.603,   -3.534,    2.839,   -9.964,    8.910,],
                [   -1.043,   -0.041,   46.963,   -3.643,    9.294,   -9.339,    9.676,],
                [   -1.776,   -0.041,   64.183,   -1.200,    5.137,   -9.339,    9.704,], ]
        algo = GeneAlgo( 64, 41, g41 )
        algo.run( 10000 )
