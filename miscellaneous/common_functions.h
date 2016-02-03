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

using namespace cv;
using namespace std;

const static int nblocks = 4;
const static int nscales = 4;
const static int orientationsPerScale[50] = { 8, 8, 8, 8 };
const static int pos_label = 0;
const static int neg_label = 1;

float* calc_gist_feature(const string fname, const int nblocks, const int nscales, const int* orientations_per_scale);
float* calc_gist_feature(const Mat& img, const int nblocks, const int nscales, const int* orientations_per_scale);
color_image_t* load_color_mat(const string fname);
color_image_t* load_color_mat(const Mat& inimg);
image_t* load_gray_mat(const string fname);
image_t* load_gray_mat(const Mat& inimg);

vector<pair<string, int>> getCSVcontent(istream& str);
string setUniqueName(const string src, const string flag);
int cal_descriptor_size();

int predict_mat(const Mat& img);

