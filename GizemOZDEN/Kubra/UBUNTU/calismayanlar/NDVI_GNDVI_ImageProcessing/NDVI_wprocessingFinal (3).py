from scipy.spatial import distance as dist
import sys
from imutils import perspective
from imutils import contours
import numpy as np
import matplotlib.pyplot as plt
import cv2
import imutils
import PIL.Image
import PIL.ExifTags
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import os
import csv
import copy
import sklearn
from sklearn.preprocessing import MinMaxScaler as minmaxscale
#Image Processing : START
BASE_COEFF_SURVEY2_NDVI_JPG = {"red":   {"slope": 6.51199915, "intercept": -0.29870245},
                               "green": {"slope": 1.00, "intercept": 0.00},
                               "blue":  {"slope": 10.30416005, "intercept": -0.65112026}}
BASE_COEFF_SURVEY2_NDVI_TIF = {"red":   {"slope": 1.06087488594, "intercept": 3.21946584661},
                                   "green": {"slope": 1.00, "intercept": 0.00},
                                   "blue":  {"slope": 1.46482226805, "intercept": -43.6505776052}}
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def MetaData(filedirectory,filename):
    img = PIL.Image.open(filedirectory+"/"+filename)
    exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGSvi
    }
    cameramake=exif['ImageDescription']
    cameramake = cameramake.split()
    cameraModel = cameramake[1]
    return(cameraModel)

def preprocessing(filedirectory,rawfilename,filename):
    cameraModel = MetaData(filedirectory,filename)
    if cameraModel == "Survey3":
        try:
            data = np.fromfile(filedirectory+"/"+rawfilename, dtype=np.uint8)
            # data2 = np.fromfile("F:\\DCIM\Photo\\2018_0507_142527_011.RAW", dtype=np.uint8)
            data = np.unpackbits(data)
            # data2 = np.unpackbits(data2)
            datsize = data.shape[0]
            # dat2size = data2.shape[0]
            data = data.reshape((int(datsize / 4), 4))
            temp = copy.deepcopy(data[0::2])
            temp2 = copy.deepcopy(data[1::2])
            data[0::2] = temp2
            data[1::2] = temp
            udata = np.packbits(np.concatenate([data[0::3], np.array([0, 0, 0, 0] * 12000000, dtype=np.uint8).reshape(12000000,4),   data[2::3], data[1::3]], axis=1).reshape(192000000, 1)).tobytes()
            img = np.fromstring(udata, np.dtype('u2'), (4000 * 3000)).reshape((3000, 4000))
        except Exception as e:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           print(str(e) + ' Line: ' + str(exc_tb.tb_lineno))
           oldfirmware = True
    elif(cameraModel == 'Survey2'):
        with open(filedirectory+"/"+rawfilename) as rawimage:
            img = np.fromfile(rawimage, np.dtype('u2'), (4608 * 3456)).reshape((3456, 4608))
    try:
        color = cv2.cvtColor(img, cv2.COLOR_BAYER_RG2RGB).astype("float32")
        plt.figure(30)
        plt.imshow(color)
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # self.PreProcessLog.append(str(e) + ' Line: ' + str(exc_tb.tb_lineno))
        print(str(e) + ' Line: ' + str(exc_tb.tb_lineno))
    redmax = np.percentile(color[:,:,0],98)
    redmin = np.percentile(color[:, :, 0],2)
    print("redmax= '%3f'and redmin = '%3f'",redmax,redmin)
    greenmax = np.percentile(color[:, :, 1],98)
    greenmin = np.percentile(color[:, :, 1],2)
    print("greenmax= '%3f'and greenmin = '%3f'",greenmax,greenmin)
    bluemax = np.percentile(color[:, :, 2],98)
    bluemin = np.percentile(color[:, :, 2],2)
    print("bluemax= '%3f'and bluemin = '%3f'",bluemax,bluemin)
    # color = cv2.merge((color[:,:,0],color[:,:,2],color[:,:,1])).astype(np.dtype('u2'))
    color[:,:,0] = (((color[:,:,0] - redmin) / (redmax - redmin)))
    color[:,:,2] = (((color[:,:,2] - bluemin) / (bluemax - bluemin)))
    color[:,:,1] = (((color[:,:,1] - greenmin) / (greenmax - greenmin)))
    print("BEFORE \n")
    print("color max is", color.max())
    print("\n color min is", color.min())
    print("\n color mean and std is",color.mean(),color.std())
    color[color > 1.0] = 1.0
    color[color < 0.0] = 0.0
    color= cv2.normalize(color.astype("float"), None, 0.0, 1.0, cv2.NORM_MINMAX)
    print("After \n")
    print("color max is", color.max())
    print("\n color min is", color.min())
    print("\n color mean and std is",color.mean(),color.std())
    color = color * 255.0
    color = color.astype("uint8")
