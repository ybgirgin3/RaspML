#NDVI algorithm for Raspberry Pi

This project provide several implementations of the NDVI real-time algorithm for Raspberry Pi and Raspberry Pi NoIR Camera.

**Note:**

	- All implementations assume that the Raspberry Pi and Pi NoIR Camera are properly configured.
	- This project is being tested with Raspberry Pi 3 and Pi NoIR Camera V1 Rev 1.3.

## Install dependencies:
Execute all the commands below to install the necessary dependencies for all implementations:
 - `$ sudo apt-get update`
 - `$ sudo apt-get upgrade`
 - `$ sudo rpi-update`
 - `$ sudo reboot`
 - `$ sudo apt-get install build-essential git cmake pkg-config`
 - `$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev`
 - `$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`
 - `$ sudo apt-get install libxvidcore-dev libx264-dev`
 - `$ sudo apt-get install libgtk2.0-dev`
 - `$ sudo apt-get install libatlas-base-dev gfortran`
 - `$ sudo apt-get install g++ libopencv-dev python-dev python-numpy python-opencv opencv-docs ffmpeg`

## Using Python algorithm:

Requirements:
  - Python 2.7 or higher;
  - OpenCV 2.4 or higher;
	
Use:
  - Raspberry Pi open the terminal in this folder;
  - Run the command: `$ python Python/main.py`
  
## Using C++ algorithm:

Requirements:
  - OpenCV 2.4 or higher;
  - RaspiCam: C++ API, version 1.3 or higher, can be installed in http://www.uco.es/investiga/grupos/ava/node/40;

Compile:
  - In C++ folder, run the command: `$ g++ main.cpp -o  main -I/usr/local/include/ -lraspicam -lraspicam_cv -lopencv_core -lopencv_highgui`

Use:
  - Raspberry Pi open the terminal in this folder;
  - Run the command: `$ ./C++/main`

## Benchmark
**Python:**
- 12 FPS;
- Resolution: 100x133;

**C++:**
- 20 FPS;
- Resolution: 640x480;
