//#include <SDKDDKVer.h>
//#include <Windows.h>
#include <stdio.h>

#include "core/version.hpp"

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#ifdef _DEBUG
	#pragma comment(lib, "opencv_core231d.lib")
	#pragma comment(lib, "opencv_gpu231d.lib")
	#pragma comment(lib, "opencv_imgproc231d.lib")
	#pragma comment(lib, "opencv_highgui231d.lib")
#else
	#pragma comment(lib, "opencv_core231d.lib")
	#pragma comment(lib, "opencv_gpu231.lib")
	#pragma comment(lib, "opencv_imgproc231.lib")
	#pragma comment(lib, "opencv_highgui231.lib")
#endif

int main(int argc, char* argv[])
{
	cv::Mat image;
	cv::VideoCapture capture;
	capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);
	capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);
	capture.open(0);

	while(true) {
		capture >> image;
		cv::imshow("test", image);

		int c = cv::waitKey(10);
		if (c == 27) break;
	}

	return 0;
}
