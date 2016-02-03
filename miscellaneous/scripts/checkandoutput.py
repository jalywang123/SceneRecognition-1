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
        dest = "./errorfile.csv"
        prior = "C:\\Users\\Johnny\\Desktop\\processing_data\\training_data"
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
                        output_dirname = filename.split('-', 1)[0]
                        output_filename = ".".join([filename.split('-', 1)[1].split('.', 1)[0], "jpg"])
                        output = os.path.join(output_dirname, output_filename)
                        print output
                        label = 2
                        if output_dirname == 'negative':
                            label = 0
                        else:
                            label = 1
                        tmp = ";".join([output, str(label)])
                        writer.writerow([os.path.join(prior, tmp)])
            else:               
                for subdirname in dirnames:
                    subject_path = os.path.join(dirname, subdirname)
                    print subject_path
                    for filename in os.listdir(subject_path):
                        if os.stat(os.path.join([subject_path, filename])).st_size > 0:
                            print ','.join([filename, "is Good!"])
                        else:
                            output_dirname = filename.split('-', 1)[0]
                            output_filename = ".".join([filename.split('-', 1)[1].split('.', 1)[0], "jpg"])
                            output = os.path.join(output_dirname, output_filename)
                            print output
                            label = 2
                            if output_dirname == 'negative':
                                label = 0
                            else:
                                label = 1
                            tmp = ";".join([output, str(label)])
                            writer.writerow([os.path.join(prior, tmp)])