from flask import Flask, render_template, flash
from flask import request, redirect, url_for, send_file #get post 하려면 필수
import pymysql
from PIL import Image
import os
from werkzeug.utils import secure_filename
import cv2
import time
import json
import shutil
import glob

import auto_infer
import remove_edit_infer
import re_edit_infer
import frames2video

# from flask_dropzone import Dropzone

# ======= Mostel 모델 class 입력======

# ==================================

app = Flask(__name__)


db_conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'alpaco4',
    passwd = '1234',
    db = 'test',
    charset = 'utf8'
)

    
@app.route('/')
def main():
    return render_template('main.html')


id = ''
pwd = ''

# 앱을 실행시키기 위해 작성
@app.route("/login_check", methods=['POST']) 
def login_check():

    global id
    global pwd

    id = request.form['id']
    pwd = request.form['pwd']

    cursor1 = db_conn.cursor()
    query = f"select * from user_info where user_id like '{id}' and user_pwd like '{pwd}'"
    cursor1.execute(query)
    result = cursor1.fetchall()

    if result:
        cursor = db_conn.cursor()
        query = "SELECT * FROM history_table"
        cursor.execute(query)

        result_table = []
        for i in cursor: # i = (1, datetime.datetime(2023, 6, 19, 20, 25, 26), '기록1', '이미지 저장1') 튜플 형태로 받는다
            temp = {'Version':i[0],'Movie_name':i[1],'Time':str(i[2]).split(" ")[0]}
            result_table.append(temp)

        return render_template('history.html', result_table = result_table)
    else:
        return '''
            <script>
            alert("존재하지 않는 ID 이거나 비밀번호가 일치하지 않습니다.");
            window.location = "/";
            </script>
        '''
    
@app.route('/signup') # 접속하는 URL
def signup():
    return render_template('signup.html')

@app.route('/signup_add', methods=['POST'])
def signup_add():
    id = request.form['id']
    pwd = request.form['pwd']
    phone = request.form['phone']

    if id != '' and pwd != '' and phone != '':
        
        cursor = db_conn.cursor()
        query = f"insert into user_info (user_id, user_pwd, user_phone) values ('{id}','{pwd}','{phone}')"

        cursor.execute(query)
        db_conn.commit()
        return render_template('main.html')
    else:
        return render_template('error.html')

