# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 15:36:21 2021

@author: mastaffs
"""
from PIL import Image
import os
import numpy as np
from skimage.segmentation import mark_boundaries as mkbdy
from skimage.measure import label, regionprops
import shutil

# base_path = r'F:\diamond_project\frame_mask_v2\41_80'
# frame_path = os.path.join(base_path, 'frame001')
# mask_path = os.path.join(base_path, 'mask_new')
# vis_save_path = os.path.join(base_path, 'frame001_vis')
# tmp_txt_save_path = os.path.join(base_path, 'txt_files')

frame_path = r'../data_output/2_1stFrame'
mask_path = r'../data_output/3_mask_new_v5'
tmp_txt_save_path = r'../data_output/4_frame_mask/txt_files5'
vis_save_path = r'../data_output/4_frame_mask/frame001_vis5'
os.makedirs(vis_save_path, exist_ok=True)
os.makedirs(tmp_txt_save_path, exist_ok=True)

exist_list = os.listdir(tmp_txt_save_path)
# exist_list = []
mask_list = [n for n in os.listdir(mask_path) if not n[:11] in exist_list]

for nn in mask_list:
    mask = Image.open(os.path.join(mask_path,nn))
    mask_np = np.array(mask)
    
    ############# visualization ##############
    img_path = os.path.join(frame_path,nn[:11]+'_001.png')
    img = Image.open(img_path).convert('RGB')
    img_np = np.array(img)
    
    img_mask = mkbdy(img_np,mask_np[:,:,0],color=(1,0,0),outline_color=(1,0,0))
    img_mask = mkbdy(img_mask,mask_np[:,:,1],color=(0,1,0),outline_color=(0,1,0))
    img_mask = Image.fromarray((img_mask*255).astype('uint8'))
    
    img_mask.save(os.path.join(vis_save_path, nn[:11]+'_001_new_mask_vis.png'))
    
    ############ extract txt file ###############
    txt_save_path = os.path.join(tmp_txt_save_path,nn[:11])
    if os.path.isdir(txt_save_path):
        shutil.rmtree(txt_save_path)
    os.makedirs(txt_save_path)
    
    ## 0=R=reflection 1=G=inclusion
    cnt = 0
    for channel in range(2):
        mask_single = mask_np[:,:,channel]
        mask_single [mask_single>0] = 255
        
        boxes = []
        lbl = label(mask_single)
        props = regionprops(lbl)
        
        for prop in props:
            if prop.coords.shape[0]>1:
                save_name = os.path.join(txt_save_path, f'{nn[:11]}_{cnt}_{channel}.txt')
                np.savetxt(save_name, prop.coords, delimiter=' ', fmt='%d') 
                cnt += 1
    
    print(f'{nn}')

        
    
    
    







