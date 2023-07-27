import glob
import os
import cv2


class frames2video():
    def __init__(self, video_name):
        self.video_name = video_name

    def make_video(self):
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
        out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame_width, frame_height))

        for frame in frames:
            out.write(frame)
        out.release()
                

# import frames2video

# a = frames2video.frames2video('사모님')
# a.make_video()