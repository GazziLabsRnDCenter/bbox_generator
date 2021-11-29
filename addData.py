import json
import os
import os.path

from argparse import ArgumentParser

def main():
    # Argument 처리
    parser = ArgumentParser(description = 'Process NIA_PET Add BoundingBox')
    parser.add_argument('SrcPath', type=str, nargs=1) #입력경로
    parser.add_argument('DstPath', type=str, nargs=1) #목적경로
    args = parser.parse_args()

    if not os.path.isdir(args.SrcPath[0]):
      print("ERROR> Invalid path")
      return
    
    srcPath = args.SrcPath[0]
    dstPath = args.DstPath[0]
 
        #목적경로 폴더 생성
    for (root, dirs, files) in os.walk(srcPath):

        # 통계용 리스트
        breed_count = {}
        age_count = {}
        species_count = {}
        region_count = {} 

        subdir_name = ""
        output_target_path = dstPath
        if srcPath != root:
            subdir_name = root.replace(srcPath, "")
            output_target_path = dstPath + subdir_name 
            if not os.path.exists(output_target_path):
                os.makedirs(output_target_path)   
            try:
                if len(files) > 0:
                    for filename in files:
                        name, ext = os.path.splitext(filename)
                        if ext.lower() == '.json':
                            jsonPath = os.path.join(root, filename)
                            newJsonPath = os.path.join(output_target_path, name)
                            breed_count, age_count, species_count, region_count = saveJson(jsonPath, newJsonPath, breed_count, age_count, species_count, region_count)
            except Exception as e:
                break
            
            finally:
                with open(output_target_path + os.sep + "{}_count.txt".format(subdir_name), "w", encoding="UTF-8") as countfile:
                    countfile.write(f"BREED: {breed_count}\n")
                    countfile.write(f"AGE: {age_count}\n")
                    countfile.write(f"SPECIES: {species_count}\n")
                    countfile.write(f"REGION: {region_count}\n")
                    

#BoundingBodx 추가 후 json 저장
def saveJson(jsonPath, newJsonPath, breed_count, age_count, species_count, region_count):
    with open(jsonPath, "r", encoding="UTF-8") as json_file:
        dictionary = json.load(json_file)

    try:
        len_label = len(dictionary['labelingInfo'])
        metaData = {}
        metaData['metaData'] = dictionary['metaData']
        metaData['inspRejectYn'] = dictionary['inspRejectYn']
        metaData['labelingInfo'] = []
    except Exception as e:
        print(jsonPath + " jsonError")
        raise e
    
    #통계 데이터 추가
    breed = metaData['metaData']['breed']
    if breed not in breed_count:
        breed_count[breed] = 1
    else:
        breed_count[breed] += 1

    age = metaData['metaData']['age']
    if age not in age_count:
        age_count[age] = 1
    else:
        age_count[age] += 1
    
    species = metaData['metaData']['species']
    if species not in species_count:
        species_count[species] = 1
    else:
        species_count[species] += 1

    region = metaData['metaData']['region']
    if region not in region_count:
        region_count[region] = 1
    else:
        region_count[region] += 1

    for index in range(len_label):    
        try:
            poly = dictionary['labelingInfo'][index]['polygon']['location'][0]
            len_poly = len(poly) // 2 + 1
        except Exception as e:
            print(jsonPath + " jsonError")
            raise e

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

        #추가 데이터가 있는 경우 
        """ 
        metaData['BasicInfo'] = {}
        metaData['BasicInfo']["identifier"] = "피부질환"
        metaData['BasicInfo']["src_path"] = 경로
        metaData['BasicInfo']["lable_path"] = 경로
        metaData['BasicInfo']["type"] = "json"
        metaData['BasicInfo']["fileformat"] = "jpg"
        """ 

    with open(newJsonPath + ".json", "w", encoding="UTF-8") as outfile:
        outfile.write(json.dumps(metaData, indent=2, ensure_ascii=False))

    return breed_count, age_count, species_count, region_count

if __name__ == "__main__":
    main()