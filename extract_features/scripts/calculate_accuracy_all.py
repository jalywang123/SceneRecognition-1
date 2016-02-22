import os
import sys
import shutil

OUTPUT_DIR = "C:\\Users\\Johnny\\Desktop\\extract_features\\scripts\\runTest"

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_txt <ground truth folder> <predicted folder>"
        sys.exit(1)

    ground_truth = sys.argv[1]
    predicted = sys.argv[2]

    g_files = []
    p_files = []

    for root, dirs, files in os.walk(ground_truth):
        for file in files:
            if file.endswith(".txt"):
                g_files.append(file)

    for root, dirs, files in os.walk(predicted):
        for file in files:
            if file.endswith(".txt"):
                p_files.append(file)

    all_true_positive = 0
    all_true_negative = 0
    all_false_positive = 0
    all_false_negative = 0

    for i in range(len(g_files)):
        
        g_contents = []
        p_contents = []

        file1 = os.path.abspath(ground_truth + "\\" + g_files[i])
        file2 = os.path.abspath(predicted + "\\" + p_files[p_files.index(g_files[i])])
        with open(file1, 'r') as g, open(file2, 'r') as p:
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

        output_folder = file2.split('.')[0]
        print output_folder 
    
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
                false_negative += 1
                output_false_positive = output_folder + "\\" + "false_negative"
                if not os.path.exists(output_false_positive):
                    os.mkdir(output_false_positive)
                output_filename = output_false_positive + "\\" + '-'.join(filename_1.split('\\', 4)[4].split('.')[0].split('\\')) + ".jpg"
                shutil.copy(filename_1, output_filename)
            if filename_1 == filename_2 and int(label_1) == 0 and label_1 != label_2:
                false_positive += 1
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

        all_true_positive += true_positive
        all_true_negative += true_negative
        all_false_negative += false_negative
        all_false_positive += false_positive

    # print out overall accuracy and overall precision, overall recall
    if all_true_positive != 0 and all_true_negative != 0 : 
        all_precision = "%.9f" % (all_true_positive / float(all_true_positive + all_false_positive))
        all_recall = "%.9f" % (all_true_positive / float(all_true_positive + all_false_negative))
        all_accuracy = "%.9f" % ((all_true_positive + all_true_negative) / float(all_true_positive + all_false_negative + all_true_negative + all_false_positive))
    print "\n\n"
    print " The overall precision is : " + all_precision + "\n"
    print " The overall recall is : " + all_recall + "\n"
    print " The overall accuracy is : " + all_accuracy + "\n"


