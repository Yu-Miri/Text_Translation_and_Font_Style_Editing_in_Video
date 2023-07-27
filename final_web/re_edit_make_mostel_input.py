import glob
import cv2
import os
import json


class mostel_input():

    def __init__(self, video_name, current_frame):
        self.video_name = video_name
        self.current_frame = current_frame
        
    def make_input(self):
     
        config_path = f'static/uploads/{self.video_name}/edit/config.json'
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)

        x_min = int(min([float(config['LABELS'][i]['x']) for i in range(4)]))
        x_max = int(max([float(config['LABELS'][i]['x']) for i in range(4)]))
        y_min = int(min([float(config['LABELS'][i]['y']) for i in range(4)]))
        y_max = int(max([float(config['LABELS'][i]['y']) for i in range(4)]))

        text = config['TEXT']
        # input_frame_path를 가져오기
        input_frame_path = os.path.join(f'static/uploads/{self.video_name}/frames/output', self.current_frame)

        # image도 로드
        img = cv2.imread(input_frame_path)

        # i_s 경로
        crop_root = f'static/uploads/{self.video_name}/edit/re_edit/input'
        i_s_dir = os.path.join(crop_root, 'i_s')

        # crop 이미지 저장
        crop = img[y_min:y_max, x_min:x_max]
        crop_name = os.path.join(i_s_dir, '0000.png')
        cv2.imwrite(crop_name, crop)

        # i_t.txt 만들기
        i_s_name = '0000.png'
        i_t_name = os.path.join(crop_root, 'i_t.txt')

        f = open(i_t_name, 'w')
        f.write(i_s_name + ' ' + text)
        f.close()


        

