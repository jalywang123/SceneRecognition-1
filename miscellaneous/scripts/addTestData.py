import os, sys
import csv
import shutil


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: addTestData <training.csv> <add.csv>"
        sys.exit(1)

    if not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
        print "CSV path does not exist !"
        sys.exit(1)
    else:
        OUT_PATH = "./add_test_confirm.csv"
        if os.path.isfile(OUT_PATH):
            os.remove(OUT_PATH)
        writer = csv.writer(open(OUT_PATH, 'w'))
        with open(sys.argv[1], 'r') as tfile, open(sys.argv[2], 'r') as afile:
            trainreader = csv.reader(tfile, delimiter = ';')
            addreader = csv.reader(afile, delimiter = ';')

            trainingdata = list(trainreader)
            addingdata = list(addreader)

            i = 0
            while i < len(addingdata):
                a_name = addingdata[i][0].split('-', 1)[1]
                j = 0
                flag = False
                while j < len(trainingdata):
                    t_name = trainingdata[j][0].split('-', 1)[1]
                    if a_name == t_name:
                        flag = True
                    j += 1
                if flag == False:
                    writer.writerow([';'.join([addingdata[i][0], addingdata[i][1]])])
                    from_path = addingdata[i][0]
                    to_path = "C:\\Users\\Johnny\\Desktop\\extract_features\\dataset\\testing_data"
                    shutil.copy(from_path, os.path.join(to_path, 'negative-' + a_name))
                i += 1
                

            


