from mostel import tps_spatial_transformer,model, standard_text
from mostel import web_predict
import json
import glob
import cv2
import os


class mostel_output():
    def __init__(self, video_name, current_frame):
        self.video_name = video_name
        self.current_frame = current_frame
    def main(self):

        # mostel inference 하기
        config = 'mostel/configs/mostel-train.py'
        checkpoint = 'mostel/checkpoint/train_step-160000.model'

        input_dir = f'static/uploads/{self.video_name}/edit/re_edit/input/i_s'
        save_dir = f'static/uploads/{self.video_name}/edit/re_edit/output'
        f = web_predict.style_transfer(config = config, input_dir = input_dir, save_dir = save_dir, 
                        checkpoint = checkpoint, slm = True, dilate=True)

        f.main()


        output_frame_path = f'static/uploads/{self.video_name}/frames/output/{self.current_frame}'
        img = cv2.imread(output_frame_path)

        # 각 point path 가져오기
        config_path = f'static/uploads/{self.video_name}/edit/config.json'
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)

        x_min = int(min([float(config['LABELS'][i]['x']) for i in range(4)]))
        x_max = int(max([float(config['LABELS'][i]['x']) for i in range(4)]))
        y_min = int(min([float(config['LABELS'][i]['y']) for i in range(4)]))
        y_max = int(max([float(config['LABELS'][i]['y']) for i in range(4)]))

        # style바뀐 이미지 path 가져오기
        output_path = f'static/uploads/{self.video_name}/edit/re_edit/output/0000.png'
        # i_s image path 가져오기
        i_s_path = f'static/uploads/{self.video_name}/edit/re_edit/input/i_s/0000.png'

        # output_crop img     
        crop_img = cv2.imread(output_path)

        # i_s이미지로 resize
        i_s_img = cv2.imread(i_s_path)
        i_s_size = (i_s_img.shape[1], i_s_img.shape[0])
        crop_img = cv2.resize(crop_img, dsize = i_s_size, interpolation = cv2.INTER_LINEAR)

        img[y_min: y_max, x_min:x_max] = crop_img

        cv2.imwrite(output_frame_path, img)

                


        
