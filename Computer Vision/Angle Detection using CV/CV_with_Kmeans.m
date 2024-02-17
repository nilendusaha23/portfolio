% Distribution of Angle using Computer Vision on Images using K-Means Method
%%
close all
clear
clc
%% Load image 

input_pic = imread('KMeans_method_images/aiimg20.jpg');
figure(1)
imshow(input_pic) 
title('Input image');

 %% Image rotate

rotated_img = imrotate(input_pic, 270);
figure(2)
imshow(rotated_img)
title('Rotated Image');
 
%% Convert Image from RGB Color Space to L*a*b* Color Space

lab_he = rgb2lab(rotated_img);
%% Classify the Colors in 'a*b*' Space Using K-Means Clustering

ab = lab_he(:,:,1:2);
ab = im2single(ab);
nColors = 3;
% repeat the clustering 3 times 
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',3);
figure(3)
imshow(pixel_labels,[])
title('Image Labeled by Cluster Index');

%% Create Images that Segment the Kmeans Cluster Image by Color

% Cluster 1
mask1 = pixel_labels==1;
cluster1 = rotated_img .* uint8(mask1);
figure(4)
imshow(cluster1)
title('Cluster 1')

% Cluster 2

mask2 = pixel_labels==2;
cluster2 = rotated_img .* uint8(mask2);
figure(5)
imshow(cluster2)
title('Cluster 2')

% Cluster 3

mask3 = pixel_labels==3;
cluster3 = rotated_img .* uint8(mask3);
figure(6)
imshow(cluster3)
title('Cluster 3')




%% Saving the required image 
imwrite(cluster3, 'cluster.jpg');

%%
taken_picture = imread('cluster.jpg');


%% Load reference line coordinates and view the chosen clustered image 

load('hLines_ref_kmeans.mat')
figure(7)
title('Frame')
imshow(taken_picture)
title('Chosen image')


%% Converting image to black and white 
BW = im2bw(taken_picture);
figure(8)
imshow(BW)
title('Binary image')
%% Apply a close morphology to make continuous lines
Closed_Morph_image = imclose(BW,strel('square',10));
figure(9)
imshow(Closed_Morph_image)
title('Closed Morph Image')
%% Applying Erosion on the image to reduce noise
se = strel('line',11,90);
eroded_image = imerode(Closed_Morph_image,se);
figure(10)
imshow(eroded_image)
title('Eroded Image')
%% Applying Dilation on the image

dilated_image = imdilate(eroded_image,se);
figure(11)
imshow(dilated_image)
title('Dilated Lines')

%% Apply a skeleton morphology to get the thinnest lines

Skeletonized_image = bwskel(dilated_image);
figure(12)
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
[linePos_ref,markerPos_ref] = getVizPosArray(hLines_ref_kmeans);

lineFrame_ref = insertShape(outFrame,'Line',linePos_ref,...
            'Color','blue','LineWidth',30);
outFrame_final = insertObjectAnnotation(lineFrame_ref,...
            'circle',markerPos_ref,'','Color','red','LineWidth',15);
% View image
figure(13)
imshow(outFrame_final)
title('Detected Angled Line')
%% Angle Calculation
% Reference line coordinates
x1 = hLines_ref_kmeans.point2(1,1);
y1 = hLines_ref_kmeans.point2(1,2);
x2 = hLines_ref_kmeans.point1(1,1);
y2 = hLines_ref_kmeans.point1(1,2);

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
figure(14)
imshow(final_image)
title('Required Output')
