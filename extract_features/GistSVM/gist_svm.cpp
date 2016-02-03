#include "gist_svm.h"

using namespace cv;
using namespace std;
using namespace cv::ml;

GistSVM::GistSVM(){
	int nblocks = 4; 
	int nscales = 4; 
	vector<int> orientationsPerScale = vector<int>(4, 8);
	int pos_label = 1; 
	int neg_label = 0;

	this->nblocks_ = nblocks;
	this->nscales_ = nscales;
	this->orientationsPerScale_ = orientationsPerScale;
	this->pos_label_ = pos_label;
	this->neg_label_ = neg_label;
}

GistSVM::GistSVM(int nblocks, int nscales, vector<int> orientationsPerScale, int pos_label, int neg_label){
	//update fields
	this->nblocks_ = nblocks;
	this->nscales_ = nscales;
	this->orientationsPerScale_ = orientationsPerScale;
	this->pos_label_ = pos_label;
	this->neg_label_ = neg_label;
}

int GistSVM::cal_color_descriptor_size(){
	
	int descsize = 0;

	/* compute descriptor size */
	for (int i = 0; i < this->nscales_; i++)
		descsize += this->nblocks_*this->nblocks_*this->orientationsPerScale_[i];
	
	//for color image
	descsize *= 3;

	return descsize;

}

int GistSVM::cal_gray_descriptor_size(){

	int descsize = 0;

	/* compute descriptor size */
	for (int i = 0; i < this->nscales_; i++)
		descsize += this->nblocks_*this->nblocks_*this->orientationsPerScale_[i];

	return descsize;

}

void GistSVM::load_color_mat(const Mat& inimg){
	
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

	this->color_image_ = im;
}

void GistSVM::load_gray_mat(const Mat& inimg){
	
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

	this->gray_image_ = im;
}

float* GistSVM::calc_gist_feature(const Mat& img){

	printf("\n");
	printf("Loading Image...");
	float* result = NULL;
	if (img.channels() == 1){
		this->load_gray_mat(img);

		/*compute descriptor*/
		result = bw_gist_scaletab(this->gray_image_, this->nblocks_, this->nscales_, &this->orientationsPerScale_[0]);


		/*clean up*/
		image_delete(this->gray_image_);

	}
	else if (img.channels() == 3){
		this->load_color_mat(img);

		/*compute descriptor*/
		result = color_gist_scaletab(this->color_image_, this->nblocks_, this->nscales_, &this->orientationsPerScale_[0]);

		/*clean up*/
		color_image_delete(this->color_image_);
	}
	else
		printf("Loading Image failed...Is it a gray or RGB image ?");

	return result;
}

void GistSVM::load_svm_from_file(string svmfile){

	//load svm from xml
	cout << endl << "Loading SVM Model......" << endl;
	this->svm_ = SVM::create();
	this->svm_ = StatModel::load<SVM>(svmfile);
	cout << endl << "Successfully loaded SVM Model......" << endl;

}

void GistSVM::train_SVM(const Mat trainData, const Mat labelData){
	
	//check trainData size. It must be the same as the result of calc_descriptor_size
	
	int descriptor_size;
	
	if (trainData.channels() == 1)
		descriptor_size = this->cal_gray_descriptor_size();
	else if (trainData.channels() == 3)
		descriptor_size = this->cal_color_descriptor_size();
	else
		cout << endl << "Calculate descriptor size error !" << endl;
	
	assert(descriptor_size == trainData.cols);

	//train svm model
	cout << endl << "Training SVM Model......" << endl;
	this->svm_ = SVM::create();
	this->svm_->setType(SVM::C_SVC);
	this->svm_->setKernel(SVM::LINEAR);
	this->svm_->setTermCriteria(TermCriteria(TermCriteria::MAX_ITER, 100, 1e-6));
	this->svm_->train(trainData, ROW_SAMPLE, labelData);
	cout << endl << "Successfully trained SVM Model......" << endl;

	cout << endl << "Saving svm.xml...." << endl;
	this->svm_->save("./svm.xml");
	cout << endl << "Successfully saved svm.xml..." << endl;

}

int GistSVM::predict_mat(const Mat& img){
	
	float response = this->svm_->predict(img);

	return response;
}
