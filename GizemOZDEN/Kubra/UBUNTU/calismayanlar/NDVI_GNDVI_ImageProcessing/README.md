# Image Processing of Plant Images

## Introduction
Vertical Farming is a revolutionized farming method that produces high quality crops without the relying on favorable weather, skilled labor, high quality soil along with abundant amount of water and area of land. The introduction of vertical farming into the agriculture scene has addressed the major shortcomings of conventional farming methods, while offering a modern, efficient and economically feasible solution that can be implemented in large cities yielding high quality crops.

Although vertical farming seems to be advantageous, there are additional artificial intelligence  can be integrated  to the develop an ability to monitor-control- understand the natural dynamics involved during a growth cycle of a plant.

This is where the concept of incorporating machine learning into vertical farming sounds very promising since machine learning could be used to optimize the vertical farming methods with useful monitoring data.

<img width="517" alt="Image_1" src="https://user-images.githubusercontent.com/56647167/69622202-f06c8900-1059-11ea-8a06-cd18615a5bdf.png">

State-of-the-art sensors and cameras are used to measure the physical parameters of environment and health of the plant respectively. To take advantage of implementing state-of-the-art machine learning, computer vision algorithms are integrated to extract useful visual information from images with which the machine learning can be used to map the sensor values with the visual plant health index and produce an coherent pattern helping the user to further understand the environment factors effecting the health of the plant and monitor the health of the plant in the plant environment. With the coherent machine learnt pattern, one can not only monitor the growth of the plant, but also forecast the health of the plant under a given plant environmental conditions.

Considering this project involves plants as are main objects, well established measurement parameters like NDVI & GNDVI and other physical properties of the plants like dimensions can be extracted from the image using multispectral cameras shot in different light spectrum bands.

<img width="810" alt="Image_2" src="https://user-images.githubusercontent.com/56647167/69622212-f5c9d380-1059-11ea-89d4-7bff144a839d.png">

---

## Image Pre-Processing 

<img width="515" alt="Image_5" src="https://user-images.githubusercontent.com/56647167/69622320-2873cc00-105a-11ea-81b0-952c1a899b06.png">

1. Processing
* The RAW images are converted into an 8-bit grayscale JPEG image which is then feed into the calibration method to produce a reflectance calibrated image.

<img width="500" alt="Image_4" src="https://user-images.githubusercontent.com/56647167/69622318-27429f00-105a-11ea-8563-7018ac3c0829.png">

2. Calibarated
* The process of transforming the pixel values would produce a near perfect RGN (RED – GREEN - NIR) image in the respective surrounding environment which can now be used to generate the NDVI, GNDVI and physical dimensions of the plant using computer vision algorithms.

<img width="500" alt="Image_3" src="https://user-images.githubusercontent.com/56647167/69622316-26117200-105a-11ea-8a96-0166a9efcc92.png">

3.  Image Segmentation
* The plants/leafs are segmented from the environment to precise draw the edges of the plant/leafs of the plant to accurately evaluate the dimensions, NDVI & GNDVI values of the plant only by subtracting the background of the image.



## Calculating the Vegetation Index

Normalized Difference Vegetation Index (NDVI) is a graphical indicator which visually indicates the presence of vegetation in the area of object under observation.

NDVI is calculated from these individual measurements as follows: –

<img width="180" alt="Image_12" src="https://user-images.githubusercontent.com/56647167/69622347-3590bb00-105a-11ea-863a-939b04ef731f.png">

where RED and NIR stand for the spectral reflectance measurements acquired in the red and near-infrared regions, respectively. NDVI itself thus varies between -1.0 and +1.0.

NDVI-RESULT

<img width="493" alt="Image_10" src="https://user-images.githubusercontent.com/56647167/69622338-31649d80-105a-11ea-8891-bca30f68f499.png">

Green-Normalized Difference Vegetation Index is also graphical indicator and a slightly modified version of NDVI which uses the Green and Near-infrared (NIR) spectrum of light of the light rather than the conventional Red and Near-infrared (NIR) spectrum of light. The following is the formulation to estimate the GNDVI of the area under observational.

<img width="180" alt="Image_11" src="https://user-images.githubusercontent.com/56647167/69622343-332e6100-105a-11ea-90c5-8503e66fe494.png">

GNDVI-RESULT

<img width="493" alt="Image_9" src="https://user-images.githubusercontent.com/56647167/69622338-31649d80-105a-11ea-8891-bca30f68f499.png">


### FINAL RESULT

<img width="800" alt="Image_5" src="https://user-images.githubusercontent.com/56647167/69622322-2a3d8f80-105a-11ea-9f26-ea349e788023.png">



## Segmenting and Calculating the Dimensions of the Plant

<img width="515" alt="Image_8" src="https://user-images.githubusercontent.com/56647167/69622328-2f024380-105a-11ea-8eda-dff4673d127f.png">

Once the contour maps are generated, the contour map is used to calculate the edges that are detected in the contour maps using OpenCV library’s measuring tools to get a good approximated dimension calculation.

<img width="335" alt="Image_13" src="https://user-images.githubusercontent.com/56647167/69622351-36c1e800-105a-11ea-9b61-82be7ce85074.png">


The contour maps were generated from the segmented image, the Distance of the contours are measured in pixels’ unit. To convert the measurements units from pixels to a desired unit (like inches), a test image of an object with predetermined dimensions (like a coin) should be taken from a stationary angle. Once the test image taken, test image is used for calculating the unit conversion factor to convert the units from pixels to any desired unit (like inches).


<img width="618" alt="Image_7" src="https://user-images.githubusercontent.com/56647167/69622324-2dd11680-105a-11ea-8e8d-c0aa10e7800c.png">
