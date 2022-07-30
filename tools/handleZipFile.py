from  multiprocessing import Process,Pool
import os
import json
import zipfile
import os
import librosa

poolNum = 8

def load_audio(audio_file):
    x , sr = librosa.load(audio_file, sr=20000)
    return x, sr

def task(zip_file, count):
    # config
    MUSIC_DIR_STR = "./musicDir/"               # 解压后的文件路径
    AUDIOFILE_DIR_STR = "./audiofile/"          # librosa.load 处理后的文件路径
    ZIPFILE_DIR_STR = "./original_beatmaps/"    # 原始zip文件路径
    zFile = ""
    try:
        zFile = zipfile.ZipFile(ZIPFILE_DIR_STR + zip_file, "r")
    except:
        print(f'RETURN ----------- ERROR ZIPFILE zip_file: {zip_file}, count: {count}')
        return
    else:
        pass

    if (zFile == ""):
        print(f'RETURN ----------- ERROR ZIPFILE is null: {zip_file}, count: {count}')
        return

    audio_file = ""
    info_data = {}
    mc_data = {}
    offset = 0
    beatMapFileName = ""
    dirPath = MUSIC_DIR_STR + zip_file
    if (not os.path.exists(dirPath)):
        os.makedirs(dirPath)

    for fileM in zFile.namelist():
        zFile.extract(fileM, dirPath)
        if "info.dat" in fileM:
            data = zFile.read(fileM).decode("utf-8")
            info_data = json.loads(data)
            bpm = info_data["_beatsPerMinute"]
            offset = info_data["_songTimeOffset"]
            difficultSets = info_data["_difficultyBeatmapSets"]
            for mmap in difficultSets:
                if (mmap["_beatmapCharacteristicName"] == "Standard"):
                    beatMapFileName = mmap["_difficultyBeatmaps"][0]["_beatmapFilename"]
                    break

    if beatMapFileName == "":
        print(f'RETURN ----------- ERROR no Standard difficult level: {zip_file}, count: {count}')
        return

    for fileM in zFile.namelist():
        zFile.extract(fileM, dirPath)
        if beatMapFileName in fileM:
            data = zFile.read(fileM).decode("utf-8")
            mc_data = json.loads(data)
        elif ".egg" in fileM:
            audio_file = fileM
        elif ".mp3" in fileM:
            audio_file = fileM

    notes = mc_data["_notes"]
    notes = notes[:len(notes)-1]  

    '''
    TODO : 目前只处理了 notes 的数据，还需要处理  _obstacles _events 数据，以便后续的模型学习处理。
    '''

    if (not os.path.exists(AUDIOFILE_DIR_STR)):
        os.makedirs(AUDIOFILE_DIR_STR)

    jsonPath = AUDIOFILE_DIR_STR + zip_file + ".json"
    if(os.path.isfile(jsonPath)):
        print(f'RETURN ----------- file had been handled: {zip_file}, count: {count}')
        return

    x_, sr = load_audio(dirPath + "/" + audio_file)
    
    with open(jsonPath, "w") as f:
        json.dump({
            "x": x_.tolist(),
            "sr": sr,
            "notes": notes,
            "offset":offset,
            "bpm": bpm,
        }, f)

    print(f'dump json : {jsonPath},count: {count}')
    
if __name__=='__main__':
    pool = Pool(poolNum)
    zip_files = os.listdir("original_beatmaps")
    count = 0
    for zip_file in zip_files:
        if ".zip" in zip_file:
            count += 1
            pool.apply_async(func = task, args=(zip_file, count,))
        
    pool.close()
    pool.join()
  
    print('DONE!')