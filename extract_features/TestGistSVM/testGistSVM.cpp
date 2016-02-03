#include "GistSVM/gist_svm.h"
#include <iomanip>

using namespace cv;
using namespace std;
using namespace cv::ml;

#pragma comment(lib, "GistSVM.lib")

const string image_path_test = "C:\\Users\\Johnny\\Desktop\\video_test\\";
const string svm_file = "../GistSVM/svm.xml";
const string output_dir = ".\\output";

vector<pair<string, int>> getCSVcontent(istream& str){

	string line;
	vector<pair<string, int>> result;

	while (getline(str, line)) {
		istringstream iss(line);
		string a, b;
		getline(iss, a, ';');
		getline(iss, b);
		pair<string, int> tmp;
		tmp.first = a;
		tmp.second = stoi(b);
		result.push_back(tmp);
	}

	return result;
}



int main(int argc, const char** argv){
	
	//initialize GistSVM class
	GistSVM gsvm;

	//make test data mat
	Mat testData;

	//iterate over the video folder
	int i = 0;
	while (i != 50){
		ostringstream image_num;
		image_num << setfill('0') << setw(6) << i;
		string img = image_path_test + "img" + image_num.str() + ".jpg";
		Mat tmpImg = imread(img);
		//extract image feature and store it in Mat

		int imageChannels = tmpImg.channels();
		assert(imageChannels == 1 || imageChannels == 3);
		int descsize;
		if (imageChannels == 1)
			descsize = gsvm.cal_gray_descriptor_size();
		else
			descsize = gsvm.cal_color_descriptor_size();
		
		float* result = gsvm.calc_gist_feature(tmpImg);
		Mat tmp_img = Mat(1, descsize, CV_32FC1, result);

		testData.push_back(tmp_img);
		++i;
	}

	//print out test set size
	cout << endl << "Size of testing data = " << testData.size() << endl;
	
	//load svm
	gsvm.load_svm_from_file(svm_file);


	//making predictions
	for (int j = 0; j < testData.rows; ++j){
		
		Mat sampleMat = testData.row(j);

		float response = gsvm.predict_mat(sampleMat);

		ostringstream image_num;
		image_num << setfill('0') << setw(6) << j;
		string img = image_path_test + "img" + image_num.str() + ".jpg";
		Mat tmp_img = imread(img);

		ostringstream ss;
		ss << response;
		string res(ss.str());

		putText(tmp_img, res, Point(100, 100), 0, 5.1, Scalar(255, 255, 0), 4);
		imshow("Image-" + image_num.str(), tmp_img);
		waitKey(0);
		destroyWindow("Image-" + image_num.str());
	}

	return 0;

}