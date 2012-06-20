import ImageGrab
import time

class BlockFetcher:
    # (x, y) The position measure by opening tetrix_battle in firefox
    # put the window to left-hand-side and scroll to top
    #CANDIDATE_POINT = ( 340, 525 )
    # block RGB at CANDIDATE_POINT
    #BLOCK_N = (208, 80, 102)
    #BLOCK_S = (76, 159, 48)
    #BLOCK_I = (38, 136, 165)
    #BLOCK_O = (192, 142, 36)
    #BLOCK_T = (166, 59, 163)
    #BLOCK_J = (53, 95, 178)
    #BLOCK_L = (204, 116, 58)

    # (x, y) The position measure by opening tetrix_battle in chrome
    # put the window to left-hand-side and scroll to top

    # at home
    # CANDIDATE_POINT = ( 342, 514 )
    BLOCK_N = ( 254, 65, 104)
    BLOCK_I = ( 44, 200, 249)
    BLOCK_L = ( 255, 140, 48)
    BLOCK_O = ( 255, 221, 63)
    BLOCK_J = ( 72, 113, 238)
    BLOCK_T = ( 219, 80, 184)
    BLOCK_S = ( 134, 221, 41)

    # at work
    CANDIDATE_POINT = ( 338, 525 )
    BLOCK_I = ( 60, 152, 171)
    BLOCK_O = ( 204, 165, 65)

    # error tolerant
    ERROR = 3

    def __init( self ):
        pass

    def isWithinRGB( self, standardRGB, inputRGB, error ):
        for i in range(3):
            if abs( standardRGB[i] - inputRGB[i] ) > error:
                return False
        else:
            return True

    def getRgbOnScreen( self, x, y ):
        im = ImageGrab.grab( ( x, y, x + 1, y + 1 ) )
        pix = im.load()
        return pix[0, 0]

    def getBlockName( self ):
        rgb = self.getRgbOnScreen( BlockFetcher.CANDIDATE_POINT[0], BlockFetcher.CANDIDATE_POINT[1] )
        print rgb
        if self.isWithinRGB( BlockFetcher.BLOCK_N, rgb, BlockFetcher.ERROR):
            return "N"
        elif self.isWithinRGB( BlockFetcher.BLOCK_S, rgb, BlockFetcher.ERROR):
            return "S"
        elif self.isWithinRGB( BlockFetcher.BLOCK_I, rgb, BlockFetcher.ERROR):
            return "I"
        elif self.isWithinRGB( BlockFetcher.BLOCK_O, rgb, BlockFetcher.ERROR):
            return "O"
        elif self.isWithinRGB( BlockFetcher.BLOCK_T, rgb, BlockFetcher.ERROR):
            return "T"
        elif self.isWithinRGB( BlockFetcher.BLOCK_J, rgb, BlockFetcher.ERROR):
            return "J"
        elif self.isWithinRGB( BlockFetcher.BLOCK_L, rgb, BlockFetcher.ERROR):
            return "L"
        else:
            return None

if __name__ == '__main__':
    blockfetch = BlockFetcher()
    time.sleep(1)
    for i in range(30):
        time.sleep(2)
        print blockfetch.getBlockName()