@app.route('/history')
def history():
    # 커서 객체 생성
    cursor = db_conn.cursor()

    query = "select * from history_table"

    cursor.execute(query)
    
    result = []
    for i in cursor: # i = (1, datetime.datetime(2023, 6, 19, 20, 25, 26), '기록1', '이미지 저장1') 튜플 형태로 받는다
        temp = {'Version':i[0],'Movie_name':i[0],'Time':i[2]}
        result.append(temp)
    return render_template('history.html', result_table = result)



ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
UPLOAD_FOLDER = 'static/videos/input' # 원본 프레임들



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def saveVideo(video):
    f_name = secure_filename(video.filename)
    base, ext = os.path.splitext(f_name)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)

    # 파일 형식을 감지한다.
    detected_format = ext[1:].lower()

    # mp4, mov, avi만 저장하도록 한다.
    if detected_format in ALLOWED_EXTENSIONS:
        video.save(save_path)
        return save_path
    else:
        # 이외의 파일은 저장하지 않는다.
        return '업로드 파일 형식을 확인해주세요.'

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('파일을 찾을 수 없습니다.')
            return redirect(request.url)

        video = request.files['file']

        if video.filename == '':
            flash('업로드한 파일을 찾을 수 없습니다.')
            return redirect(request.url)
        if video and allowed_file(video.filename):
            file_name = video.filename # OOO.mp4 or OOO.mov or OOO.avi
            f_name = secure_filename(video.filename) # 파일 형식 이름
            
            # 멘토수정 EasyOCR - Auto 부분 ====================================================================
            filename_folder_name= file_name.split(".")[0] # 사모님
            global folder_name
            folder_name=filename_folder_name
            
            app.config["CURRENT_SHOW"]=f"static/uploads/{folder_name}/frames/output/0000.png"
            global output_directory
            output_directory = f"static/uploads/{folder_name}/frames/output/" 
            
            os.mkdir(f"./static/uploads/{filename_folder_name}")
            
            os.mkdir(f"./static/uploads/{filename_folder_name}/videos")
            os.mkdir(f"./static/uploads/{filename_folder_name}/videos/input") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/videos/auto") # input에 뮤비명으로 폴더 만들고,
            
            os.mkdir(f"./static/uploads/{filename_folder_name}/frames")
            os.mkdir(f"./static/uploads/{filename_folder_name}/frames/input") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/frames/output") # input에 뮤비명으로 폴더 만들고,
            
            os.mkdir(f"./static/uploads/{filename_folder_name}/auto")
            os.mkdir(f"./static/uploads/{filename_folder_name}/auto/input") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/auto/output") # input에 뮤비명으로 폴더 만들고,
            
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit")
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/re_edit") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/re_edit/input") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/re_edit/output") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/re_edit/input/i_s") # input에 뮤비명으로 폴더 만들고,
            
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/remove_edit") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/remove_edit/input") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/remove_edit/output") # input에 뮤비명으로 폴더 만들고,
            os.mkdir(f"./static/uploads/{filename_folder_name}/edit/remove_edit/input/i_s") # input에 뮤비명으로 폴더 만들고,
            
            # 멘토수정 동영상이름폴더 생성 및 그 안에 origin folder 저장 부분 ====================================
            cursor = db_conn.cursor()

            current_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            movie_name = file_name.split(".")[0]
            query = f"insert into history_table (Movie_name, Time) values ('{movie_name}','{current_time}')"

            cursor.execute(query)
            db_conn.commit()
            db_conn.close()
            
            # =============================================================================
            video.save(f"./static/uploads/{filename_folder_name}/videos/input/"+ file_name) # 업로드 파일 저장

            

            auto_infer.inference(filename_folder_name)
            return render_template('display.html', filename_folder_name=filename_folder_name, uploaded_filename=file_name)
        else:
            flash('업로드 파일 형식이 맞지 않습니다.')
            return redirect(request.url)
    else:
        return render_template('upload.html')

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if not filename:
        flash('No filename specified for download')
        return redirect(url_for('upload_image'))

    filename_folder_name=filename.split(".")[0]
    path = f"static/uploads/{filename_folder_name}/videos/auto/{filename}"
    
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        flash('File not found')
        return redirect(url_for('upload_image'))

flag = 0 #2023 06 22수정

@app.route('/edit', methods=['GET'])
def edit_get():
    global flag 

    if flag != 1:
        app.config["LABELS"]=[] #2023 06 22 수정
    flag = 0
    get_filename = request.args.get('filename')
    if get_filename != None:
        global folder_name
        folder_name=get_filename.split(".")[0]
        app.config["CURRENT_SHOW"]=f"static/uploads/{folder_name}/frames/output/0000.png"
        global output_directory
        output_directory = f"static/uploads/{folder_name}/frames/output/" 
    else:
        folder_name=folder_name
    image =app.config["CURRENT_SHOW"].split('/')[-1]
    labels = app.config["LABELS"]
    app.config["FILES"]=sorted(glob.glob(f"static/uploads/{folder_name}/frames/output/*"))
    view_img_path = f"static/uploads/{folder_name}/frames/output"
    return render_template('tagger.html', directory=output_directory, view_img_path=view_img_path, image=image, labels=labels, head=app.config["HEAD"], len=len(app.config["FILES"]))


######################내가 만든 코드

def open_my_config():
    with open(f'static/uploads/{folder_name}/edit/config.json', "r") as file:
        my_config = json.load(file)
    return my_config

def save_my_config(cfg_file):
    cfg_name=os.path.join(f'static/uploads/{folder_name}/edit/','config.json')
    with open(cfg_name, 'w') as file:
        json.dump(cfg_file, file)
        
