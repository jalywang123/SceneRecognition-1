import os
import sys
import json

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: create_txt <json file> <output path>"
        sys.exit(1)

    output_dir = os.path.abspath(sys.argv[2])
    if not os.path.exists(output_dir) :
        os.mkdir(output_dir)
    
    BASE_PATH = "\\\\ws-qvl016\\Frames - Hong Kong SD"

    if not os.path.exists(sys.argv[1]):
        print "Provided json does not exist !"
        sys.exit(1)
    else:
        json_file = os.path.abspath(sys.argv[1])
        with open(json_file, 'r') as js_f:
            data = json.load(js_f)
            for d in data:
                output_file_name = output_dir + "\\" + d['Track'] + '-' + str(d['Date']) + '.txt'
                # get each race frame range. StartingFrame and FinishingFrame might not in the same folder
                videoNames = d['VideoName'].split(',')
                starts = d['StartingFrame'].split(',')
                finishes = d['FinishingFrame'].split(',')
                # get file path
                i = 0
                while i < len(videoNames) / 2:
                    
                    all_files = []

                    if videoNames[i * 2] == videoNames[i * 2 + 1]:
                        fname = BASE_PATH + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2]
                        sample_frames = map(lambda x: (x, 1), range(int(starts[i]) - 25, int(starts[i]) + 25, 1)) + map(lambda x: (x, 0), range(int(starts[i]) + 500, int(finishes[i]), 25))
                        for (sample_num, label) in sample_frames:
                            image_name = fname + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"    
                            all_files.append((image_name, label))
                    else:
                        # race frames are not in same folder then it is a bit complicated
                        # first, extract images in folder one then extract other images in folder 2
                        positive_samples = map(lambda x: (x, 1), range(int(starts[i]) - 25, int(starts[i]) + 25, 1))
                        fname_1 = BASE_PATH + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2]
                        for (sample_num, label) in positive_samples:
                            positive_image_name = fname_1 + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"
                            all_files.append((positive_image_name, label))

                        negative_sample = int(starts[i]) + 500
                        fname_2 = BASE_PATH + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2 + 1]
                        file_path_1 = fname_1 + "\\" + "img" + '{:06d}'.format(negative_sample) + ".jpg" 
                        while os.path.exists(file_path_1):
                            negative_sample_name = fname_1 + "\\" + "img" + '{:06d}'.format(negative_sample) + ".jpg"
                            all_files.append((negative_sample_name, 0))
                            negative_sample += 25
                            file_path_1 = fname_1 + "\\" + "img" + '{:06d}'.format(negative_sample) + ".jpg"
                        
                        # negative samples in next folder
                        negative_samples = map(lambda x: (x, 0), range(0, int(finishes[i]), 25))
                        for (sample_num, label) in negative_samples:
                            image_name = fname_2 + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"    
                            all_files.append((image_name, label))
                    
                    #write to file
                    with open(output_file_name, 'a') as f:
                        for (file_name, label) in all_files:
                            f.write(file_name + ";" + str(label) + "\n")
                    i += 1