#    color = cv2.bitwise_not(color)
    print("After * 255 \n")
    print("color max is", color.max())
    print("\n color min is", color.min())
    print("\n color mean and std is",color.mean(),color.std())
    cv2.imencode(".jpg", color)
#    cv2.cvtColor(color,cv2.COLOR_BGR2RGB)
    names = rawfilename.split('.')
    outputfilename = processed_newpath+"/"+names[0]+"_Processed.jpg"
    name = names[0]+"_Processed.jpg"
#    color = cv2.cvtColor(color,cv2.COLOR_BGR2RGB)
    cv2.imwrite(outputfilename,color)
    return(outputfilename,name)

def imageResize(x,y,filedir=None,filename=None,img = None):
    img = Image.open(filename)
    print("Image was provided")
    img_resized= img.resize((x,y), Image.ANTIALIAS)
    new_filename = filedir+'\Image_scaled.jpg'
    img_resized.save(new_filename, optimize = True, quality = 95)
    return(new_filename)

def segmentImage(x1,y1,x2,y2,img,num=5):
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    w = len(img[0])
    h = len(img)
    x= int(x1*w)
    y = int(y1*h)
    a = int(x2*w)
    b = int(y2*h)
    rect = (x,y,a,b)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,num,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img2 = img*mask2[:,:,np.newaxis]
    cv2.imwrite(filedir+"/segmented_image.JPG",img2)
    return (img2,(filedir+"/segmented_image.JPG"))

def datatype (image):
    if (image.dtype == 'uint8'):
        return (0)
    elif (image.dtype == 'uint16'):
       return (1)
    else:
       print("Couldnt recognize the datatype of the Image")

def pixels(image):
    ndvi_pixels = []
    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(len(image[0][0])):
                if (image[i,j,k]!=0):
                    ndvi_pixels.append([i,j])
    return(ndvi_pixels)


def ndvi_calculations(pixels_image,image):
    ndvi_calc = 0
    denom_ndvi_calc = 1
    for i,j in (pixels_image):
        ndvi_calc += image[i][j]
        denom_ndvi_calc +=1
    ndvi_avg = ndvi_calc/denom_ndvi_calc
    return(ndvi_avg/255.0)

def calculateIndex(image,x,y):
    img_NDVI = image
    bands = [img_NDVI[:,:,0],img_NDVI[:,:,1],img_NDVI[:,:,2]]
    red = bands[2]
    green = bands[1]
    nir = bands[0]
    index = datatype(img_NDVI)
    if (index == 0):
        nir = nir/255
        red = red/255
        green = green/255
        if ((x == "Red" or  x =="red") and (y == "nir" or  y == "NIR")):
            numer = nir-red
            denom = nir+red
            denom[denom == 0] = 0.01
            ndvi = numer/denom
            ndvi -= ndvi.min()
            ndvi /= ndvi.max()
            ndvi *= 255.0
            ndvi = np.around(ndvi)
            ndvi = ndvi.astype("uint8")
            ndvi = cv2.equalizeHist(ndvi)
            return(ndvi)
        elif ((x== "Green" or x=="green") and (y=="nir" or y =="NIR")):
            numer = nir-green
            denom = nir+green
            denom[denom == 0] = 0.01
            gndvi = numer/denom
            gndvi -= gndvi.min()
            gndvi /= gndvi.max()
            gndvi *= 255.0
            gndvi = np.around(gndvi)
            gndvi = gndvi.astype("uint8")
            gndvi = cv2.equalizeHist(gndvi)
            return(gndvi)
    elif (index == 1):
        nir = nir/65535.0
        red = red/65535.0
        green = green/65535.0
        if ((x == "Red" or  x =="red") and (y == "nir" or  y == "NIR")):
            numer = nir-red
            denom = nir+red
            denom[denom == 0] = 0.01
            ndvi = numer/denom
            ndvi -= ndvi.min()
            ndvi /= ndvi.max()
            ndvi *= 65535.0
            ndvi = np.around(ndvi)
            ndvi = ndvi.astype("uint16")
            ndvi = cv2.equalizeHist(ndvi)
            return (ndvi)
        elif ((x=="Green" or x =="green") and (y == "NIR" or y =="nir")):
            numer = nir-green
            denom = nir+green
            denom[denom == 0] = 0.01
            gndvi = numer/denom
            gndvi -= gndvi.min()
            gndvi /= gndvi.max()
            gndvi *= 65535.0
            gndvi = np.around(gndvi)
            gndvi = gndvi.astype("uint16")
            gndvi = cv2.equalizeHist(gndvi)
            return (gndvi)

