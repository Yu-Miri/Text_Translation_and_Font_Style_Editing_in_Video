import os
import cv2
import re
import urllib.request
import easyocr
import json


    
def get_points_texts(frame_path, reader, conf_threshold = 0.4):
    # easyocr
    results = reader.readtext(frame_path)

    # confidence filtering
    conf_idx = [idx for idx in range(len(results)) if results[idx][2] > conf_threshold]
    results = [results[i] for i in conf_idx]

    # 정규표현식 filtering
    re_idx = [idx for idx in range(len(results)) if re.findall('[가-힣]+', results[idx][1])]
    results = [results[i] for i in re_idx]

    # bbox point 얻기
    points = []
    for i in range(len(results)):
        point = results[i][0]
        x_min = int(point[0][0])
        y_min = int(point[0][1])
        x_max = int(point[1][0])
        y_max = int(point[2][1])
        width = x_max - x_min
        height = y_max - y_min 

        crop_point = [x_min, y_min, width, height]
        points.append(crop_point)
    
    # recognized text 얻기
    texts = []
    for i in range(len(results)):
        text = results[i][1]
        texts.append(text)
        
    return points, texts 


def papago_api(client_id,client_secret, ko_word):
    client_id=client_id
    client_secret=client_secret
    encText = urllib.parse.quote(ko_word)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        decode=json.loads(response_body.decode('utf-8'))
        word=decode['message']['result']['translatedText']
        return word
    else:
        return print("Error Code:" + rescode)
    
    
