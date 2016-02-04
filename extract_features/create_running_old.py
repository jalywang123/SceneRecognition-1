import os
import sys
import json

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
        json_file = os.path.abspath(sys.argv[2])
        count = 0
        line1 = "set PROGRAM=\"C:\\Users\\Johnny\\Desktop\\extract_features\\build\\x64\\Debug\\TestGistSVM.exe\"" 
        flist = []
        with open(json_file, 'r') as js_f:
            data = json.load(js_f)
            for d in data:
                fname = d['Track'] + '-' + d['Date'] + '-' + d['VideoName']
                start = d['StartingFrame']
                finish = d['FinishingFrame']
                flist.append((fname, start, finish))
        for dirname, dirnames, filenames in os.walk(src):        
            if dirnames == []:
                folder_name = dirname.split('-', 2)[2].split("\\", 1)[1].replace("\\", "-")
                for i in range(len(flist)):
                    if folder_name in flist[i]:
                        output_folder = output_dir + "\\" + folder_name
                        os.mkdir(output_folder)
                        filename = output_dir + "\\" + "runGistSVM" + "_" + str(count) + ".bat"
                        count += 1
                        line2 = "set INPUT1=" + dirname
                        line3 = "set INPUT2=" + output_folder
                        line4 = "%PROGRAM% \"%INPUT1%\" \"%INPUT2%\" " + flist[i][1] + " " + flist[i][2] + " ."
                        f = open(filename, 'w')
                        f.write(line1 + "\n")
                        f.write(line2 + "\n")
                        f.write(line3 + "\n")
                        f.write("\n")
                        f.write(line4 + "\n")
                        f.close()