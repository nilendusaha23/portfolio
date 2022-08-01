% This a matlab code for exporting the data set into an Excel Sheet
% author: Nilendu Saha
clear all
load('Ta.mat')

%%
simulink_data = Ta'

%%
writematrix(simulink_data,'simulink_data.xlsx','Sheet',1);
