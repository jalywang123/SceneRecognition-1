#include "common_functions.h"
#include <opencv2/ml.hpp>
#include <iomanip>

using namespace cv::ml;

const string image_path = "\\\\ws-qvl016\\Frames - Hong Kong HD\\Happy Valley\\20150617\\17Jun race01\\";
const string image_path_test = "C:\\Users\\Johnny\\Desktop\\video_test\\";

int main(int argc, const char** argv){
	//read json file and construct testing matrix
	if (argc < 1){
		cout << "Usage: testVideo.cpp <svm.xml>" << endl;
		return 0;
	}

	const string svm_file = argv[1];
	//define test data mat and test label mat
	Mat testData;
	int descsize = cal_descriptor_size();

	//iterate over the video folder
	int i = 0;
	while (i != 1800){
		ostringstream image_num;
		image_num << setfill('0') << setw(6) << i;
		string img = image_path + "img" + image_num.str() + ".jpg";
		//extract image feature and store it in Mat
		float* result = calc_gist_feature(img, nblocks, nscales, orientationsPerScale);
		Mat tmp_img = Mat(1, descsize, CV_32FC1, result);
		testData.push_back(tmp_img);
		++i;
	}

	cout << endl << "i = " << i << endl;

	//print out test set size
	cout << endl << "Size of testing data = " << testData.size() << endl;

	//load svm from xml
	cout << endl << "Loading SVM Model......" << endl;
	Ptr<SVM> svm = SVM::create();
	svm = StatModel::load<SVM>(svm_file);
	cout << endl << "Successfully loaded SVM Model......" << endl;

	//making predictions
	for (int j = 0; j < testData.rows; ++j){
		Mat sampleMat = testData.row(j);
		//cout << endl << "Size of sampleMat data = " << sampleMat.size() << endl;
		//cout << endl << "sampleMat = " << sampleMat << endl;
		//cout << endl << svm->getVarCount() << endl;
		float response = svm->predict(sampleMat);

		ostringstream image_num;
		image_num << setfill('0') << setw(6) << j;
		string img = image_path + "img" + image_num.str() + ".jpg";
		Mat tmp_img = imread(img);
		
		ostringstream ss;
		ss << response;
		string res(ss.str());
		
		putText(tmp_img, res, Point(100, 100), 0, 5.1, Scalar(255, 255, 0), 4);
		imshow("Image-" + image_num.str() ,tmp_img);
		waitKey(0);
		destroyWindow("Image-" + image_num.str());
	}

	return 0;

}