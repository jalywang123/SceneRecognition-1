import json, os, sys
import shutil

class CreateTrain:

    """

    CreateTrain is a class to create traing set for svm classifier.

    usage:
        ParseJson(path_to_json_HD, path_to_json_SD, output_dir)

    """
    #private variables
    __image_root_HD = "\\\\ws-qvl016\\Frames - Hong Kong HD"
    __image_root_SD = "\\\\ws-qvl016\\Frames - Hong Kong SD"
    __hd_fp = ""
    __sd_fp = ""
    __output_dir = ""

    #constructor
    def __init__(self, hd_f, sd_f, dest):
        if os.path.exists(hd_f) and os.path.exists(sd_f):           
           self.__hd_fp = os.path.abspath(hd_f)
           self.__sd_fp = os.path.abspath(sd_f)
        else:
            print "Json files do not exist"

        if os.path.exists(dest):
            shutil.rmtree(dest)
            os.mkdir(dest)
        else:
            os.mkdir(dest)

        self.__output_dir = dest

    #sample HD json file
    def sampleHD(self):

        with open(self.__hd_fp, 'r') as hd_f:
            data = json.load(hd_f)
            for d in data:
                output_file_name = self.__output_dir + "\\" + d['Track'] + '-' + str(d['Date']) + '.txt'
                start = d['StartingFrame']
                finish = d['FinishingFrame']

                #for starting frames samples 
                leftbound = d['StartingFrame'] - 25
                rightbound = d['StartingFrame'] + 50

                if leftbound < 0:
                    leftbound = 0
                
                all_files = []

                src_dir = os.path.join(self.__image_root_HD, d['Track'], str(d['Date']), d['VideoName'])
                sample_frames = map(lambda x: (x, 1), range(leftbound, rightbound, 1)) + map(lambda x: (x, 0), range(start + 500, finish, 25))
                for (sample_num, label) in sample_frames:
                    image_name = src_dir + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"    
                    all_files.append((image_name, label))

                #write to file
                with open(output_file_name, 'a') as f:
                    for (file_name, label) in all_files:
                        f.write(file_name + ";" + str(label) + "\n")


    #sample SD json file
    def sampleSD(self):

        json_file = self.__sd_fp
        with open(json_file, 'r') as js_f:
            data = json.load(js_f)
            for d in data:
                output_file_name = self.__output_dir + "\\" + d['Track'] + '-' + str(d['Date']) + '.txt'
                # get each race frame range. StartingFrame and FinishingFrame might not in the same folder
                videoNames = d['VideoName'].split(',')
                starts = d['StartingFrame'].split(',')
                finishes = d['FinishingFrame'].split(',')
                # get file path
                i = 0
                while i < len(videoNames) / 2:
                    
                    all_files = []

                    if videoNames[i * 2] == videoNames[i * 2 + 1]:
                        fname = self.__image_root_SD + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2]
                        sample_frames = map(lambda x: (x, 1), range(int(starts[i]) - 25, int(starts[i]) + 50, 1)) + map(lambda x: (x, 0), range(int(starts[i]) + 500, int(finishes[i]), 25))
                        for (sample_num, label) in sample_frames:
                            image_name = fname + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"    
                            all_files.append((image_name, label))
                    else:
                        # race frames are not in same folder then it is a bit complicated
                        # first, extract images in folder one then extract other images in folder 2
                        positive_samples = map(lambda x: (x, 1), range(int(starts[i]) - 25, int(starts[i]) + 50, 1))
                        fname_1 = self.__image_root_SD + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2]
                        for (sample_num, label) in positive_samples:
                            positive_image_name = fname_1 + "\\" + "img" + '{:06d}'.format(sample_num) + ".jpg"
                            all_files.append((positive_image_name, label))

                        negative_sample = int(starts[i]) + 500
                        fname_2 = self.__image_root_SD + "\\" + d['Track'] + "\\" + str(d['Date']) + "\\" + videoNames[i * 2 + 1]
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




if __name__ == '__main__':
    
    json_1 = sys.argv[1]
    json_2 = sys.argv[2]
    output_dir = sys.argv[3]

    print json_1, json_2, output_dir

    #sampling
    pj = CreateTrain(json_1, json_2, output_dir)
    pj.sampleHD()
    pj.sampleSD()

    

