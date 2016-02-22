import os
import sys
import json
import shutil

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_runing <json file> <output path>"
        sys.exit(1)

    output_dir = os.path.abspath(sys.argv[2])
    if not os.path.exists(output_dir) :
        os.mkdir(output_dir)
        
    BASE_PATH = "\\\\ws-qvl016\\Frames - Hong Kong HD"
    
    if not os.path.exists(sys.argv[1]):
        print "Provided json does not exist !"
        sys.exit(1)
    else:
        json_file = os.path.abspath(sys.argv[1])
        count = 0
        line1 = "set PROGRAM=\"C:\\Users\\Johnny\\Desktop\\extract_features\\build\\x64\\Debug\\TestGistSVM.exe\"" 
        with open(json_file, 'r') as js_f:
            data = json.load(js_f)
            for d in data:
                folder_name = d['Track'] + "-" + str(d['Date']) + "-" + d['VideoName']
                fname = BASE_PATH + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + d['VideoName']
                start = d['StartingFrame']
                finish = d['FinishingFrame']
                if os.path.exists(fname):
                    output_folder = output_dir + "\\" + folder_name
                    if not os.path.exists(output_folder):
                        os.mkdir(output_folder)
                    else:
                        shutil.rmtree(output_folder)
                        os.mkdir(output_folder)
                    filename = output_dir + "\\" + "runGistSVM" + "_" + str(count) + ".bat"
                    count += 1
                    line2 = "set INPUT1=" + fname
                    line3 = "set INPUT2=" + output_folder
                    line4 = "%PROGRAM% \"%INPUT1%\" \"%INPUT2%\" " + str(start) + " " + str(finish) + "."
                    f = open(filename, 'w')
                    f.write(line1 + "\n")
                    f.write(line2 + "\n")
                    f.write(line3 + "\n")
                    f.write("\n")
                    f.write(line4 + "\n")
                    f.close()