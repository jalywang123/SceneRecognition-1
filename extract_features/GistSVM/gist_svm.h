extern "C"{
#include "lear_gist/gist.h"
#include "lear_gist/standalone_image.h"
#include <stdio.h>
}

#include <opencv2/opencv.hpp>
#include <sstream>
#include <fstream>
#include <iostream>
#include <string>

#include <opencv2/ml.hpp>

class GistSVM{

private:	
	int nblocks_;
	int nscales_;
	std::vector<int> orientationsPerScale_;
	int pos_label_;
	int neg_label_;
	image_t* gray_image_;
	color_image_t* color_image_;
	cv::Ptr<cv::ml::SVM> svm_;

public:
	GistSVM();
	GistSVM(int nblocks, int nscales, std::vector<int> orientationsPerScale, int pos_label = 1, int neg_label = 0);

	int cal_color_descriptor_size();
	int cal_gray_descriptor_size();

	int predict_mat(const cv::Mat& img);
	float* calc_gist_feature(const cv::Mat& img);

	void load_gray_mat(const cv::Mat& inimg);
	void load_color_mat(const cv::Mat& inimg);
	void load_svm_from_file(std::string svmfile);
	void train_SVM(const cv::Mat trainData, const cv::Mat labelData);

};