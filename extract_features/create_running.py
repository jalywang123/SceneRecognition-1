import os
import sys


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_runing <input path> <output path>"
        sys.exit(1)

    output_dir = os.path.abspath(sys.argv[2])
    if not os.path.exists(output_dir) :
        os.mkdir(output_dir)
        
    
    if not os.path.exists(sys.argv[1]) :
        print "Output path does not exist !"
        sys.exit(1)
    else:
        dest = os.path.abspath(sys.argv[1])
        count = 0
        line1 = "set PROGRAM=\"C:\\Users\\Johnny\\Desktop\\extract_features\\build\\x64\\Debug\\TestGistSVM.exe\"" 
        line4 = "%PROGRAM% \"%INPUT1%\" \"%INPUT2%\"."
        for dirname, dirnames, filenames in os.walk(dest):        
            if dirnames == []:
                folder_name = dirname.split('-', 2)[2].split("\\", 1)[1].replace("\\", "-")
                output_folder = output_dir + "\\" + folder_name
                os.mkdir(output_folder)
                filename = output_dir + "\\" + "runGistSVM" + "_" + str(count) + ".bat"
                count += 1
                line2 = "set INPUT1=" + dirname
                line3 = "set INPUT2=" + output_folder
                f = open(filename, 'w')
                f.write(line1 + "\n")
                f.write(line2 + "\n")
                f.write(line3 + "\n")
                f.write("\n")
                f.write(line4 + "\n")
                f.close()