print ("Index is calculated")

def calibrate(multiple,values):
    slope = multiple["slope"]
    intercept = multiple["intercept"]
    return int((slope*values) + intercept)

def calibration(filename,name,pixel_min_max):
    img = cv2.imread(filename,-1)
    bands = [img[:,:,0],img[:,:,1],img[:,:,2]]
    blue = bands[0]
    green = bands[1]
    red = bands[2]
    base_coef = BASE_COEFF_SURVEY2_NDVI_JPG
    pixel_min_max["redmax"] = max(red.max(),pixel_min_max["redmax"])
    pixel_min_max["redmin"] = min(red.min(),pixel_min_max["redmin"])
    pixel_min_max["greenmax"] = max(green.max(),pixel_min_max["greenmax"])
    pixel_min_max["greenmin"] = min(green.min(),pixel_min_max["greenmin"])
    pixel_min_max["bluemax"] = max(blue.max(),pixel_min_max["bluemax"])
    pixel_min_max["bluemin"] = min(blue.min(),pixel_min_max["bluemin"])
    min_max_list = ["redmax", "redmin", "bluemin", "bluemax"]
    for min_max in min_max_list:
        if len(min_max) == 6:
            color = min_max[:3]
        elif len(min_max) == 7:
            color = min_max[:4]
        else:
            color = min_max[:5]
        pixel_min_max[min_max] = calibrate(base_coef[color],pixel_min_max[min_max])
    red = ((red * base_coef["red"]["slope"]) + base_coef["red"]["intercept"])
    green = ((green * base_coef["green"]["slope"]) + base_coef["green"]["intercept"])
    blue = ((blue * base_coef["blue"]["slope"]) + base_coef["blue"]["intercept"])
    maxpixel = pixel_min_max["redmax"] if pixel_min_max["redmax"] > pixel_min_max["bluemax"] else pixel_min_max["bluemax"]
    minpixel = pixel_min_max["redmin"] if pixel_min_max["redmin"] < pixel_min_max["bluemin"] else pixel_min_max["bluemin"]
    red = ((red - minpixel) / (maxpixel - minpixel))
    green = ((green - minpixel) / (maxpixel - minpixel))
    blue = ((blue - minpixel) / (maxpixel - minpixel))
    red *= 255
    green *= 255
    blue *= 255
    red = red.astype(int)
    green = green.astype(int)
    blue = blue.astype(int)
    red = red.astype("uint8")
    green = green.astype("uint8")
    blue = blue.astype("uint8")
    refimg = cv2.merge((blue,green,red))
    names = filename.split('.')
    cv2.imwrite(calibrated_newpath+"/"+name+"_Calibrated.jpg",refimg)
    return(calibrated_newpath+"/"+name+"_Calibrated.jpg")

