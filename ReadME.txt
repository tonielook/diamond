/media/hdd/css_data/hdr_data_v2

1 gen_mask.py  XML -> mask img
2.1 save1stFrame.m -> 1st frame of video
* 2 shiftMask2frame.m  mask img -> shifted mask img
3 inclusion_coords_to_txt.py  shifted mask img -> txt folder for each ID (coords)
4 read_label_to_box.py txt folder for each ID (coords) -> txt folder (ID_template) (bounding box coords)
* 5 trace_defects.py  txt folder (ID_template) -> trajectory
5.1 cutVideo.m   ori video -> half video

https://drive.google.com/drive/u/1/folders/1_p9NnNUyzW4qhuO7VBrl1D6DQ3ljgn59