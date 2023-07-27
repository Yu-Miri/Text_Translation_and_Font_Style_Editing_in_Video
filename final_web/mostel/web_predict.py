import os
import argparse
import math
import torch
import cv2
import time
import torchvision.transforms.functional as F
import numpy as np
from tqdm import tqdm
from mmcv import Config
from torch.utils.data import DataLoader
from mostel.model import Generator
from mostel.datagen import custom_dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def test_speed(G, i_t, i_s):
        num = 50
        start_time = time.time()
        for _ in range(num):
            tmp = G(i_t, i_s)
        time_cost = (time.time() - start_time) / num
        return time_cost


class MyDilate():
    def __init__(self) -> None:
        tmp_distance = 3
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tmp_distance, tmp_distance))  # MORPH_RECT  MORPH_CROSS  MORPH_ELLIPSE
        self.kernel = kernel
        self.iterations = 1

    def __call__(self, img, binary=True):
        img = img * 255
        if binary:
            ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        dilate_img = cv2.morphologyEx(img, cv2.MORPH_DILATE, self.kernel, iterations=self.iterations)
        ret, dilate_img = cv2.threshold(dilate_img, 127, 255, cv2.THRESH_BINARY)
        dilate_img = dilate_img[:, :, np.newaxis] / 255

        return dilate_img
    
class style_transfer():
    def __init__(self, config, input_dir, save_dir, checkpoint, i_t_name = 'i_t.txt', vis = False, slm = False, speed = False, dilate = False):
        self.config = config
        self.input_dir = input_dir
        self.save_dir = save_dir
        self.checkpoint = checkpoint
        self.i_t_name = i_t_name
        self.vis = vis
        self.slm = slm
        self.speed = speed
        self.dilate = dilate
        
        assert self.input_dir is not None
        assert self.save_dir is not None
        assert self.checkpoint is not None
    def main(self):


        cfg = Config.fromfile(self.config)
        G = Generator(cfg, in_channels=3).to(device)
        checkpoint = torch.load(self.checkpoint)
        G.load_state_dict(checkpoint['generator'])
        print('Model loaded: {}'.format(self.checkpoint))

        batch_size = 256 if not self.speed else 1
        eval_data = custom_dataset(cfg, data_dir=self.input_dir, i_t_name=self.i_t_name, mode='eval')
        eval_loader = DataLoader(
            dataset=eval_data,
            batch_size=batch_size,
            num_workers=4,
            shuffle=False,
            drop_last=False)
        eval_iter = iter(eval_loader)

        G.eval()
        total_fps = []
        if self.dilate:
            mydilate = MyDilate()
        
        with torch.no_grad():
            for step in tqdm(range(len(eval_data)), total=math.ceil(len(eval_data)/batch_size)):
                try:
                    inp = next(eval_iter)
                except StopIteration:
                    break
                i_t = inp[0].to(device)
                i_s = inp[1].to(device)
                name_list = inp[2]

                gen_o_b_ori, gen_o_b, gen_o_f, gen_x_t_tps, gen_o_mask_s, gen_o_mask_t = G(i_t, i_s)

                if self.speed:
                    time_cost = test_speed(G, i_t, i_s)
                    total_fps.append(1 / time_cost)
                    print('Params: %s, Inference self.speed: %fms, FPS: %f, %f' % (
                        str(sum(p.numel() for p in G.parameters() if p.requires_grad)),
                        time_cost * 1000, 1 / time_cost, sum(total_fps) / len(total_fps)))

                gen_o_b_ori = gen_o_b_ori * 255
                gen_o_b = gen_o_b * 255
                gen_o_f = gen_o_f * 255
                gen_x_t_tps = gen_x_t_tps * 255

                for tmp_idx in range(gen_o_f.shape[0]):
                    name = str(name_list[tmp_idx])
                    name, suffix = name.split('.')

                    o_mask_s = gen_o_mask_s[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    o_mask_t = gen_o_mask_t[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    o_b_ori = gen_o_b_ori[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    o_b = gen_o_b[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    o_f = gen_o_f[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    x_t_tps = gen_x_t_tps[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                    
                    ori_o_mask_s = o_mask_s
                    if self.dilate:
                        tmp_i_s = (i_s * 255)[tmp_idx].detach().to('cpu').numpy().transpose(1, 2, 0)
                        o_mask_s = mydilate(o_mask_s)
                        o_b = o_mask_s * o_b_ori + (1 - o_mask_s) * tmp_i_s
                    
                    if self.slm:
                        alpha = 0.5
                        o_f = o_mask_t * o_f + (1 - o_mask_t) * (alpha * o_b + (1 - alpha) * o_f)

                    if self.vis:
                        # cv2.imwrite(os.path.join(self.save_dir, name + '_o_f.' + suffix), o_f[:, :, ::-1])
                        cv2.imwrite(os.path.join(self.save_dir, name + '_o_b.' + suffix), o_b[:, :, ::-1])
                        # cv2.imwrite(os.path.join(self.save_dir, name + '_o_b_ori.' + suffix), o_b_ori[:, :, ::-1])
                        # cv2.imwrite(os.path.join(self.save_dir, name + '_o_mask_s.' + suffix), o_mask_s * 255)
                        # cv2.imwrite(os.path.join(self.save_dir, name + '_o_mask_t.' + suffix), o_mask_t * 255)
                        # cv2.imwrite(os.path.join(self.save_dir, name + '_x_t_tps.' + suffix), x_t_tps[:, :, ::-1])
                    else:
                        cv2.imwrite(os.path.join(self.save_dir, name + '.' + suffix), o_f[:, :, ::-1])
