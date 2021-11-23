# Calculates and Generates Bounding Boxes Coordinates from the Polygonal Coordinates in JSON Metadata   

이 유틸리티는 2021년 인공지능 학습 데이터 구축 사업의 반려동물 피부질환 데이터에 대하여 JSON 메타데이터의 polygon 정보로부터 bounding box 정보를 생성, 추가합니다.   

본 유틸리티의 저작권은 (주)가치랩스(http://gazzi.ai)에 있습니다.   
본 프로그램 구동에 필요한 Python 및 부가 라이브러리 각각은 저작권자의 권리를 따릅니다.   

## CMD 실행 방법
```
python addData.py 입력경로 출력경로
```

## 설치해야 할 모듈
1. python version : 3.9.6
2. python -m pip install --upgrade pip
2. python -m pip install argparse

## ERROR
```
json 데이터에 오류가 있을시, 파일명 출력과 함께 프로그램이 종료됩니다. 
파일명에 맞는 json 파일을 확인하시고 올바른 데이터를 입력 후 다시 프로그램을 실행시키시면 됩니다.
```

**발견된 오류**
1. json 데이터 오류
2. 이미 boundingBox가 있는 경우
boundingBox가 있을 경우, 아래의 항목을 추가하여 저장했습니다.

-------------------------------
"label": "A1_구진/플라크",
"type": "box"


## BoundingBox의 형태 예시)
```
{
    "boundingBox": {
    "location": [
        {
        "Xmin": 465,
        "Xmax": 550,
        "Ymin": 235,
        "Ymax": 290
        }
    ],
    "label": "A1_구진/플라크",
    "type": "box"
    }
}
```
