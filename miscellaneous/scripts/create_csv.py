import os
import sys
import csv

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: create_csv <Base Path>"
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print "Base Path does not exist !"
        sys.exit(1)
    else:
        dest = "./testing.csv"
        BASE_PATH = os.path.abspath(sys.argv[1])
        writer = csv.writer(open(dest, "w"))
        for dirname, dirnames, filenames in os.walk(BASE_PATH):
            if dirnames == []:
                for filename in os.listdir(dirname):
                    subject_path = os.path.join(dirname, filename)
                    header = filename.split('-', 1)[0]
                    label = 2
                    if header == 'negative':
                        label = 0
                    else:
                        label = 1
                    tmp = ";".join([subject_path, str(label)])
                    writer.writerow([tmp])
            else:               
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    for filename in os.listdir(subject_path):
                        subject_path = os.path.join(dirname, filename)
                        header = filename.split('-', 1)[0]
                        label = 2
                        if header == 'negative':
                            label = 0
                        else:
                            label = 1
                        tmp = ";".join([subject_path, str(label)])
                        writer.writerow([tmp])