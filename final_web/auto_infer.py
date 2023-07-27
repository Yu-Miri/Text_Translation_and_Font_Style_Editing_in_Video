import video2frames
import auto_make_mostel_input
import auto_make_output

# video_name = 'theglory'

def inference(video_name):

  video_frame = video2frames.video2frames(video_name)
  video_frame.make_frame()

  input = auto_make_mostel_input.mostel_input(video_name)
  input.make_input()

  output = auto_make_output.mostel_output(video_name)
  output.main()

