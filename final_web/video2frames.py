import glob
import os
import cv2


class video2frames():
    def __init__(self, video_name):
        self.video_name = video_name

    def make_frame(self):
        # 업로드 된 영상 path
        videos_input_path = glob.glob(os.path.join(f'static/uploads/{self.video_name}/videos/input', '**'))[0] # 업로드 될 때 하나의 비디오만 있다는 가정하에 작성
        # video를 frame 단위 자르기
        vidcap = cv2.VideoCapture(videos_input_path)
        frames = []
        while True:
            success, image = vidcap.read()
            if not success:
                break
            frames.append(image)
        vidcap.release()


        # frame 이미지 저장경로 지정
        frames_input_path = f'static/uploads/{self.video_name}/frames/input'
        # frame 이미지들 저장
        for idx, frame in enumerate(frames):
            frame_name = str(idx).zfill(4)
            save_path = os.path.join(frames_input_path, f"{frame_name}.png")
            cv2.imwrite(save_path, frame)