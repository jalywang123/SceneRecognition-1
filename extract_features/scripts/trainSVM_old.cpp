#include "common_functions.h"
#include <opencv2/ml.hpp>

using namespace cv::ml;



int main(int argc, const char** argv){

	const string output_dir = "./svm.xml";
	//read training csv file
	ifstream file;
	file.open(argv[1], ifstream::in);
	vector<pair<string, int>> contents = getCSVcontent(file);
	file.close();

	ifstream file_tmp;
	file_tmp.open(argv[2], ifstream::in);
	vector<pair<string, int>> contents_tmp = getCSVcontent(file_tmp);
	file_tmp.close();

	//compute descriptor size
	int descsize = cal_descriptor_size();
	
	//total sample size
	int totalsample = contents.size();
	Mat trainData;
	Mat labelData;
	Mat testData;
	Mat labeltest;

	int count = 0;
	//iterate every item in training.csv file
	for (const auto& c : contents){
		float* tmp_desc = new float[descsize]; 
		ifstream ifs;
		ifs.open(c.first, fstream::binary);
		ifs.read((char*)tmp_desc, descsize * sizeof(float));
		ifs.close();
		Mat tmp_img = Mat(1, descsize, CV_32FC1, tmp_desc);
		trainData.push_back(tmp_img);
		labelData.push_back(Mat(1, 1, CV_32SC1, c.second));
		////print out mat
		//cout << "Training Data = " << endl << tmp_img << endl;
		//cout << "Size of training data = " << trainData.size() << endl;
		//cout << "Labels = " << endl << labelData << endl;
		//cout << "Size of training data = " << labelData.size() << endl;
		//count++;
	}

	//iterate every item in testing.csv file
	for (const auto& c : contents_tmp){
		float* tmp_desc = new float[descsize];
		ifstream ifs;
		ifs.open(c.first, fstream::binary);
		ifs.read((char*)tmp_desc, descsize * sizeof(float));
		ifs.close();
		Mat tmp_img = Mat(1, descsize, CV_32FC1, tmp_desc);
		testData.push_back(tmp_img);
		labeltest.push_back(Mat(1, 1, CV_32SC1, c.second));
		//cout << endl << "Label test data = " << c.second << endl;
	}

	cout << "Size of training data = " << trainData.size() << endl;
	cout << "Size of label = " << labelData.size() << endl;

	cout << "Size of testing data = " << testData.size() << endl;
	cout << "Size of test label = " << labeltest.size() << endl;

	//train svm model
	cout << endl << "Training SVM Model......" << endl;
	Ptr<SVM> svm = SVM::create();
	svm->setType(SVM::C_SVC);
	svm->setKernel(SVM::LINEAR);
	svm->setTermCriteria(TermCriteria(TermCriteria::MAX_ITER, 100, 1e-6));
	svm->train(trainData, ROW_SAMPLE, labelData);
	cout << endl << "Successfully trained SVM Model......" << endl;

	cout << endl << "Saving svm.xml...." << endl;
	svm->save(output_dir);
	cout << endl << "Successfully saved svm.xml..." << endl;


	int total = testData.rows;
	int correct_num = 0;
	//making predictions
	for (int i = 0; i < testData.rows; ++i){
		Mat sampleMat = testData.row(i);
		float response = svm->predict(sampleMat);
		int target = labeltest.at<int>(i, 0);
			
		if (target == response)
			correct_num++;	
		//cout << endl << "target = " << target << endl;
		//cout << endl << "response = " << response << endl;
	}

	cout << endl << "correct_num = " << correct_num << endl;
	//print out accuracy
	cout << endl << "The prediction accuracy: " << correct_num / total << endl;
	return 0;
}