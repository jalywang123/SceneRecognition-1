#include "GistSVM/gist_svm.h"
#include <iomanip>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace cv;
using namespace std;
using namespace cv::ml;
using namespace boost::filesystem;

#pragma comment(lib, "GistSVM.lib")

const string train_folder = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\training_set";

static vector<string> getTxtContent(istream& str){

	string line;
	vector<string> result;

	while (getline(str, line)){
		istringstream iss(line);
		string a;
		getline(iss, a);
		result.push_back(a);
	}

	return result;
}

static vector<pair<string, int>> getImages(istream& str){

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

	if (argc < 2){
		cout << "Usage: trainSVM.cpp <input txt file>" << endl;
		return 0;
	}


	txt_path = argv[1];

	//initialize GistSVM class
	GistSVM gsvm;

	//make test data mat
	Mat trainData;
	Mat labelData;


	//iterate over txt file to get all training txt files
	ifstream file;
	file.open(txt_path, ifstream::in);
	vector<string> contents = getTxtContent(file);
	file.close();


	for (const auto& c : contents){

		//iterate over txt file to get all training images files
		ifstream filetmp;
		filetmp.open(c, ifstream::in);
		cout << endl << c << endl;
		vector<pair<string, int>> images = getImages(filetmp);
		filetmp.close();
		
		for (const auto& img : images){
			
			Mat tmpImg = imread(img.first);
			if (tmpImg.empty()) {
				
				cout << endl << img.first + "is empty !!" << endl;
				continue;

			}
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

			trainData.push_back(tmp_img);
			labelData.push_back(img.second);
			cout << endl << "Calculated : " + img.first << endl;
			cout << endl << "Ground Truth Label is : " + to_string(img.second)<< endl;

		}

	}

	//print out test set size
	cout << endl << "Size of training data = " << trainData.size() << endl;


	//train the SVM model
	gsvm.train_SVM(trainData, labelData);


	return 0;

}