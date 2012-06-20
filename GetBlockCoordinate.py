import ImageGrab
import time

def isWithinRGB( standardRGB, inputRGB, error ):
    for i in range(3):
        if abs( standardRGB[i] - inputRGB[i] ) > error:
            return False
    else:
        return True

def getBlockName():
    # (x, y)
    tetrixCandidateZone = ( 758, 555 )
    # width and height
    zoneWH = 25

    im = ImageGrab.grab(
        ( tetrixCandidateZone[0],
          tetrixCandidateZone[1],
          tetrixCandidateZone[0] + zoneWH,
          tetrixCandidateZone[1] + zoneWH )
        )
    f = open( "test" + str( time.time() ) + ".jpg", "wb" )
    im.save( f, "JPEG" )
    f.close()
    pix = im.load()
    print pix[10, 10]

if __name__ == '__main__':

    time.sleep(1)
    for i in range(30):
        time.sleep(2)
        getBlockName()



