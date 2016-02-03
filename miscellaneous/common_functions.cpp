#include "common_functions.h"


color_image_t* load_color_mat(const string fname){

	Mat img = imread(fname, CV_LOAD_IMAGE_COLOR);
	resize(img, img, Size(256, 256));

	int height = img.rows;
	int width = img.cols;
	color_image_t *im = color_image_new(width, height);

	for (int i = 0; i < height; ++i){
		for (int j = 0; j < width; ++j){
			Vec3b intensity = img.at<Vec3b>(i, j);
			im->c1[i*width + j] = intensity.val[2];
			im->c2[i*width + j] = intensity.val[1];
			im->c3[i*width + j] = intensity.val[0];
		}
	}

	return im;
}

color_image_t* load_color_mat(const Mat& inimg){

	Mat img = inimg.clone();
	resize(img, img, Size(256, 256));

	int height = img.rows;
	int width = img.cols;
	color_image_t *im = color_image_new(width, height);

	for (int i = 0; i < height; ++i){
		for (int j = 0; j < width; ++j){
			Vec3b intensity = img.at<Vec3b>(i, j);
			im->c1[i*width + j] = intensity.val[2];
			im->c2[i*width + j] = intensity.val[1];
			im->c3[i*width + j] = intensity.val[0];
		}
	}

	return im;
}

image_t* load_gray_mat(const string fname){

	Mat img = imread(fname, CV_LOAD_IMAGE_GRAYSCALE);
	resize(img, img, Size(256, 256));

	int height = img.rows;
	int width = img.cols;

	image_t *im = image_new(width, height);

	for (int i = 0; i < height; ++i){
		for (int j = 0; j < width; ++j){
			float intensity = img.at<float>(i, j);
			im->data[i * width + j] = intensity;
		}
	}

	im->stride = sizeof(float) * width * height;

	return im;
}

image_t* load_gray_mat(const Mat& inimg){

	Mat img = inimg.clone();
	resize(img, img, Size(256, 256));

	int height = img.rows;
	int width = img.cols;

	image_t *im = image_new(width, height);

	for (int i = 0; i < height; ++i){
		for (int j = 0; j < width; ++j){
			float intensity = img.at<float>(i, j);
			im->data[i * width + j] = intensity;
		}
	}

	im->stride = sizeof(float) * width * height;

	return im;
}

//function to calculate one image gist descriptor
float* calc_gist_feature(const string fname, const int nblocks, const int nscales, const int* orientations_per_scale){
	printf("\n");
	printf("Loading %s", fname.c_str());
	Mat tmp = imread(fname);
	float* result = NULL;
	if (tmp.channels() == 1){
		image_t* im = load_gray_mat(fname);

		/*compute descriptor*/
		result = bw_gist_scaletab(im, nblocks, nscales, orientations_per_scale);

		/*clean up*/
		image_delete(im);

	}
	else if (tmp.channels() == 3){
		color_image_t* im = load_color_mat(fname);

		/*compute descriptor*/
		result = color_gist_scaletab(im, nblocks, nscales, orientations_per_scale);

		/*clean up*/
		color_image_delete(im);
	}
	else
		printf("Loading %s failed...Is it a gray or RGB image ?", fname.c_str());

	return result;
}

//function to calculate one image gist descriptor
float* calc_gist_feature(const Mat& img, const int nblocks, const int nscales, const int* orientations_per_scale){
	printf("\n");
	printf("Loading Image...");
	float* result = NULL;
	if (img.channels() == 1){
		image_t* im = load_gray_mat(img);

		/*compute descriptor*/
		result = bw_gist_scaletab(im, nblocks, nscales, orientations_per_scale);

		/*clean up*/
		image_delete(im);

	}
	else if (img.channels() == 3){
		color_image_t* im = load_color_mat(img);

		/*compute descriptor*/
		result = color_gist_scaletab(im, nblocks, nscales, orientations_per_scale);

		/*clean up*/
		color_image_delete(im);
	}
	else
		printf("Loading Image failed...Is it a gray or RGB image ?");

	return result;
	
}

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


string setUniqueName(const string src, const string flag){

	size_t start_pos = src.find(flag);
	size_t image_start_pos = start_pos + 9;
	size_t end_pos = src.find(".jpg");
	size_t str_length = end_pos - image_start_pos;
	//get the substring
	string output = src.substr(image_start_pos, str_length);
	return flag + "-" + output + ".bin";
}

int cal_descriptor_size(){
	int descsize = 0;

	/* compute descriptor size */
	for (int i = 0; i < nscales; i++)
		descsize += nblocks*nblocks*orientationsPerScale[i];
	//for color image
	descsize *= 3;

	return descsize;
}


int predict_mat(const Mat& img){



}