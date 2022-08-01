%This set of code plots the variation in angular velocities in task 1 of data taken from NX simulation.
%The simulation data is loaded from the spreadsheet.
%%
clear
clc
%%
T = readtable('twobar_solution_2_velocity.xlsx');

Step = T{:,1};
Link_AB = T{:,2};
Liink_OA = T{:,3};
AVelocity_Link_AB = T{:,2}*(pi/180);
AVelocity_Link_OA = T{:,3}*(pi/180);

%% PLOT Results velocities

figure(1)
plot((Step),(AVelocity_Link_OA),(Step),(AVelocity_Link_AB))
grid
title('Variation of \omega_1 and \omega_2')
xlabel('Point')
ylabel('omega(rad/sec)')
legend('\omega_1','\omega_2')
xlim([1 50]);
ylim([-2 13]);