import os
import json

comId = 9

JSONDIR = "./jsonfile" + str(comId) + "/"
json_files = os.listdir(JSONDIR)

X = []
Y = []

def handleAllFile():
    X.clear()
    Y.clear()
    OUTDIR = "./out" + str(comId) + "/"
    if (not os.path.exists(OUTDIR)):
        os.makedirs(OUTDIR)

    maxCnt = len(json_files)
    for i in range (maxCnt):
        jsonPath = JSONDIR + "dataset" + str(i + 1) + ".json"
        if(os.path.isfile(jsonPath)):
            with open(jsonPath, "r") as f:
                dataset = json.load(f)
                for i in range (len(dataset['X'])):
                    X.append(dataset['X'][i])
                for i in range (len(dataset['Y'])):
                    Y.append(dataset['Y'][i])
                
    with open(OUTDIR + "datasetAll"+ str(comId) + ".json", "w") as f:
            json.dump({
                "X": X,
                "Y": Y,
            }, f)

    # malody

    with open(OUTDIR + "malody.txt", "w") as f:
        for y in Y:
            strs = [str(i) for i in y]
            line = " ".join(strs)
            f.write(line + "\n")

if __name__=='__main__':
    handleAllFile()
    print('DONE!')            
