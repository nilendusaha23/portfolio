% analysis of task 1 using for loop method

clear
clc

tic
%% Variable declaration

r1=0.3; r2=0.2;  %in meters
i=0;   

%%  Solution for the analysis

for xb=0.3:-0.006:0             % for loop for xb from 0.3 to 0
    yb=-xb+0.3;
    A=2*r2*xb;
    B=2*r2*yb;
    C=(r2)^2-(r1)^2+(xb)^2+(yb)^2; 
    R=sqrt(A^2+B^2);
    Z=C/R;
    zz=sqrt(1-Z^2);
    i=i+1; % added a counter
    %Position Analysis
    theta2=atan2(B,A)+atan2(zz,Z); 
    if theta2<0; theta2=theta2+2*pi;end   
    theta2b=atan2(B,A)-atan2(zz,Z);
    if theta2b<0; theta2b=theta2b+2*pi;end
    theta1=atan2((yb-r2*sin(theta2)),(xb-r2*cos(theta2)));  
    Xb(i)=xb; Yb(i)=yb; T1(i)=theta1; T2(i)=theta2; T2b(i)=theta2b; %T2 has two solutiuons and rejecting the value of theta2b in further steps
    %Velocity analysis
    ub=2*cos(2.3562); %initial angle at the begining of the path is 135 degrees
    vb=2*sin(2.3562);
    w1=(ub*cos(theta2)+vb*sin(theta2))/(r1*sin(theta2-theta1)); 
    w2=(ub*cos(theta1)+vb*sin(theta1))/(r2*sin(theta1-theta2));
    W2(i)=w2; W1(i)=w1;
    point(i)=i; 
end

%% PLOT Required Results for variation in angles

figure(1)
plot((point),(T1*180/pi),(point),(T2*180/pi))
grid
title('Variation of \Theta_1 and \Theta_2')
xlabel('Point')
ylabel('Theta(deg)')
legend('\Theta_1','\Theta_2')
xlim([1 50]);
ylim([-40 165]);


%% PLOT Required Results for variation in angular velocities

figure(2)
plot((point),(W1),(point),(W2))
grid
title('Variation of \omega_1 and \omega_2')
xlabel('Point')
ylabel('omega(rad/sec)')
legend('\omega_1','\omega_2')
xlim([1 50]);

toc
