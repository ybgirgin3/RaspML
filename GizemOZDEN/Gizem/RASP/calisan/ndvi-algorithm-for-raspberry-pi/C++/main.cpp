/*
 * Author: Maik Basso
 * Email: maik@maikbasso.com.br
 * 
 * To compile: 
 * g++ main.cpp -o  main -I/usr/local/include/ -lraspicam -lraspicam_cv -lopencv_core -lopencv_highgui
 *
 * */
#include <ctime>
#include <iostream>
#include <raspicam/raspicam_cv.h>

using namespace std;
 
int main () {
    raspicam::RaspiCam_Cv Camera;
    cv::Mat frame, ndvi, top, bottom;
    double cumulativeNdvi, averageNdvi;
    
    //set camera params
    int resolution[][2] = {{1920,1080},{1336,768},{1280,720},{1024,768},{800,600},{640,480},{320,240},{160,120},{100,133}};
    int resolutionNumber = 8;
    Camera.set(CV_CAP_PROP_FORMAT, CV_8UC3);   
    Camera.set(CV_CAP_PROP_FRAME_WIDTH, resolution[resolutionNumber][0]);
    Camera.set(CV_CAP_PROP_FRAME_HEIGHT, resolution[resolutionNumber][1]);
    Camera.set(CV_CAP_PROP_FPS, 60);
    /**
     * Sets a property in the VideoCapture.
    * * 
    * Implemented properties:
    * CV_CAP_PROP_FRAME_WIDTH,CV_CAP_PROP_FRAME_HEIGHT,
    * CV_CAP_PROP_FORMAT: CV_8UC1 or CV_8UC3
    * CV_CAP_PROP_BRIGHTNESS: [0,100]
    * CV_CAP_PROP_CONTRAST: [0,100]
    * CV_CAP_PROP_SATURATION: [0,100]
    * CV_CAP_PROP_GAIN: (iso): [0,100]
    * CV_CAP_PROP_EXPOSURE: -1 auto. [1,100] shutter speed from 0 to 33ms
    * CV_CAP_PROP_WHITE_BALANCE_RED_V : [1,100] -1 auto whitebalance
    * CV_CAP_PROP_WHITE_BALANCE_BLUE_U : [1,100] -1 auto whitebalance
    **/

    //Open camera
    if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
		return -1;
	}
    
	while(true) {
		//start time
		double timerBegin = cv::getTickCount();
		
		//frame capture
        Camera.grab();
        Camera.retrieve(frame);
        
        //frame properties
        int width = frame.size().width;
		int height = frame.size().height;
		
		//initialize variables
		cumulativeNdvi = 0.0;
		averageNdvi = 0.0;
		top = cv::Mat::ones(height, width, CV_32FC1);
		bottom = cv::Mat::ones(height, width, CV_32FC1);
		ndvi = cv::Mat::ones(height, width, CV_32FC1);
        
        //get the image bands
		std::vector<cv::Mat> channels;
        split(frame, channels);
        //b = channels[0];
        //g = channels[1];
        //nir = channels[2];

        //calculate NDVI
        subtract(channels[0], channels[2], top);
		add(channels[0], channels[2], bottom);
		//avoid division by zero in the entire array
		//bottom[bottom == 0] = 0.01
		divide(top, bottom, ndvi);
		//http://stackoverflow.com/questions/12687437/how-to-calculate-and-use-cvmat-mean-value
		//cv::Scalar tempVal = mean(ndvi);
		//float averageNdvi = tempVal.val[0];
		cumulativeNdvi = cv::sum(ndvi)[0];
		averageNdvi = cumulativeNdvi / (width*height);
        
        //total time
        double totalTime = double(cv::getTickCount()-timerBegin)/double(cv::getTickFrequency());
        double fps = (float) ((float)(1)/totalTime);
        
        //statistics
        system("clear");
		cout << "########################################" << endl;
		cout << "######## NDVI C++ by Maik Basso ########" << endl;
		cout << "########################################" << endl << endl;
		cout << "\tFrame size: " << width << "x" << height << endl; 
		cout << "\tPixels per frame: " << (width*height) << endl;
		cout << "\tCumulative NDVI: " << cumulativeNdvi << endl;
		cout << "\tAverage NDVI: " << averageNdvi << endl << endl;
		cout << "########################################" << endl;
		cout << "\tTime per frame: " << totalTime  << " s" << endl;
		cout << "\tFPS: " << fps << endl;
		cout << "########################################" << endl;
		
		//display image
		//cv::imshow("Imagem original", frame);
    }
    
    //stop the camera
    Camera.release();
    
    //save image 
    //cv::imwrite("raspicam_cv_image.jpg",image);
    
    return 0;
}
