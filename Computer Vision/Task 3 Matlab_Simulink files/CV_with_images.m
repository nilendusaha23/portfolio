% Distribution of Angle using Computer Vision on Images using Colour Threshold Method
%%
close all 
clear
clc
%% Load image and coordinates for the reference line
input_pic = imread('Color_threshold_method_images/img10.jpg');
load('hLines_ref1.mat')
figure(1)
imshow(input_pic)
title('Input Picture')


%% Image rotate

rotated_img = imrotate(input_pic, 270);
figure(2)
imshow(rotated_img)
title('Rotated Image')


%% Color Masking in HSV format
Masked_image = ColorMask(rotated_img);
figure(3)
imshow(Masked_image)
title('Masked image to a specified color')
%% Applying a close morphology to make continuous lines

Closed_Morph_image = imclose(Masked_image,strel('square',10));
figure(4)
imshow(Closed_Morph_image)
title('Closed Morph Image')
%% Applying Erosion on the image to reduce noise
se = strel('line',11,90);
eroded_image = imerode(Closed_Morph_image,se);
figure(5)
imshow(eroded_image)
title('Eroded Image')
%% Applying Dilation on the image

dilated_image = imdilate(eroded_image,se);
figure(6)
imshow(dilated_image)
title('Dilated Image')

%% Apply a skeleton morphology to get the thinnest lines

Skeletonized_image = bwskel(dilated_image);
figure(7)
imshow(Skeletonized_image)
title('Skeletonized Lines')

%% Detect Lines
% Perform Hough Transform Algorithm
[H,T,R] = hough(Skeletonized_image);

% Identify the peaks in Hough Transform
hPeaks =  houghpeaks(H);

% Extract the required line from hough transform and peaks
hLines = houghlines(Skeletonized_image,T,R,hPeaks,...
        'FillGap',1500,'MinLength',100);

%% View The Detected Line
% Annotate the required line
[linePos,markerPos] = getVizPosArray(hLines);

lineFrame = insertShape(rotated_img,'Line',linePos,...
            'Color','blue','LineWidth',30);
outFrame = insertObjectAnnotation(lineFrame,...
            'circle',markerPos,'','Color','red','LineWidth',15);

% Annotate the reference line

[linePos_ref,markerPos_ref] = getVizPosArray(hLines_ref);

lineFrame_ref = insertShape(outFrame,'Line',linePos_ref,...
            'Color','blue','LineWidth',30);
outFrame_final = insertObjectAnnotation(lineFrame_ref,...
            'circle',markerPos_ref,'','Color','red','LineWidth',15);

% View image
figure(8)
imshow(outFrame_final)
title('Detected Angled Line')
%% Angle Calculation
% Reference line coordinates
x1 = hLines_ref.point2(1,1);
y1 = hLines_ref.point2(1,2);
x2 = hLines_ref.point1(1,1);
y2 = hLines_ref.point1(1,2);

% Angled line coordinates

x3 = hLines.point2(1,1);
y3 = hLines.point2(1,2);
x4 = hLines.point1(1,1);
y4 = hLines.point1(1,2);

% Slope Calculation
m1 = (y2-y1)/(x2-x1);
m2 = (y4-y3)/(x4-x3);
m = (m1-m2)/(1+m1*m2);
% Required Angle 
theta = atan(m);
required_angle = theta * (180/pi);

%% Final Annotated Image

position=[1750 3880];
box_color ={'red'};
text_str=sprintf('%.2f',required_angle);
final_image=insertText(outFrame_final,position,text_str,'FontSize',200,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
figure(9)
imshow(final_image)
title('Required Output')

