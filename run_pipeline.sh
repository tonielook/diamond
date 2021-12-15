# first prepare data_input
# copy all mp4 files into data_input/Videos_Ori

 /home/tonielook/MATLAB/R2021b/bin/matlab -nodisplay -nosplash -nodesktop -r "run('./cutVideo.m');exit;"
cd ../data_output/6_Videos
rename "s/.avi//" *avi
cd ../../codes

 python gen_mask.py
 /home/tonielook/MATLAB/R2021b/bin/matlab -nodisplay -nosplash -nodesktop -r "run('./save1stFrame.m');exit;"
 /home/tonielook/MATLAB/R2021b/bin/matlab -nodisplay -nosplash -nodesktop -r "run('./shiftMask2frame.m');exit;"
 python inclusion_coords_to_txt.py
 python read_label_to_box.py
 python trace_defects.py
