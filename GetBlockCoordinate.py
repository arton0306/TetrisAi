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
    tetrisCandidateZone = ( 387, 457 )  # at rent home, ubuntu15.04, firefox, 1920*1080
    tetrisCandidateZone = ( 396, 551 )  # at rent home, ubuntu15.04, firefox, 1920*1080, tune page
    # width and height
    zoneWH = 30

    im = ImageGrab.grab(
        ( tetrisCandidateZone[0],
          tetrisCandidateZone[1],
          tetrisCandidateZone[0] + zoneWH,
          tetrisCandidateZone[1] + zoneWH )
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



