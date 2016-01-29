import pyscreenshot as ImageGrab
import time

class BlockFetcher:
    # (x, y) The position measure by opening tetris_battle in firefox
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

    # (x, y) The position measure by opening tetris_battle in chrome
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

    # at rent home, ubuntu15.04, firefox, 1920*1080
    CANDIDATE_POINT = ( 387, 457 )
    BLOCK_N = (252, 77, 115)
    BLOCK_I = (45, 210, 255)
    BLOCK_L = (255, 150, 56)
    BLOCK_O = (255, 221, 63)
    BLOCK_J = (75, 123, 242)
    BLOCK_T = (225, 83, 193)
    BLOCK_S = (142, 228, 46)
    # at rent home, ubuntu15.04, firefox, 1920*1080, tune page
    CANDIDATE_POINT = ( 396, 551 )
    BLOCK_O = (204, 165, 65)
    BLOCK_N = (255, 78, 106)
    BLOCK_L = (255, 162, 46)
    BLOCK_S = (142, 238, 53)
    BLOCK_I = (60, 152, 171)
    BLOCK_T = (235, 80, 205)
    BLOCK_J = (72, 131, 255)

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
        # must convert to RGB after grab,
        # because the format of grab is decide by internal algorithm
        # sometimes mode RGB, sometimes mode P (palette)
        im = ImageGrab.grab(bbox=(x, y, x + 1, y + 1)).convert('RGB')
        pix = im.getpixel((0,0))
        return pix

    def getBlockName( self ):
        rgb = self.getRgbOnScreen( BlockFetcher.CANDIDATE_POINT[0], BlockFetcher.CANDIDATE_POINT[1] )
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
            print(rgb, "is not valid block color")
            return None

if __name__ == '__main__':
    blockfetch = BlockFetcher()
    # time.sleep(1)
    for i in range(50):
        # time.sleep(2)
        blockName = blockfetch.getBlockName()
        if blockName is not None:
            print(blockName)
