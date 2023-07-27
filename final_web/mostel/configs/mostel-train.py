# Loss
lb = 1.
lb_mask = 1.
lb_beta = 10.
lf = 1.
lf_theta_1 = 10.
lf_theta_2 = 1.
lf_theta_3 = 500.
lf_mask = 10.
lf_rec = 0.1

# Recognizer
with_recognizer = True
use_rgb = True
# train/home/ubuntu/SRNet/MOSTEL/output_recognizer = True
train_recognizer = True
rec_lr_weight = 1.

# StyleAug
vflip_rate = 0.5
hflip_rate = 0.5
angle_range = [(-15, -5), (5, 15)]

# Train
learning_rate = 5e-5
decay_rate = 0.9
beta1 = 0.9
beta2 = 0.999
max_iter = 300000
write_log_interval = 100
save_ckpt_interval = 50000
gen_example_interval = 50000
task_name = 'mostel-train-real-eng'
checkpoint_savedir = 'output/' + task_name + '/'  # dont forget '/'
ckpt_path = 'None'
inpaint_ckpt_path = 'output/erase-train/finetune_output/train_step-100000.model'
vgg19_weights = 'models/vgg19-dcbb9e9d.pth'
# rec_ckpt_path = 'None'
rec_ckpt_path = 'models/recognizer_pretrain.pth'

# data
batch_size = 16
real_bs = 2
with_real_data = True if real_bs > 0 else False
# with_real_data = False
# num_workers = 8
num_workers = 4
data_shape = [64, 256]
data_dir = [
    'datasets/training/filtered_data_train',
    'datasets/training/filtered_data_val',
    'datasets/training/filtered_data_test'
]
real_data_dir = [
    '/home/ubuntu/SRNet/MOSTEL/datasets/training/mlt2017-train-patch',
    '/home/ubuntu/SRNet/MOSTEL/datasets/training/mlt2017-val-patch',
    '/home/ubuntu/SRNet/MOSTEL/datasets/training/ic13-test-patch'
    # 'datasets/training/mix_real_data_train',
    # 'datasets/training/mix_real_data_val',
    # 'datasets/training/mix_real_data_test'
]
i_s_dir = 'i_s'
t_b_dir = 't_b'
t_f_dir = 't_f'
mask_t_dir = 'mask_t'
mask_s_dir = 'mask_s'
txt_dir = 'txt'
font_path = 'mostel/arial.ttf'
example_data_dir = 'demo_img/imgs'
example_result_dir = checkpoint_savedir + 'val_visualization'
# 학습 중에 찍히는 output 보기 위한 데이터셋 준비
# predict 해서 볼 output 데이터셋 준비

# TPS
TPS_ON = True
num_control_points = 10
stn_activation = 'tanh'
tps_inputsize = data_shape
tps_outputsize = data_shape
tps_margins = (0.05, 0.05)

# predict
predict_ckpt_path = None
predict_data_dir = None
predict_result_dir = checkpoint_savedir + 'pred_result'