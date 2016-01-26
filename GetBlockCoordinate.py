import pyscreenshot as ImageGrab
import time

def isWithinRGB( standardRGB, inputRGB, error ):
    for i in range(3):
        if abs( standardRGB[i] - inputRGB[i] ) > error:
            return False
    else:
        return True

def getBlockName():
    # (x, y)
    tetrixCandidateZone = ( 387, 457 )
    # width and height
    zoneWH = 30

    im = ImageGrab.grab(
        ( tetrixCandidateZone[0],
          tetrixCandidateZone[1],
          tetrixCandidateZone[0] + zoneWH,
          tetrixCandidateZone[1] + zoneWH )
        ).convert('RGB')
    f = open( "test" + str( time.time() ) + ".jpg", "wb" )
    im.save( f, "JPEG" )
    f.close()
    pix = im.load()
    print(pix[0, 0])

if __name__ == '__main__':

    time.sleep(1)
    for i in range(30):
        time.sleep(2)
        getBlockName()



