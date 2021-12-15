%% Masked ROI
clear all;
close all;
clc;

path_mask = '../data_output/1_Masks';
path_img = '../data_output/1_Images';
path_frame = '../data_output/2_1stFrame';
path_save = '../data_output/3_mask_new_v5';
if ~exist(path_save, 'dir')
   mkdir(path_save)
end

id_list = dir(fullfile(path_mask,'*_mask.png'));
fprintf(num2str(length(id_list)));
%%%%%%%%%%%%% Loop for iamge %%%%%%%%%%%%%%%%%%%%
for idx = 1:length(id_list)
    id = id_list(idx).name(1:11);
    fprintf([num2str(idx),' ', num2str(id)]);
    
    v1_frame = imread(fullfile(path_frame,[id,'_001.png']));
    v1_img = imread(fullfile(path_img,[id,'.png']));
    v1_mask = imread(fullfile(path_mask,[id,'_mask.png']));

    v1_img = im2double(v1_img);
    v1_frame = im2double(v1_frame);
    v1_mask = im2double(v1_mask);
    
    mask_new = zeros(size(v1_mask));
    range_hw = 15;
    
    %% Gradient %%
    [ix,iy] = gradient(v1_img);
    igrad = abs(ix)+abs(iy);
    
    [fx,fy] = gradient(v1_frame);
    fgrad = abs(fx)+abs(fy);

    %% reflection
    mask_single = v1_mask(:,:,1);
    igrad_tmp = igrad.*mask_single;
    % figure; imshow(imfuse(igrad,igrad_tmp));
    
    img1 = v1_img.*v1_mask(:,:,1);
%     figure;imshow(img1)
    img2 = v1_img.*v1_mask(:,:,2);
%     figure; imshow((img1+img2)*10);
    
%     filename = 'D:\OneDrive - City University of Hong Kong\1214\vis_mask_grad_enhance.png';
%     frame = getframe(gca); 
%     img = frame2im(frame); 
%     imwrite(img,filename); 
    
    dist = zeros(1,3);
    index = 0;
    % neg = move up, pos = down, neg = move left, pos = right
    %%%%%%%%%%%%%%% Loop for search window %%%%%%%%%%%%%%
    for hh = -5:1:5
        for ww = -5:1:5
            index = index + 1;

            % MSE of pixel value %
%                 frame_shift = circshift(v1_frame, [hh,ww]);
%                 masked_frame = frame_shift.*mask_single;
%                 figure; imshow(imfuse(frame_shift,mask_single));
%                 mse = sum((masked_frame - masked_img).^2,'all');

            % Gradient %
            fgrad_shift = circshift(fgrad, [hh,ww]);
            fgrad_tmp = fgrad_shift.*mask_single;
%             figure; imshow(imfuse(fgrad,mask_single));
            mse_grad = sum((igrad_tmp - fgrad_tmp).^2,'all');

            dist(index,:)=[hh,ww,mse_grad];
        end
    end
    [~,I] = min(dist(:,3));
    info = dist(I,:);
    sh = info(1); sw = info(2);
    mask_shift = circshift(mask_single,[-sh,-sw]);
    mask_new(:,:,1) = mask_shift;
%     figure; imshow(imfuse(v1_frame, mask_new(:,:,1)));
    fprintf(' Reflection');
    
    %% Inclusion
    mask_single = v1_mask(:,:,2);
    
%     masked_img = v1_img.*mask_single;
%     figure; imshow(imfuse(v1_img, mask_single));

    igrad_tmp = igrad.*mask_single;
    
    dist = zeros(1,3);
    index = 0;
    %%%%%%%%%%%%%%% Loop for search window %%%%%%%%%%%%%%
    for hh = -range_hw:1:range_hw
        for ww = -range_hw:1:range_hw
            index = index + 1;

%             frame_shift = circshift(v1_frame, [hh,ww]);
%             masked_frame = frame_shift.*mask_single;
%             figure; imshow(imfuse(frame_shift,mask_single));
%             mse = sum((masked_frame - masked_img).^2,'all');

            % Gradient %
            fgrad_shift = circshift(fgrad, [hh,ww]);
            fgrad_tmp = fgrad_shift.*mask_single;
%             figure; imshow(imfuse(fgrad,mask_single));
            mse_grad = sum((igrad_tmp - fgrad_tmp).^2,'all');

            dist(index,:)=[hh,ww,mse_grad];
        end
    end
    [~,I] = min(dist(:,3));
    info = dist(I,:);
    sh = info(1); sw = info(2);
    mask_shift = circshift(mask_single,[-sh,-sw]);
%     figure; imshow(imfuse(v1_frame,mask_shift));
%     figure; imshow(imfuse(v1_frame,mask_single));
    mask_new(:,:,2) = mask_shift;
    fprintf(' Inclusion');
    
    %% Save
    save_name = fullfile(path_save,[num2str(id),'_mask.png']);
    imwrite(mask_new,save_name);
    fprintf([' save...','\n'])
end
