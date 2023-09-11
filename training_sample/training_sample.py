import numpy as np
from PIL import Image
from pathlib import Path

def img_cnvrt(path: str):
    img = Image.open(path)
    img.load()
    arr = np.asarray(img.convert('1'), dtype='int32')
    l = list()
    for j in range(len(arr)):
        l = l + list(arr[j])
    return l

def ts_init(path:str):
    input_folder = Path(path + '/input')
    ts = list()
    input_bin_img = list()
    for i in range(len(list(input_folder.iterdir()))):
        set_folder = Path(path + f'/input/set{i}')
        input_bin_img.append(list())
        for j in range(len(list(set_folder.iterdir()))):
            input_bin_img[i].append(img_cnvrt(path + f'/input/set{i}/{j}.png'))
    ts.append(input_bin_img)
    out_f = open(path + '/output.txt')
    out_v = list()
    while 1:
        line = out_f.readline()
        if line:
            out_v.append(list((int(x) for x in line[:-1])))
        else:
            break
    ts.append(out_v)
    return ts

def test():
    file = open('lab1/training_sample\output.txt')
    out = list()
    while 1:
        line = file.readline()
        if line:
            out.append(list((int(x) for x in line[:-1])))
        else:
            break
    print(out)