@app.route('/back_button/')
def back_button():
    app.config["LABELS"]=[] #2023 06 22 수정
    dir_path = f'/static/uploads/{folder_name}/frames/output'
    fname=app.config["CURRENT_SHOW"].split("/")[-1] #0000.png
    fname_num=fname.split('.')[0]
    fname_num=int(fname_num)
    new_fname=fname_num-1
    if new_fname<0:
        new_fname=0
    new_fname=str(new_fname).zfill(4)
    new_fname=new_fname+'.png'
    app.config["CURRENT_SHOW"]=os.path.join(dir_path,new_fname)
    app.config["HEAD"]-=1
    
    return redirect(url_for('edit_get')) 

@app.route('/next_button/')
def next_button():
    app.config["LABELS"]=[] #2023 06 22 수정
    dir_path = f'/static/uploads/{folder_name}/frames/output'
    fname=app.config["CURRENT_SHOW"].split("/")[-1] #0000.png
    fname_num=fname.split('.')[0]
    fname_num=int(fname_num)
    new_fname=fname_num+1
    #print("Test")
    #print(output_directory) static/uploads/행사remover/frames/output
    #if len(output_directory) < new_fname:
    #    new_fname-=1
    new_fname=str(new_fname).zfill(4)
    new_fname=new_fname+'.png'
    app.config["CURRENT_SHOW"]=os.path.join(dir_path,new_fname)
    app.config["HEAD"]+=1
    
    return redirect(url_for('edit_get')) 

point_count = 0

@app.route('/add/<id>')
def add(id):
    global point_count
    point_count += 1
    x = request.args.get("x")
    y = request.args.get("y")

    if len(app.config["LABELS"]) < 4:
        app.config["LABELS"].append({ "x":x, "y":y })
        
        
        if len(app.config["LABELS"]) == 4:
            save_name=os.path.join(f'static/uploads/{folder_name}/edit/','config.json')
            app.config.pop('PERMANENT_SESSION_LIFETIME', None)
            with open(save_name, 'w') as file:
                json.dump(app.config, file)
            pass
    else:
        point_count = 1
        app.config["LABELS"]=[{ "x":x, "y":y }] 
    
    #print(app.config["LABELS"])

    global flag
    flag = 1
    return redirect(url_for('edit_get',point_count=point_count)) #이렇게 하면 filename이 None (url에서 filename이 사라진다)
    
@app.route('/reset/')
def reset():
    #현재 이미지: app.config["CURRENT_SHOW"]
    #원본 이미지 구하기
    
    fname=app.config["CURRENT_SHOW"].split("/")[-1] #0000.png
    source=f'static/uploads/{folder_name}/frames/input/{fname}'
    destination=f'static/uploads/{folder_name}/frames/output/{fname}'
    shutil.copy(source, destination)
    app.config["LABELS"]=[] #2023 06 22 수정
    return redirect(url_for('edit_get')) 

@app.route('/remove_edit/')
def remove():
    current_file=app.config["CURRENT_SHOW"].split("/")[-1]
    remove_edit_infer.inference(folder_name, current_file) 
    app.config["LABELS"]=[] #2023 06 22 수정
    return redirect(url_for('edit_get')) 


@app.route('/reedit', methods=['POST'])
def reedit():
    text = request.form.get("text")
    my_config=open_my_config()
    my_config['TEXT']=text
    save_my_config(my_config) # cfg 다시 저장

    current_file=app.config["CURRENT_SHOW"].split("/")[-1]
    re_edit_infer.inference(folder_name, current_file)
    app.config["LABELS"]=[] #2023 06 22 수정
    return redirect(url_for('edit_get'))

@app.route('/download_video/')
def download_video():
    f2v=frames2video.frames2video(video_name=folder_name)
    f2v.make_video()
    filename=folder_name+'.mp4'
    path = f"static/uploads/{folder_name}/videos/auto/{filename}"
    
    return send_file(path, as_attachment=True)

# flask 웹 서버를 실행시키기 위해서는 필수 작성
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config["HEAD"] = 0
    #folder_name='사모님'
    #app.config["CURRENT_SHOW"]=f"static/uploads/{folder_name}/frames/output/0000.png"
    #global output_directory
    #output_directory = f"static/uploads/{folder_name}/frames/output/" 
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["LABELS"]=[]
    

    app.run(host="127.0.0.1", port="5012", debug=True) # url을 바꾸는 방식
