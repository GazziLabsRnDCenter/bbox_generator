'''
    addData.py
    
    Copyright 2021 by GazziLabs Co.,Ltd.
    All rights reserved.
    
    This tool calculates and generates bounding box coordinates from polygon coordinates
    in JSON metadata for the NIA PET DISEASE data set.
    
    See README.md to run the tool.
'''

import json
import sys
from argparse import ArgumentParser
from os import makedirs, walk
from os.path import isdir, join, exists, splitext

def main():
    # Argument 처리
    parser = ArgumentParser(description = 'Process NIA_PET Add BoundingBox')
    parser.add_argument('SrcPath', type=str, nargs=1) #입력경로
    parser.add_argument('DstPath', type=str, nargs=1) #목적경로
    args = parser.parse_args()

    if not isdir(args.SrcPath[0]):
      print("ERROR> Invalid path")
      return
    
    srcPath = args.SrcPath[0]
    dstPath = args.DstPath[0]

    #목적경로 폴더 생성
    for (root, dirs, files) in walk(srcPath): 
        subdir_name = ""
        output_target_path = dstPath
        if srcPath != root:
            subdir_name = root.replace(srcPath, "")
            output_target_path = dstPath + subdir_name 
            if not exists(output_target_path):
                makedirs(output_target_path)

        if len(files) > 0:
            for filename in files:
                name, ext = splitext(filename)
                if ext.lower() == '.json':
                    jsonPath = join(root, filename)
                    newJsonPath = join(output_target_path, name)
                    saveJson(jsonPath, newJsonPath)

#BoundingBodx 추가 후 json 저장
def saveJson(jsonPath, newJsonPath):
    with open(jsonPath, "r", encoding="UTF-8") as json_file:
        dictionary = json.load(json_file)
    
    try:
        len_label = len(dictionary['labelingInfo'])
        metaData = {}
        metaData['metaData'] = dictionary['metaData']
        metaData['inspRejectYn'] = dictionary['inspRejectYn']
        metaData['labelingInfo'] = []
    except:
        print(jsonPath + " jsonError")
        sys.exit(0)
    
    for index in range(len_label):    
        try:
            poly = dictionary['labelingInfo'][index]['polygon']['location'][0]
            len_poly = len(poly) // 2 + 1
        except:
            print(jsonPath + " jsonError")
            sys.exit(0)

        y_list = []
        x_list = []

        for i in range(1, len_poly):
            y_value = dictionary['labelingInfo'][index]['polygon']['location'][0]['y{0}'.format(i)]
            x_value = dictionary['labelingInfo'][index]['polygon']['location'][0]['x{0}'.format(i)]
            y_list.append(int(y_value))
            x_list.append(int(x_value))
        
        Xmin = min(x_list)
        Xmax = max(x_list)
        Ymin = min(y_list)
        Ymax = max(y_list)

        polygon = dictionary['labelingInfo'][index]['polygon']
        metaData['labelingInfo'].append({'polygon' : polygon})
        AddData = metaData['labelingInfo'][index]

        #기존의 json 파일에 boundingbox가 있는 경우
        if 'boundingBox' in dictionary['labelingInfo'][index].keys():
            boundingbox = dictionary['labelingInfo'][index]['boundingBox']
            metaData['labelingInfo'][index]['boundingBox'] = boundingbox
            
        else:
            location = {"location": [{"Xmin": Xmin ,"Ymin" : Ymin, "Xmax" : Xmax, "Ymax" : Ymax}]}
            AddData['boundingBox'] = location
     

        AddData['boundingBox']['label'] = dictionary['labelingInfo'][index]['polygon']['label']
        AddData['boundingBox']['type'] = "box"
            
    with open(newJsonPath + ".json", "w", encoding="UTF-8") as outfile:
        outfile.write(json.dumps(metaData, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()