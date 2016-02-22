#include "GistSVM/gist_svm.h"
#include <iomanip>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace cv;
using namespace std;
using namespace cv::ml;
using namespace boost::filesystem;

#pragma comment(lib, "GistSVM.lib")

const string svm_file = "C:\\Users\\Johnny\\Desktop\\extract_features\\TrainSVM\\svm.xml";
const string test_example = "\\\\ws-qvl016\\Frames - Hong Kong SD\\Happy Valley\\20090211\\VTS_01_3\\img008420.jpg";

static vector<pair<string, int>> getTxtContent(istream& str){

	string line;
	vector<pair<string, int>> result;

	while (getline(str, line)){
		istringstream iss(line);
		string a, b;
		getline(iss, a, ';');
		getline(iss, b);
		pair <string, int> tmp;
		tmp.first = a;
		tmp.second = stoi(b);
		result.push_back(tmp);
	}

	return result;
}


int main(int argc, const char** argv){

	string txt_path = "";
	string output_dir = "";

	if (argc < 3){
		cout << "Usage: testGistSVM.cpp <input txt file> <output folder>" << endl;
		return 0;
	}


	txt_path = argv[1];
	output_dir = argv[2];

	//initialize GistSVM class
	GistSVM gsvm;

	//make test data mat
	Mat testData;

	//iterate over txt file
	ifstream file;
	file.open(txt_path, ifstream::in);
	vector<pair<string, int>> contents = getTxtContent(file);
	file.close();
	
	for (const auto& c : contents){

		string img = c.first;
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
		cout << endl << "Calculated : " + img << endl;
	
	}

	//Mat tmpImg = imread(test_example);
	//int descsize = gsvm.cal_color_descriptor_size();
	//float* result = gsvm.calc_gist_feature(tmpImg);
	//Mat tmp_img = Mat(1, descsize, CV_32FC1, result);
	//testData.push_back(tmp_img);

	//print out test set size
	cout << endl << "Size of testing data = " << testData.size() << endl;

	//load svm
	gsvm.load_svm_from_file(svm_file);

	//get output file name
	int start_pos = txt_path.find("test_set") + 9;
	int length = txt_path.length() - start_pos;
	string output_file_name = txt_path.substr(start_pos, length);

	//making predictions
	for (int j = 0; j < testData.rows; ++j){

		Mat sampleMat = testData.row(j);

		float response = gsvm.predict_mat(sampleMat);

		// write to output file
		string image_name = contents[j].first;
		
		ostringstream ss;
		ss << response;
		string res(ss.str());

		string line_content = image_name + ";" + res + "\n";

		ofstream f;
		f.open(output_dir + "\\" + output_file_name, ofstream::out | ofstream::app);
		f << line_content;
		f.close();

		/*imshow("Image-" + image_num.str() + ".jpg", tmp_img);
		waitKey(0);
		destroyWindow("Image-" + image_num.str());*/
	}

	//for (int j = 0; j < testData.rows; ++j){
	//	Mat sampleMat = testData.row(j);
	//	float response = gsvm.predict_mat(sampleMat);
	//	cout << endl << "Response = " << response << endl;
	//	int i;
	//	cin >> i;
	//}


	return 0;

}