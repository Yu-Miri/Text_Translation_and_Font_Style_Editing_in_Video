from pipeline_utils import get_points_texts
from pipeline_utils import papago_api
import easyocr
import glob
import cv2
import os
import pickle


class mostel_input():

    def __init__(self, video_name):
        self.reader = easyocr.Reader(['ko'])
        self.video_name = video_name
        
    def make_input(self):
        # 업로드 frame 가져오기
        upload_file_dir = sorted(glob.glob(f'static/uploads/{self.video_name}/frames/input/**'))

        for frame_path in upload_file_dir:

            # OCR 통한 BBox point와 text 얻기
            points, texts = get_points_texts(frame_path, reader = self.reader)

            # image도 로드
            img = cv2.imread(frame_path)

            # 각 frame 마다 폴던 만들기
            frame_folder_path = os.path.join(f'static/uploads/{self.video_name}/auto/input', frame_path.rsplit('/', 1)[-1][:-4])
            if not os.path.exists(frame_folder_path):
                os.mkdir(frame_folder_path)
                os.mkdir(frame_folder_path + '/i_s')


            # i_s 경로
            crop_root = frame_folder_path
            i_s_dir = os.path.join(frame_folder_path, 'i_s')

            # crop_image 얻기
            for i, crop_point in enumerate(points):
                x_min, y_min, width, height = crop_point
                crop = img[y_min:y_min+height, x_min:x_min+width]
                crop_name = os.path.join(i_s_dir, f'{str(i).zfill(4)}.png')
                cv2.imwrite(crop_name, crop)
                
                # 각 crop이미지의 좌표값 pickle로 저장
                pickle_name = os.path.join(crop_root, f'{str(i).zfill(4)}.pickle')
                with open(pickle_name, 'wb') as f:
                    pickle.dump(crop_point, f)
                    
                    
            # papago api를 통한 해석
            eng_lst = []
            for text in texts:
                en_word = papago_api(client_id = 'xnMNujqDWGpaydIvrogd', client_secret = "y920EttA4q", ko_word= text)
                eng_lst.append(en_word)
                
            # i_t.txt 만들기
            i_s_names = sorted(os.listdir(i_s_dir))
            i_t_name = os.path.join(crop_root, 'i_t.txt')

            f = open(i_t_name, 'w')
            for name, eng in zip(i_s_names, eng_lst):
                data = name + ' ' + eng + '\n'
                f.write(data)
            f.close()


        

