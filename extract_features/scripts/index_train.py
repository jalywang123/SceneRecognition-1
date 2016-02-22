import os
import sys
import json

if __name__ == '__main__':

    PATH = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\training_set"
    train_txt = PATH + "\\" + "train.txt"

    for root, dirnames, filenames in os.walk(PATH):
        with open(train_txt, 'w') as tf:
            for f in filenames:
                tf.write(PATH + "\\" + f + "\n")
