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
train_recognizer = True
rec_lr_weight = 1.

# StyleAug
vflip_rate = 0.5
hflip_rate = 0.5
angle_range = [(-15, -5), (5, 15)]

# Train
learning_rate = 5e-7
decay_rate = 0.9
beta1 = 0.9
beta2 = 0.999
max_iter = 100000
write_log_interval = 1000
save_ckpt_interval = 5000
gen_example_interval = 10
task_name = 'training'
checkpoint_savedir = 'train_output/' + task_name + '/'  # dont forget '/'
ckpt_path = 'checkpoint/train_step-210000.model'
inpaint_ckpt_path = 'checkpoint/final_erase_ckpt.model'
vgg19_weights = 'checkpoint/vgg19-dcbb9e9d.pth'
rec_ckpt_path = 'checkpoint/best_recognizer.model'
# rec_ckpt_path = None

# data
batch_size = 32
real_bs = 4
with_real_data = True if real_bs > 0 else False
num_workers = 4
data_shape = [64, 256]
data_dir = [
    'MOSTEL/dataset/Synthetic_data'
]
real_data_dir = [
    # 'datasets/training/mix_real_data_train',
    # 'datasets/training/mix_real_data_val',
    # 'datasets/training/mix_real_data_test'
    'datasets/training/mostel_Real_data'
]
i_s_dir = 'i_s'
t_b_dir = 't_b'
t_f_dir = 't_f'
mask_t_dir = 'mask_t'
mask_s_dir = 'mask_s'
txt_dir = 'txt'
font_path = 'arial.ttf'
example_data_dir = 'demo_img/imgs'
example_result_dir = checkpoint_savedir + 'val_visualization'

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