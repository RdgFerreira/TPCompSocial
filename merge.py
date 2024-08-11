import json
from os import listdir
from os.path import isfile, join

files = [f"memes/{f}" for f in listdir("memes") if isfile(join("memes", f))]


def merge_JsonFiles(filenames):
    result = list()
    for f1 in filenames:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('memes40001-50000.json', 'w') as output_file:
        json.dump(result, output_file)


merge_JsonFiles(files)
