import os
import sys

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_txt <input txt folder> <output path>"
        sys.exit(1)

    output_dir = os.path.abspath(sys.argv[2])
    if not os.path.exists(output_dir) :
        os.mkdir(output_dir)

    if not os.path.exists(sys.argv[1]):
        print "Provided txt folder does not exist !"
        sys.exit(1)
    else:
        src = sys.argv[1]
        line1 = "set PROGRAM=\"C:\\Users\\Johnny\\Desktop\\extract_features\\build\\x64\\Debug\\TestGistSVM2.exe\"" 
        line3 = "set INPUT2=" + output_dir
        count = 0
        for root, dirnames, filenames in os.walk(src):
            for f in filenames:
                line2 = "set INPUT1=" + os.path.abspath(root) + "\\" + f
                filename = output_dir + "\\" + "runGistSVM" + "_" + str(count) + ".bat"
                count += 1
                line4 = "%PROGRAM% \"%INPUT1%\" \"%INPUT2%\" "              
                f = open(filename, 'w')
                f.write(line1 + "\n")
                f.write(line2 + "\n")
                f.write(line3 + "\n")
                f.write("\n")
                f.write(line4 + "\n")
                f.close()