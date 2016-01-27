import json, os, sys
import shutil
import random

class ParseJson:

    """

    ParseJson is a class to copy selected frames in src path to dest path.
    __range is the number of frames that will be selected in each race.

    usage:
        ParseJson(path_to_json, path_to_output_directory)

    """
    #private variables
    __image_root = "\\\\ws-qvl016\\Frames - Hong Kong HD"
    __range = 0
    __json_fp = ""
    __output_dir = ""

    #constructor
    def __init__(self, js_f, dest):
        if os.path.exists(js_f):           
           self.__json_fp = js_f
        else:
            print "Json file does not exists"

        if os.path.exists(dest):
            shutil.rmtree(dest)
            os.mkdir(dest)
        else:
            os.mkdir(dest)

        self.__output_dir = dest

    #change root dir
    def setroot(self, root):
        self.__image_root = root

    #sample starting frames
    def samplestart(self, rate = 10):
        self.__range = rate
        with open(self.__json_fp, 'r') as f:
            data = json.load(f)
            for d in data:
                src_dir = os.path.join(self.__image_root, d['Track'], str(d['Date']), d['VideoName'])

                #sample the frames at the starting frames
                leftbound = d['StartingFrame'] - self.__range / 2
                rightbound = d['StartingFrame'] + self.__range / 2

                if leftbound < 0:
                    leftbound = 0

                n_frm = [x for x in xrange(leftbound, rightbound, 1)]
                img_fn = ['img%.6d.jpg' % x for x in n_frm]
                
                #concatenate paths to make absolute paths
                from_fn = map(lambda x: os.path.join(src_dir, x), img_fn)

                #create output format
                out_fn = map(lambda x: '-'.join([d['Track'], str(d['Date']), d['VideoName'], x]), img_fn)
                to_fn = map(lambda x: os.path.join(self.__output_dir, x), out_fn)

                #perform shuffling
                if len(from_fn) == len(to_fn):
                    result = zip(from_fn, to_fn)
                    for (p1, p2) in result:
                        shutil.copy(p1, p2)
                else:
                    print "Length of from_fn and to fn is not equal !!!"


    #sample finishing frames
    def samplefinish(self, rate = 10):
        self.__range = rate
        with open(self.__json_fp, 'r') as f:
            data = json.load(f)
            for d in data:
                src_dir = os.path.join(self.__image_root, d['Track'], str(d['Date']), d['VideoName'])

                #sample the frames at the Finishing frames
                leftbound = d['FinishingFrame'] - self.__range / 2
                rightbound = d['FinishingFrame'] + self.__range / 2

                if leftbound < 0:
                    leftbound = 0

                n_frm = [x for x in xrange(leftbound, rightbound, 1)]
                img_fn = ['img%.6d.jpg' % x for x in n_frm]
                
                #concatenate paths to make absolute paths
                from_fn = map(lambda x: os.path.join(src_dir, x), img_fn)

                #create output format
                out_fn = map(lambda x: '-'.join([d['Track'], str(d['Date']), d['VideoName'], x]), img_fn)
                to_fn = map(lambda x: os.path.join(self.__output_dir, x), out_fn)

                #perform shuffling
                if len(from_fn) == len(to_fn):
                    result = zip(from_fn, to_fn)
                    for (p1, p2) in result:
                        shutil.copy(p1, p2)
                else:
                    print "Length of from_fn and to fn is not equal !!!"

    #sample random frames
    def samplerandom(self, rate = 10, step = 10):
        self.__range = rate
        with open(self.__json_fp, 'r') as f:
            data = json.load(f)
            for d in data:
                src_dir = os.path.join(self.__image_root, d['Track'], str(d['Date']), d['VideoName'])

                #sample the frames at the starting frames
                p = (d['FinishingFrame'] - d['StartingFrame']) / self.__range
                leftbound = d['StartingFrame'] + p
                rightbound = d['FinishingFrame'] - p 

                n_frm = [random.randrange(leftbound, rightbound, step) for x in range(rate)]
                img_fn = ['img%.6d.jpg' % x for x in n_frm]
                
                #concatenate paths to make absolute paths
                from_fn = map(lambda x: os.path.join(src_dir, x), img_fn)

                #create output format
                out_fn = map(lambda x: '-'.join([d['Track'], str(d['Date']), d['VideoName'], x]), img_fn)
                to_fn = map(lambda x: os.path.join(self.__output_dir, x), out_fn)

                #perform shuffling
                if len(from_fn) == len(to_fn):
                    result = zip(from_fn, to_fn)
                    for (p1, p2) in result:
                        shutil.copy(p1, p2)
                else:
                    print "Length of from_fn and to fn is not equal !!!"

if __name__ == '__main__':
    input_fn = sys.argv[1]
    output_dir = sys.argv[2]

    print input_fn, output_dir

    pj = ParseJson(input_fn, output_dir)
    pj.samplerandom(10, 50)

