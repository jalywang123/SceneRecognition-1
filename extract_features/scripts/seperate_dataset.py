import os
import sys
import json
import shutil

if __name__ == '__main__':

    PATH_1 = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\f1"
    PATH_2 = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\f2"
    OUTPUT_DIR = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\training_set"

    for root, dirnames, filenames in os.walk(PATH_1):
        file_num = int(len(filenames) * 0.8)
        for i in range(file_num):
            shutil.move( ".\\f1\\" + filenames[i], OUTPUT_DIR + "\\" + filenames[i])

    
    for root, dirnames, filenames in os.walk(PATH_2):
        file_num = int(len(filenames) * 0.8)
        for i in range(file_num):
            shutil.move(".\\f2\\"+ filenames[i], OUTPUT_DIR + "\\" + filenames[i])