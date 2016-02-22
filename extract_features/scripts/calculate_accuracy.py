import os
import sys
import shutil

OUTPUT_DIR = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\runTest"

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_txt <ground truth txt> <predicted txt>"
        sys.exit(1)

    ground_truth = sys.argv[1]
    predicted = sys.argv[2]

    g_contents = []
    p_contents = []
    with open(ground_truth, 'r') as g, open(predicted, 'r') as p:
        g_contents = g.readlines()
        p_contents = p.readlines()

    count = 0
    for i in range(len(g_contents)):
        filename_1, label_1 = g_contents[i].split(';')
        filename_2, label_2 = p_contents[i].split(';')
        if filename_1 == filename_2 and label_2 != label_1:
            count += 1

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    output_folder = OUTPUT_DIR + "\\" + ground_truth.split('.')[0]
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for i in range(len(g_contents)):
        filename_1, label_1 = g_contents[i].split(';')
        filename_2, label_2 = p_contents[i].split(';')
        if filename_1 == filename_2 and int(label_1) == 1 and label_1 == label_2:
            true_positive += 1
        if filename_1 == filename_2 and int(label_1) == 0 and label_1 == label_2:
            true_negative += 1
        if filename_1 == filename_2 and int(label_1) == 1 and label_1 != label_2:
            false_positive += 1
            output_false_positive = output_folder + "\\" + "false_negative"
            if not os.path.exists(output_false_positive):
                os.mkdir(output_false_positive)
            output_filename = output_false_positive + "\\" + '-'.join(filename_1.split('\\', 4)[4].split('.')[0].split('\\')) + ".jpg"
            shutil.copy(filename_1, output_filename)
        if filename_1 == filename_2 and int(label_1) == 0 and label_1 != label_2:
            false_negative += 1
            output_false_negative = output_folder + "\\" + "false_positive"
            if not os.path.exists(output_false_negative):
                os.mkdir(output_false_negative)
            output_filename = output_false_negative + "\\" + '-'.join(filename_1.split('\\', 4)[4].split('.')[0].split('\\')) + ".jpg"
            shutil.copy(filename_1, output_filename)

    # print out accuracy
    precision = "%.9f" % 0.0
    recall = "%.9f" % 0.0
    print true_positive
    print true_negative
    print false_negative
    print false_positive
    if true_positive != 0 and true_negative != 0 : 
        precision = "%.9f" % (true_positive / float(true_positive + false_positive))
        recall = "%.9f" % (true_positive / float(true_positive + false_negative))
        accuracy = "%.9f" % ((true_positive + true_negative) / float(true_positive + false_negative + true_negative + false_positive))

    print " The precision is : " + precision + "\n"
    print " The recall is : " + recall + "\n"
    print " The accuracy is : " + accuracy + "\n"



