from  multiprocessing import Pool
import os
import json
import os
import librosa
import numpy as np

comId = 9   # 示例数据
poolNum = 8  # 进程池大小


beatMod = 4
musicClip = 16
need_Refresh = True
X = []     # embedded数据
Y = []     # label数据

def get_audio_features(x, sr, bpm, position, offset):
    one_beat = 60 / bpm
    beat = position * one_beat / beatMod - offset/1000
    start = beat
    end = start + one_beat / (beatMod)
    if start < 0:
        start = 0
    start_index = int(sr * start)
    end_index = int(sr * end)
    
    features = []
    mfcc1 = librosa.feature.mfcc(y=x[start_index:end_index], sr=sr, n_mfcc=32)
    features += [float(np.mean(e)) for e in mfcc1]
    
    return features

def createAttrIndex():
    AttrIndex = []
    for index in range (0, 4):
        for layer in range (0, 3):
            for _type in range(0, 4):
                for direction in range(0, 9):
                    attrMap = {
                        "index": index,
                        "layer": layer,
                        "_type": _type,
                        "direction": direction
                    }
                    AttrIndex.append(attrMap)
    return AttrIndex


def findAttrIndex(index, layer, _type, direction, AttrIndex):
    for i in range(0, len(AttrIndex)):
        if (AttrIndex[i]["index"] == index) and (AttrIndex[i]["layer"] == layer) and (AttrIndex[i]["_type"] == _type) and (AttrIndex[i]["direction"] == direction):
            return i + 1
    return -1


def get_columns_list(notes, AttrIndex):
    columns = {}
    maxPos = 0
    for note in notes:
        beat = note['_time']
        _lineIndex = note['_lineIndex'] # 0、1、2、3
        _lineLayer = note['_lineLayer'] # 0、1、2
        _type = note['_type'] # 0, 1, 2, 3
        _direction = note['_cutDirection'] # 0-8 
        position = int(beat * beatMod)
        index = findAttrIndex(_lineIndex, _lineLayer, _type, _direction, AttrIndex)
        if index == -1:  # 数据格式不规范，超出现有范围
            return {}, -1
        columns[position] = index
        if (position > maxPos):
            maxPos = position

    return columns, maxPos


def get_one_data(start, end, columns, bpm, x_, sr, offset):
    x = []  # MFCC
    y = []  # label
    for i in range(start, end):
        audio_features = get_audio_features(x_, sr, bpm, i, offset)
        x.append(audio_features)
        
        if i in columns.keys():
            y.append(columns[i])
        else:
            y.append(0) # 尝试将数据补足，保证每一个X的时间序列都有对应的Y
        
    return x, y

def task(zip_file, count):
    AUDIOFILE_DIR_STR = "./audiofile/"
    jsonDirPath = "./jsonfile" + str(comId)

    if (not os.path.exists(jsonDirPath)):
        os.makedirs(jsonDirPath)

    with open(AUDIOFILE_DIR_STR + zip_file, "r") as f:
        try:
            data = json.load(f)
        except:
            print(f'RETURN ----------- ERROR JISONFILE mcz_file: {zip_file}, count: {count}')
            return
        else:
            pass
        
    AttrIndex = createAttrIndex()
    
    notes = data["notes"]
    notes = notes[:len(notes)-1]
    audio_x =  np.array(data["x"])
    audio_sr = data["sr"]
    bpm = data["bpm"]
    offset = data["offset"]
    columns_list, maxPos= get_columns_list(notes, AttrIndex)
    
    if maxPos ==  -1:
        print(f'RETURN ############### DATA ERROR : {zip_file}, count: {count}')
        return

    _now = 0
    src = []
    label = []
    clipNum = beatMod * musicClip
    while (_now + clipNum) < maxPos:
        x, y = get_one_data(_now, _now + clipNum, columns_list, bpm, audio_x, audio_sr, offset)
        src.append(x)
        label.append(y)
        _now += clipNum

    jsonPath = jsonDirPath + "/dataset" + str(count) + ".json"
    if(os.path.isfile(jsonPath)):
        if (need_Refresh):
            os.remove(jsonPath)
    with open(jsonPath, "w") as f:
        json.dump({
            "X": src,
            "Y": label,
        }, f)
    print(f'dump json : {jsonPath}')
    
if __name__=='__main__':
    pool = Pool(poolNum)
    
    count = 0
    zip_files = os.listdir("./audiofile/")
    for zip_file in zip_files:
        if ".json" in zip_file:
            count += 1
            pool.apply_async(func = task, args=(zip_file, count,))
            # task(zip_file, count,)
        
    pool.close()
    pool.join()

    print('DONE!')
