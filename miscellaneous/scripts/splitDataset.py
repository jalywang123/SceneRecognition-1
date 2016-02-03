import os
import sys
import shutil

def cal_training_testing(count_pos, count_neg, path):
    for dirname, dirnames, filenames in os.walk(path):
        if dirnames == []:
            for filename in os.listdir(dirname):
                header = filename.split('-', 1)[0]
                if header == 'negative':
                    count_neg += 1
                else:
                    count_pos += 1
        else:               
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    header = filename.split('-', 1)[0]
                    if header == 'negative':
                        count_neg += 1
                    else:
                        count_pos += 1
    #print out the number of positive and negative items
    print "count_neg = " + str(count_neg)
    print "count_pos = " + str(count_pos)
    return (count_pos, count_neg)


def split_dataset_testing(count_pos, count_neg, oripath, despath):
    #get the rest 20% of the data and treat it as testing set
    split_point = int(round((count_neg + count_pos) * 0.8))
    pos_num = 0
    neg_num = 0
    count = 0
    for dirname, dirnames, filenames in os.walk(oripath):
        if dirnames == []:
            for filename in os.listdir(dirname):
                header = filename.split('-', 1)[0]
                frompath = os.path.join(dirname,filename)
                topath = os.path.join(despath, filename)
                if header == 'negative' and count > split_point:
                    neg_num += 1
                    shutil.copy(frompath, topath)
                    print str(count)         
                elif header == 'positive' and count > split_point:
                    pos_num += 1
                    shutil.copy(frompath, topath)
                    print str(count)
                else:
                    print " Waiting to be shifted ..."
                count += 1
                    
        else:               
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    header = filename.split('-', 1)[0]
                    frompath = os.path.join(dirname,filename)
                    topath = os.path.join(despath, filename)
                    if header == 'negative' and count > split_point:
                        neg_num += 1
                        shutil.copy(frompath, topath)
                        print str(count)         
                    elif header == 'positive' and count > split_point:
                        pos_num += 1
                        shutil.copy(frompath, topath)
                        print str(count)
                    else:
                        print " Waiting to be shifted ..."
                    count += 1




def split_dataset_training(count_pos, count_neg, oripath, despath):
    #get 80% of the data and treat it as training set, the ratio of positive to negative is 1 : 1
    split_point = int(round(((count_neg + count_pos) / 2) * 0.8))
    pos_num = 0
    neg_num = 0
    for dirname, dirnames, filenames in os.walk(oripath):
        if dirnames == []:
            for filename in os.listdir(dirname):
                header = filename.split('-', 1)[0]
                frompath = os.path.join(dirname,filename)
                topath = os.path.join(despath, filename)
                if header == 'negative' and neg_num <= split_point:
                    neg_num += 1
                    shutil.copy(frompath, topath)         
                elif header == 'positive' and pos_num <= split_point:
                    pos_num += 1
                    shutil.copy(frompath, topath)
                else:
                    print "Finshed spliting dataset!"
                    
        else:               
            for subdirname in dirnames:
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    header = filename.split('-', 1)[0]
                    frompath = os.path.join(subject_path,filename)
                    topath = os.path.join(despath, filename)
                    if header == 'negative' and neg_num <= split_point:
                        neg_num += 1
                        shutil.copy(frompath, topath)         
                    elif header == 'positive' and pos_num <= split_point:
                        pos_num += 1
                        shutil.copy(frompath, topath)
                    else:
                        print "Finshed spliting dataset!"

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: splitDataset <Dataset Path>"
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print "Dataset Path does not exist !"
        sys.exit(1)
    else:
        #define output path
        OUT_PATH = os.path.abspath("./testing_data")
        if os.path.exists(OUT_PATH):
            shutil.rmtree(OUT_PATH)
            os.mkdir(OUT_PATH)
        else:
            os.mkdir(OUT_PATH)

        count_pos = 0
        count_neg = 0
        BASE_PATH = os.path.abspath(sys.argv[1])
        (count_pos, count_neg) = cal_training_testing(count_pos, count_neg, BASE_PATH)
        
        #split_dataset_training(count_pos, count_neg, BASE_PATH, OUT_PATH)
        split_dataset_testing(count_pos, count_neg, BASE_PATH, OUT_PATH)

        #training_pos = 0
        #training_neg = 0
        #(training_pos, training_neg) = cal_training_testing(training_pos, training_neg, OUT_PATH)

        #print "training_pos = " + str(training_pos)
        #print "training_neg = " + str(training_neg)
        
        testing_pos = 0
        testing_neg = 0
        (testing_pos, testing_neg) = cal_training_testing(testing_pos, testing_neg, OUT_PATH)

        print "testing_pos = " + str(testing_pos)
        print "testing_neg = " + str(testing_neg)





