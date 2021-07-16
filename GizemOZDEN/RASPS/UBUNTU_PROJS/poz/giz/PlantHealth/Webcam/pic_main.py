import numpy as np #arrays and math
import cv2 #opencv library
from NDVI import NDVICalc
from DVI import DVICalc

"""
kullanımı;
    resim için: python3 pic_main.py R 1617856787332-forest-2.jpg
    video için: python3 pic_main.py V
"""



#-------------------------------------------
#----------------Main Function--------------
#-------------------------------------------

def pic(src):
    # read image
    img = cv2.imread(src)

    # resize image
    img = cv2.resize(img, (640,480), cv2.INTER_AREA)

    # get image sizes
    height = img.shape[0]
    width = img.shape[1]


    #Text Related
    x = int(width/2)
    y = int(2*height/3) 
    text_color = (255,255,255) #color as (B,G,R)
    font = cv2.FONT_HERSHEY_PLAIN
    thickness = 2
    font_size = 2.0

    n =  NDVICalc(img)
    d = DVICalc(img)
    cv2.putText(img, "Raw Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
    cv2.putText(n, "NDVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
    cv2.putText(d, "DVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
    new = np.concatenate((n, d, img), axis=1)
    cv2.imshow('img', new)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def vid():
    cv2.namedWindow("preview NDVI")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        height = vc.get(3) #get height
        width = vc.get(4) #get width
        #Text Related
        x = int(width/2)
        y = int(2*height/3) 
        text_color = (255,255,255) #color as (B,G,R)
        font = cv2.FONT_HERSHEY_PLAIN
        thickness = 2
        font_size = 2.0
    else:
        rval = False

    while rval:
        ndviImage = NDVICalc(frame)
        dviImage = DVICalc(frame)

        cv2.putText(frame, "Raw Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
        cv2.putText(ndviImage, "NDVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)
        cv2.putText(dviImage, "DVI Image", (x,y), font, font_size, text_color, thickness, lineType=cv2.LINE_AA)

        newFrame = np.concatenate((ndviImage,dviImage,frame),axis=1)
        cv2.imshow("preview NDVI", newFrame)

        rval, frame = vc.read()

        key = cv2.waitKey(1)&0xFF #get a key press
        if key == ord('q'): #q for quitting
            break
        elif key == ord('p'): #p for printscreen
            curtime = datetime.datetime.now()
            formattedTime = curtime.strftime("%Y%m%d-%H-%M-%S.jpg")
            print('filename:%s' % formattedTime)
            cv2.imwrite(formattedTime,newFrame)
            print("Screenshot taken!")

    # When everything done, release the capture
    vc.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    # eğer eleman girildiyse o girdi resmi var demektir
    if len(sys.argv) > 0:
        if sys.argv[1] == 'R':
            pic(sys.argv[2])

        elif sys.argv[1] == 'V':
            vid()






