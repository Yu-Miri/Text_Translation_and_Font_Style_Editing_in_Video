from mostel import tps_spatial_transformer,model, standard_text
from mostel import web_predict
import pickle
import glob
import cv2
import os

class mostel_output():
    def __init__(self, video_name):
        self.video_name = video_name

    def main(self):

        # mostel inference 하기
        config = 'mostel/configs/mostel-train.py'
        checkpoint = 'mostel/checkpoint/train_step-160000.model'

        input_path = sorted(glob.glob(f'static/uploads/{self.video_name}/auto/input/**/i_s'))
        
        # save_dir 각 frame 만들기
        upload_file_dir = sorted(glob.glob(f'static/uploads/{self.video_name}/frames/input/**'))
        for input_dir, frame_path in zip(input_path, upload_file_dir):
            frame_folder_path = os.path.join(f'static/uploads/{self.video_name}/auto/output', frame_path.rsplit('/', 1)[-1][:-4])
            if not os.path.exists(frame_folder_path):
                os.mkdir(frame_folder_path)

            input_dir = input_dir
            save_dir = frame_folder_path
            f = web_predict.style_transfer(config = config, input_dir = input_dir, save_dir = save_dir, 
                            checkpoint = checkpoint, slm = True, dilate = True)

            f.main()

        # upload 이미지 갖고 오기
        upload_path = sorted(glob.glob(f'static/uploads/{self.video_name}/frames/input/**'))

        for frame_img in upload_path:
            img = cv2.imread(frame_img)

            frame_name = frame_img.rsplit('/', 1)[-1][:-4]

            # 각 point path 가져오기
            point_path = sorted(glob.glob(f"static/uploads/{self.video_name}/auto/input/{frame_name}/*.pickle"))
            # style바뀐 이미지 path 가져오기
            output_path = sorted(glob.glob(f'static/uploads/{self.video_name}/auto/output/{frame_name}/**'))
            # i_s image path 가져오기
            i_s_path = sorted(glob.glob(f'static/uploads/{self.video_name}/auto/input/{frame_name}/i_s/**'))

            for p_path, o_path, i_path in zip(point_path, output_path, i_s_path):
                # point 추출
                with open(p_path, 'rb') as f:
                    x_min, y_min, width, height = pickle.load(f)

                # output_crop img     
                crop_img = cv2.imread(o_path)

                # i_s이미지로 resize
                i_s_img = cv2.imread(i_path)
                i_s_size = (i_s_img.shape[1], i_s_img.shape[0])
                #print(crop_img.shape, i_s_size)
                crop_img = cv2.resize(crop_img, dsize = i_s_size, interpolation = cv2.INTER_LINEAR)
                #print(crop_img.shape, i_s_size)

                img[y_min: y_min+height, x_min:x_min+width] = crop_img

            filename = os.path.join(f'static/uploads/{self.video_name}/frames/output', frame_name + '.png')
            cv2.imwrite(filename, img)

        # output frmae으로 video 만들기
        output_frames_path = sorted(glob.glob(f'static/uploads/{self.video_name}/frames/output/**'))
        frames = []
        for output_frame in output_frames_path:
            frame = cv2.imread(output_frame)
            frames.append(frame)

        upload_path = glob.glob(os.path.join(f'static/uploads/{self.video_name}/videos/input', '**'))[0]
        upload_name = upload_path.split('/')[-1]
        output_video_path = f'static/uploads/{self.video_name}/videos/auto/{upload_name}'
        frame_width, frame_height = frames[0].shape[1], frames[0].shape[0]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

        for frame in frames:
            out.write(frame)
        out.release()
                


        
