% analysis of task 2 using for loop method
%%
clear
clc
tic
%% Variable declaration

r1=0.01; r2=0.035; r3=0.02; r4=0.03;  %length of links in meters
w1=100; a1=0; i=0;   % w1 is the angular velocity of 1st link
% For dynamics
rg1=0.005; rg2=0.0175; rg3=0.01;
m1=0.2; m2=0.6; m3=0.4;   % mass of links
Ig1=1 * 10^(-5); Ig2=4 * 10^(-4); Ig3=8 * 10^(-5);  % Moment of Inertia
T_L = 0;    % Load Torque 
%%  Solution for the analysis

for TH1=0:0.0001:2*pi             % initiating for loop
    A=cos(TH1)-(r4/r1);
    B=sin(TH1);
    C=(r4/r3)*cos(TH1)-((r1^2-r2^2+r3^2+r4^2)/(2*r1*r3));
    R=sqrt(A^2+B^2);
    Z=C/R;
    zz=sqrt(1-Z^2);
    i=i+1; % adding a counter
    
    %Position Analysis
    TH3=atan2(B,A)+atan2(zz,Z);
      if TH3<0; TH3=TH3+2*pi;end   
      TH3b=atan2(B,A)-atan2(zz,Z);
      if TH3b<0; TH3b=TH3b+2*pi;end
    TH2=atan2((-r3*sin(TH3)-r1*sin(TH1)),(r4-r3*cos(TH3)-r1*cos(TH1)));
      T1(i)=TH1; T2(i)=TH2; T3(i)=TH3; T3b(i)=TH3b;                %T3 has two solutiuons and rejecting the value of TH3b in further steps
   
    %Velocity analysis
    w3=w1*(r1*sin(TH1-TH2))/(r3*sin(TH2-TH3));
    w2=w1*(r1*sin(TH3-TH1))/(r2*sin(TH2-TH3));
    W3(i)=w3; W2(i)=w2;
    
    %Acceleration Analysis
    a3=(w1^2*r1/r3)*((1-(w2/w1))*cos(TH1-TH2)*sin(TH2-TH3)-((w2/w1)-(w3/w1))*cos(TH2-TH3)*sin(TH1-TH2))/(sin(TH2-TH3))^2;
    a2=-(w1^2*r1/r2)*((1-(w3/w1))*cos(TH1-TH3)*sin(TH2-TH3)-((w2/w1)-(w3/w1))*cos(TH2-TH3)*sin(TH1-TH3))/(sin(TH2-TH3))^2;
    A3(i)=a3; A2(i)=a2;
    
    %Acceleration due to centre of mass
    acc_xg1= -(rg1 * ( (a1*sin(TH1)) + ((w1)^2 * cos(TH1)) ) );
    acc_yg1= rg1 * ( (a1*cos(TH1)) + ((w1)^2 * sin(TH1)) );
    
    acc_xg2= -( r1 * ((a1*sin(TH1)) + ((w1)^2 * cos(TH1))) + rg2 * ((a2*sin(TH2)) + ((w2)^2 * cos(TH2))) ); 
    acc_yg2= (r1 * ((a1*cos(TH1)) - ((w1)^2 * sin(TH1)))) + (rg2 * ((a2*cos(TH2)) - ((w2)^2 * sin(TH2))));
    
    acc_xg3= (r3-rg3) * ((a3*sin(TH3)) + ((w3)^2*cos(TH3)));
    acc_yg3= -(r3-rg3) * ((a3*cos(TH3)) - ((w3)^2*sin(TH3)));
    
    %B elements
    B1 = m1*acc_xg1;
    B2 = m1*acc_yg1;
    B3 = Ig1*a1; 
    B4 = m2*acc_xg2;
    B5 = m2*acc_yg2;
    B6 = Ig2*a2;
    B7 = m3*acc_xg3;
    B8 = m3*acc_yg3;
    B9 = (Ig3*a3) + T_L;
    %B matrix
    B = [B1; B2; B3; B4; B5; B6; B7; B8; B9];
    
    %Preparing the A matrix and its inverse
    
    A = [1 0 1 0 0 0 0 0 0; 0 1 0 1 0 0 0 0 0; rg1*sin(TH1) -rg1*cos(TH1) (r1-rg1)*sin(TH1) (r1-rg1)*cos(TH1) 0 0 0 0 1; 0 0 -1 0 1 0 0 0 0; 0 0 0 -1 0 1 0 0 0; 0 0 -rg2*sin(TH2) rg2*cos(TH2) -(r2-rg2)*sin(TH2) (r2-rg2)*cos(TH2) 0 0 0; 0 0 0 0 -1 0 1 0 0; 0 0 0 0 0 -1 0 1 0; 0 0 0 0 -rg3*sin(TH3) rg3*cos(TH3) -(r3-rg3)*sin(TH3) (r3-rg3)*cos(TH3) 0];
    inverse_A = inv(A);
    
    %Finding X matrix
    
    X = inverse_A * B;
    
    %Recording the Answers
    T(i)=X(9,:);
    Joint_AX(i)=X(1,:);
    Joint_AY(i)=X(2,:);
    Joint_BX(i)=X(3,:);
    Joint_BY(i)=X(4,:);
    Joint_CX(i)=X(5,:);
    Joint_CY(i)=X(6,:);
    Joint_DX(i)=X(7,:);
    Joint_DY(i)=X(8,:);
    
end

%% PLOT Results

%%Plot of Theta2 and Theta3 vs Theta1
figure(1)
plot((T1*180/pi),(T2*180/pi),(T1*180/pi),(T3*180/pi))
grid
title('Variation of \Theta_2 and \Theta_3')
xlabel('\Theta_1(deg)')
ylabel('\Theta(deg)')
legend('\Theta_2','\Theta_3')
xlim([0 360]);

%Plot of OMEGA2 and OMEGA3 against THETA1
figure(2)
plot((T1*180/pi),W2,(T1*180/pi),W3)
grid
title('Variation of angular velocities')
xlabel('\Theta_1(deg)')
ylabel('\omega(rad/s)')
legend('\omega_2','\omega_3')
xlim([0 360]);

%Plot of alpha3 and alpha2 against Theta1
figure(3)
plot((T1*180/pi),A2,(T1*180/pi),A3)
grid
title('Variation of angular acc.')
xlabel('\Theta_1(deg)')
ylabel('\alpha(rad/s^2)')
legend('\alpha_2','\alpha_3')
xlim([0 360]);
%% Dynamics graphs
%Plot of motor torque against Theta1
figure(4)
plot((T1*180/pi),T)
grid
title('Variation of motor Torque')
xlabel('\Theta_1(deg)')
ylabel('Torque(Nm)')
legend('Torque')
xticks(0:45:360);

%Plot of Force in joint A
figure(5)
plot(Joint_AX,Joint_AY)
grid
title('Plot of Force at Joint A')
xlabel('Force at X')
ylabel('Force at Y')
xticks(-500:50:100);

%Plot of Force in joint B
figure(6)
plot(Joint_BX,Joint_BY)
grid
title('Plot of Force at Joint B')
xlabel('Force at X')
ylabel('Force at Y')
xticks(-100:50:450);

%Plot of Force in joint C
figure(7)
plot(Joint_CX,Joint_CY)
grid
title('Plot of Force at Joint C')
xlabel('Force at X')
ylabel('Force at Y')
xticks(-200:100:500);

%Plot of Force in joint D
figure(8)
plot(Joint_DX,Joint_DY)
grid
title('Plot of Force at Joint D')
xlabel('Force at X')
ylabel('Force at Y')
xticks(-100:50:500);

toc