def measuredistance(imgs,imgo,filedir,filename):
    img_contour = imgs.copy()
    img_contour = cv2.cvtColor(img_contour,cv2.COLOR_BGR2GRAY)
    img_contour = cv2.GaussianBlur(img_contour,(1,1),0)
    edges = cv2.Canny(img_contour,0,100,3)
    edges = cv2.dilate(edges,None,iterations = 5)
    edges = cv2.erode(edges,None,iterations = 5)
    plt.figure(1)
    plt.imshow(edges)
    ret,thresh = cv2.threshold(edges,130,255,0)
    image,img_contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    img_dcontour = imgo.copy()
    for c in img_contours:
        x = cv2.contourArea(c)
        if x > 1:
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            img_dcontour= cv2.drawContours(img_dcontour,[box.astype("int")],-1,(255,0,0), 3)
        pixelsPerMetric = None
        for (x,y) in box:
                cv2.circle(img_dcontour,(int(x),int(y)),5 , (0,255,0),-1)
	# unpack the ordered bounding box, then compute the midpoint
	# between the top-left and top-right coordinates, followed by
	# the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

	# compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

	# draw the midpoints on the image
        cv2.circle(img_dcontour, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(img_dcontour, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(img_dcontour, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(img_dcontour, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	# draw lines between the midpoints
        cv2.line(img_dcontour, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
	(255, 0, 255), 2)
        cv2.line(img_dcontour, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
	(255, 0, 255), 2)
        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
	# if the pixels per metric has not been initialized, then
	# compute it as the ratio of pixels to supplied metric
    	# (in this case, inches)
        if pixelsPerMetric is None:
            pixelsPerMetric = 500

        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

    	# draw the object sizes on the image
        cv2.putText(img_dcontour, "{:.1f}in".format(dimA),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
        cv2.putText(img_dcontour, "{:.1f}in".format(dimB),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
        plt.figure(2)
        plt.imshow(img_dcontour)
        plt.imsave(filedir+"/"+filename+"DistanceMap.JPG",img_dcontour)
        print("the distance of the image was sucessfully measured")
#Image Processing : END
#Start of calling methods

filedir = input("Enter the file directory \n")
files = os.chdir(filedir)
files = os.listdir(filedir)
print("Before sorting", files)
files.sort()
print("after sorting", files)
#files = files[1:]
files_arranged = []
print(files[::2])
rawfiles = files[::2]
jpgfiles = files[1::2]
if(len(rawfiles) == len(jpgfiles)):
	for i in range(len(rawfiles)):
		x=[rawfiles[i],jpgfiles[i]]
		print(x)
		files_arranged.append(x)
print("Files arranged list is", files_arranged,"\n")

processed_newpath = filedir+'/_Processed'
if not os.path.exists(processed_newpath):
    os.makedirs(processed_newpath)

calibrated_newpath = filedir+'/_Calibrate'
if not os.path.exists(calibrated_newpath):
    os.makedirs(calibrated_newpath)

ndvi_newpath = filedir+'/NDVI'
if not os.path.exists(ndvi_newpath):
    os.makedirs(ndvi_newpath)



gndvi_newpath = filedir+'/GNDVI'
if not os.path.exists(gndvi_newpath):
    os.makedirs(gndvi_newpath)


contour_newpath = filedir+'/Contourmaps'
if not os.path.exists(contour_newpath):
    os.makedirs(contour_newpath)

ndvi_avg = []
gndvi_avg = []
for rawfilename, filename in files_arranged:
    pixel_min_max = {"redmax": 0.0, "redmin": 65535.0,
                 "greenmax": 0.0, "greenmin": 65535.0,
                  "bluemax": 0.0, "bluemin": 65535.0}
    pnewfilename = ""
    newfilename = ""
    print("The raw file is",rawfilename+"\n")
    print("the image filename is", filename, "\n")
    pnewfilename,name = preprocessing(filedir,rawfilename,filename)
    print(pnewfilename)
    newfilename = calibration(pnewfilename,name,pixel_min_max)
    newfilePATH = filedir+newfilename
    new_filename = imageResize(1500,1500,filedir,newfilename)
    print("Successfully downsized the image \n")
    img  = cv2.imread(new_filename)
    print("Sucessfully read the image")
    img_seg,new_filename= segmentImage(0.15,0.15,0.85,0.85,img)
    print("Sucessfully segmented the image")
    ndvi = calculateIndex(img, "red", "nir")
    print("Successfully calculated the NDVI of the image")
    gndvi = calculateIndex(img, "green", "nir")
    print("Sucessfully calculated the GNDVI")
    arr = pixels(img_seg)
    print("Sucessfully collected pixel data")
    ndvi_avg_img = ndvi_calculations(arr,ndvi)
    print(ndvi_avg_img)
    ndvi_avg.append(ndvi_avg_img)
    gndvi_avg_img = ndvi_calculations(arr,gndvi)
    print(gndvi_avg_img)
    gndvi_avg.append(gndvi_avg_img)
    plt.imsave(str(ndvi_newpath)+"/"+filename+"NDVI.JPG", ndvi ,cmap = plt.cm.RdYlGn)
    plt.imsave(str(gndvi_newpath)+"/"+filename+"GNDVI.JPG", gndvi, cmap = plt.cm.RdYlGn)
    measuredistance(img_seg,img,contour_newpath,filename)


with open(filedir+"/NDVI.csv","w") as ndvicsv:
    wr = csv.writer(ndvicsv,dialect='excel')
    wr.writerows(map(lambda x: [x], ndvi_avg))

with open(filedir+"/GNDVI.csv","w") as gndvicsv:
    wr = csv.writer(gndvicsv,dialect='excel')
    wr.writerows(map(lambda x: [x], gndvi_avg))

