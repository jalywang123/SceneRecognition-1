#include "GistSVM/gist_svm.h"
#include <iomanip>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace cv;
using namespace std;
using namespace cv::ml;
using namespace boost::filesystem;

#pragma comment(lib, "GistSVM.lib")

const string image_path_test = "C:\\Users\\Johnny\\Desktop\\video_test";
const string svm_file = "C:\\Users\\Johnny\\Desktop\\extract_features\\GistSVM\\svm.xml";

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

	int starting_f = 0;
	int finishing_f = 0;
	string image_path = "";
	string output_dir = "";

	if (argc < 3){
		cout << "Usage: testGistSVM.cpp <input image folder> <output image folder> <Option: starting frame> <Option: finishing frame number>" << endl;
		return 0;
	}

	if (argc == 5){
		image_path = argv[1];
		output_dir = argv[2];
		starting_f = stoi(argv[3]);
		finishing_f = stoi(argv[4]);
	}
	
	image_path = argv[1];
	output_dir = argv[2];

	if (finishing_f == 0){
		path p(image_path == "" ? "." : image_path);

		vector<directory_entry> v;
		if (is_directory(p)) {

			copy(directory_iterator(p), directory_iterator(), back_inserter(v));
			starting_f = 0;
			finishing_f = v.size();
		}
	}


	//initialize GistSVM class
	GistSVM gsvm;

	//make test data mat
	Mat testData;

	//iterate over the video folder
	int i = starting_f;
	while (i != finishing_f + 1){
		ostringstream image_num;
		image_num << setfill('0') << setw(6) << i;
		string img = image_path + "\\" + "img" + image_num.str() + ".jpg";
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
		image_num << setfill('0') << setw(6) << j + starting_f;
		string img = image_path + "\\" + "img" + image_num.str() + ".jpg";
		Mat tmp_img = imread(img);

		ostringstream ss;
		ss << response;
		string res(ss.str());

		putText(tmp_img, res, Point(100, 100), 0, 5.1, Scalar(255, 255, 0), 4);

		string img_name = "image" + image_num.str() + ".jpg";
		string output = output_dir + "\\" + img_name;
		imwrite(output, tmp_img);

		/*imshow("Image-" + image_num.str() + ".jpg", tmp_img);
		waitKey(0);
		destroyWindow("Image-" + image_num.str());*/
	}

	return 0;

}