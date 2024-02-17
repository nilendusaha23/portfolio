% Distribution of Angle using Computer Vision on Video using Colour Threshold Method
%%
close all
clear
clc
%% Initialize System Objects

% Create a VideoFileReader System object to read video from a file.
vid_File_Reader = VideoReader('video/inputvid.mp4');
implay('video/inputvid.mp4');
myVideo = VideoWriter('outputvid.mp4');
depVideoPlayer = vision.DeployableVideoPlayer;
open(myVideo);
% Load the reference hLine
load('hLines_ref1.mat')

%% Loop Algorithm

while hasFrame(vid_File_Reader)
    % Acquire frame
    frame = readFrame(vid_File_Reader);

    % Color Masking in HSV format
    Masked_image = thickspoonMask(frame);

    % Applying a close morphology to make continuous lines
    Closed_Morph_image = imclose(Masked_image,strel('disk',10));
    
    % Applying Erosion on the image to reduce noise
    se = strel('line',11,90);
    eroded_image = imerode(Closed_Morph_image,se);
    
    % Applying Dilation on the image
    
    dilated_image = imdilate(eroded_image,se);

    % Apply a skeleton morphology to get the thinnest lines
    Skeletonized_image = bwskel(dilated_image);
    
    % Perform Hough Transform
    [H,T,R] = hough(Skeletonized_image);

    % Identify Peaks in Hough Transform
    hPeaks  = houghpeaks(H);

    % Extract lines from hough transform and peaks
    hLines = houghlines(Skeletonized_image,T,R,hPeaks,...
        'FillGap',1000,'MinLength',100)
    
    
    % Overlay lines
    [linePos,markerPos] = getVizPosArray(hLines);
    [linePos_ref,markerPos_ref] = getVizPosArray(hLines_ref);

    if(~isempty(hLines))
        lineFrame = insertShape(frame,'Line',linePos,...
            'Color','blue','LineWidth',5);
        outFrame = insertObjectAnnotation(lineFrame,...
            'circle',markerPos,'','Color','red','LineWidth',10);
        
        % make Reference line too

        lineFrame_ref = insertShape(outFrame,'Line',linePos_ref,...
                    'Color','blue','LineWidth',5);
        outFrame_final = insertObjectAnnotation(lineFrame_ref,...
                    'circle',markerPos_ref,'','Color','red','LineWidth',10);
        
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
        required_angle = theta * (180/pi)
        
    % Final Annotated Image

        position=[10 10];
        box_color ={'red'};
        text_str=sprintf('%.2f',required_angle);
        output=insertText(outFrame_final,position,text_str,'FontSize',150,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
    else
        output = frame;
    end
    
    % Display video frame to screen
	depVideoPlayer(output);
    
	%% Write frame to final video file
	writeVideo(myVideo, output);
	pause(1/vid_File_Reader.FrameRate);
    
end
close(myVideo)

