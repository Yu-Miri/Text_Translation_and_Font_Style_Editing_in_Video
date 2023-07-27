import remove_edit_make_mostel_input
import remove_edit_make_output

# video_name = 'theglory'
# current_frame = '0003.png'
def inference(video_name, current_frame):

  input = remove_edit_make_mostel_input.mostel_input(video_name = video_name, current_frame=current_frame)
  input.make_input()

  output = remove_edit_make_output.mostel_output(video_name = video_name, current_frame=current_frame)
  output.main()

