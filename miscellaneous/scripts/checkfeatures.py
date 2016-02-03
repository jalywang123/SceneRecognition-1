import os
import sys
import csv

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: checkfeatures <Check Path>"
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print "Check Path does not exist !"
        sys.exit(1)
    else:
        print "I am here"
        dest = "./errorfile.csv"
        BASE_PATH = os.path.abspath(sys.argv[1])
        writer = csv.writer(open(dest, "w"))
        for dirname, dirnames, filenames in os.walk(BASE_PATH):
            print dirname
            if dirnames == []:
                for filename in os.listdir(dirname):
                    subject_path = os.path.join(dirname, filename)
                    if os.stat(subject_path).st_size > 0:
                        print ','.join([filename, "is Good!"])
                    else:
                        writer.writerow([filename])
            else:               
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    print subject_path
                    for filename in os.listdir(subject_path):
                        print filename
                        if os.stat(filename).st_size > 0:
                            print ','.join([filename, "is Good!"])
                        else:
                            writer.writerow([filename])