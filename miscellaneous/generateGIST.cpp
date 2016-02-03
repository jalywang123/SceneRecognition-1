#include "common_functions.h"

int main(int argc, const char* argv[]){
	//loading images
	if (argc < 2){
		cout << "Usage: program <csv file or csv file path> <output path>" << endl;
		return 0;
	}

	printf("\n");
	printf("Input argument %s and %s", argv[1], argv[2]);


	int descsize = cal_descriptor_size();

	cout << endl << "Descriptor size : " << descsize << endl;

	//read csv file
	ifstream file;
	file.open(argv[1], ifstream::in);
	vector<pair<string, int>> contents = getCSVcontent(file);
	file.close();
	string output_folder = argv[2];
	for (const auto &c : contents){
		if (c.second == 0){
			cout << endl << c.first << endl;
			float* result = calc_gist_feature(c.first, nblocks, nscales, orientationsPerScale);

			//create output file name, must be unique
			string flag = "negative";
			//get the name of the output file
			string fname = setUniqueName(c.first, flag);
			string output_dir = output_folder + "\\" + fname;
			cout <<endl << output_dir << endl;
			FILE* pFile = fopen(output_dir.c_str(), "wb");
			fwrite(result, sizeof(float), descsize, pFile);
			fclose(pFile);
			free(result);
			}
		else if (c.second == 1){
			cout << endl << c.first << endl;
			float* result = calc_gist_feature(c.first, nblocks, nscales, orientationsPerScale);

			//create output file name, must be unique
			string flag = "positive";
			//get the name of the output file
			string fname = setUniqueName(c.first, flag);
			string output_dir = output_folder + "/" + fname;
			FILE* pFile = fopen(output_dir.c_str(), "wb");

			///* print descriptor */
			//for (int i = 0; i < descsize; i++)
			//	printf("%.4f ", result[i]);
			cout << endl << output_dir << endl;

			fwrite(result, sizeof(float), descsize, pFile);
			fclose(pFile);
			free(result);
			}
		else{
			printf("training data contains error labeling set --> %s", c.first);
			return 0;
		}
	}



	return 0;
}