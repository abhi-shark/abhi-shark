% Variable declaration
clear;
clc;
W=3000;%total, lbs
m=W/32.2;%conversion to required units
Ws=2700;%sprung mass, lbs
ms=Ws/32.2;%conversion to required units
x1=3.5; %feet
x2=-4.5; %feet
h=-1; %feet
t=6; %feet
Iz=40000;%lbs-ft^2
Ix=15000;%lbs-ft^2
c=0.5;%ft
dldphif=8000;%lbs-ft
dldphir=5000;%lbs-ft
dldphidf=1000;%lbs-ft/sec
dldphidr=500;%lbs-ft/sec
p=12; %inches
d=12; %inches
n=15; %efficiency
e=1; %steering gear box efficiency
Ks=10; %in-lbs/deg
tm=3; %inches
%linear tire coefficient - comment out for part 2
Ci=140*180/pi*2; %converted to lbs/rad
C1=Ci;
C2=Ci;
%Function declaration
function [db,b,dr,r]=yaw(delta,u,C1,C2,m,x1,x2,I,time,dt) %calculates yaw rate per
instance
% State array initialization
b = zeros(1,length(time));
db = zeros(1,length(time));
r = zeros(1,length(time));
dr = zeros(1,length(time));
% Matrixes
A =[ (-C1-C2)/(m*u) (-x1*C1-x2*C2)/(m*u^2)-1;
(-C1*x1-C1*x2)/I (-(x1)^2*C1-(x2)^2*C2)/(I*u)];
B =[C1/(m*u);
x1*C1/I];
for i = 1:1:(length(time)-1)
xv = A*[b(i);r(i)] + B*delta(i);
%output with xv
db(i)= xv(1);
dr(i)= xv(2);
%update state variables
b(i+1) = db(i)*dt + b(i);
r(i+1) = dr(i)*dt + r(i);
end
end
function
[v,dv,r,dr,phi,dphi,ddphi,Wdiff,Wsum,Cf,Cr]=yawroll(delta1,u,Dphi,Kphi,x1,x2,m,ms)
W=3000;
Ws=2700;
h=-1;
c=0.5;
Iz=40000;%lbs-ft^2
Ix=15000;%lbs-ft^2
t= 10;
dt = 0.01;
time = linspace(0,t,t/dt);
ef=0;
er=-0.03;
% State array initialization
v = zeros(1,length(time));
dv= zeros(1,length(time));
r = zeros(1,length(time));
dr = zeros(1,length(time));
phi = zeros(1,length(time));
dphi = zeros(1,length(time));
ddphi = zeros(1,length(time));
Cf = zeros(1,length(time));
Cr = zeros(1,length(time));
Cphif = zeros(1,length(time));
Cphir = zeros(1,length(time));
Ca = zeros(1,length(time));
Cb = zeros(1,length(time));
Cc = zeros(1,length(time));
Wdiff = zeros(1,length(time));
Wsum = zeros(1,length(time));
Wright = zeros(1,length(time));
Wleft = zeros(1,length(time));
Cf_left = zeros(1,length(time));
Cf_right = zeros(1,length(time));
for i = 1:1:(length(time)-1)
% Matrixes
A1=[m, 0, -ms*h;
0, Iz/32.2, -ms*h*c;
-ms*h, -ms*h*c, Ix/32.2];
A=inv(A1);
B=[-Ca(i)/u, -Cb(i)/u-m*u, 0, Cphif(i)+Cphir(i), Cf(i), Cr(i);
-Cb(i)/u, -Cc(i)/u, 0, x1*Cphif(i)+x2*Cphir(i), x1*Cf(i), x2*Cr(i);
0, ms*h*u, -Dphi, -Kphi, 0, 0];
xval = A*B*[v(i);r(i);dphi(i);phi(i);delta1(i);0];
%output with xval
dv(i)= xval(1);
dr(i)= xval(2);
ddphi(i)= xval(3);
%update state variables
v(i+1) = dv(i)*dt + v(i);
r(i+1) = dr(i)*dt + r(i);
dphi(i+1) = ddphi(i)*dt + dphi(i);
phi(i+1) = dphi(i)*dt + phi(i);
%update Cf,Cr,Cphif,Cphir,Ca,Cb,Cc,K2phi
%front
Wdiff(i+1)= ms/2*dv(i)*2/t;%Wdiff for one wheel,g=32.2,/2 for one wheel
Wsum(i+1)=(1/2)*Ws;
Wleft(i+1)=(Wdiff(i+1)+Wsum(i+1))/2;
Wright(i+1)=Wsum(i+1)-Wleft(i+1);
%left
Cf_left(i+1)=(0.2*(Wleft(i+1))-0.0000942*(Wleft(i+1))^2)*180/pi;
%right
Cf_right(i+1)=(0.2*(Wright(i+1))-0.0000942*(Wright(i+1))^2)*180/pi;
%front total
Cf(i+1)=Cf_right(i+1)+Cf_left(i+1);
%rear
Cr(i+1)=Cf(i+1);
Cphif(i+1)=Cf(i+1)*ef;
Cphir(i+1)=Cr(i+1)*er;
Ca(i+1)=Cf(i+1)+Cr(i+1);
Cb(i+1)=x1*Cf(i+1)+x2*Cr(i+1);
Cc(i+1)=x1^2*Cf(i+1)+x2^2*Cr(i+1);
end
end

%---------------------------------------------------------------------
%1.1
u1=30*5280/3600; % 30 mph in ft/s
u2=60*5280/3600; % 60 mph in ft/s
I=Iz/32.2; %unit conversion for lbf
%Eigenvalue code adapted from lecture notes
A1 =[ (-Ci-Ci)/(m*u1) (-x1*Ci-x2*Ci)/(m*u1^2)-1;
(-Ci*x1-Ci*x2)/I (-(x1)^2*Ci-(x2)^2*Ci)/(I*u1)];
eigval1 = eig(A1);
A2 =[ (-Ci-Ci)/(m*u2) (-x1*Ci-x2*Ci)/(m*u2^2)-1;
(-Ci*x1-Ci*x2)/I (-(x1)^2*Ci-(x2)^2*Ci)/(I*u2)];
eigval2 = eig(A2);

%---------------------------------------------------------------------
%1.2
spd=linspace(0,120,13); % generates the speed values to be iterated
u1=spd*5280/3600;%unit conversion from mph to ft/sec
l2=8 ; %wheelbase / ft
K2=(-m*(x1*Ci+x2*Ci))/(Ci*Ci*l2);
utrans=sqrt((-l2)*C2*x2/(m*x1))*3600/5280;
for i=1:13
ssyaw(i)=u1(i)/((l2)+u1(i)^2*K2);
end
figure(1)
plot(spd,ssyaw);
xlabel('Vehicle Speed (mph)');
ylabel('SS Yaw rate response (r / delta)');

%---------------------------------------------------------------------
%1.3
R=400;%turning radius in feet
l2=8 ; %wheelbase / ft
K2=(-m*(x1*Ci+x2*Ci))/(Ci*Ci*l2);
I=Iz/32.2; %unit conversion for lbf
speed=linspace(10,120,12); % generates the speed values to be iterated
u1=speed*5280/3600;%unit conversion from mph to ft/sec
for i=1:12
delta(i)=(l2+K2*(u1(i))^2)/R;
end
t= 10; % I assume steady state is achieved within 5 seconds, max time 10s
dt = 0.01; %time step interval
time = linspace(0,t,t/dt); %generates the time grid to iterate
for i = 1:1:length(speed)
uq3 = u1(i);
deltaqq3 = delta(i);
d_step(1:100) = 0;
d_step(101:1000) = deltaqq3;
[dbeta_loop,beta_loop,dr_loop,r_loop] = yaw(d_step,uq3,C1,C2,m,x1,x2,I,time,dt);
brate(i,:) = beta_loop./d_step;
rrate(i,:) = r_loop./d_step;
end

%---------------------------------------------------------------------
%1.4
t= 10; % I assume steady state is achieved within 5 seconds, max time 10s
dt = 0.01; %time step interval
time = linspace(0,t,t/dt); %generates the time grid to iterate
deltahw=zeros(1,t/dt); %starts at 0
for i=1:6
deltahw(100+i)=7.5*i; %changes from 0-45 in 0.0625 s
end
deltahw(107:394)=45; %constant
for i=1:12
deltahw(394+i)=45-7.5*i; %changes from 45 - -45 in 0.125 s
end
deltahw(407:694)=-45; %constant
for i=1:6
deltahw(694+i)=-45+7.5*i; %changes from -45 - 0 in 0.0625 s
end
drads=deltahw*pi/180/n; %converts from degrees to radians
figure(3);
subplot(2,1,1);
plot(time,deltahw);
title('Practical change in handwheel orientation(deg)')
subplot(2,1,2);
plot(time,drads)
title('Practical change in handwheel orientation(rad)')

%---------------------------------------------------------------------
%1.5
deltainput=deltahw*pi/180/n;
[dbetaq5_1,betaq5_1,drq5_1,rq5_1]=yaw(deltainput,44,C1,C2,m,x1,x2,I,time,dt);
[dbetaq5_2,betaq5_2,drq5_2,rq5_2]=yaw(deltainput,88,C1,C2,m,x1,x2,I,time,dt);
figure(4);
subplot(2,1,1);
plot(time,rq5_1,time,rq5_2);
legend('yaw rate-30 mph','yaw rate-60 mph');
title('yaw rate (r)')
subplot(2,1,2);
plot(time,betaq5_1,time,betaq5_2);
legend('drift angle-30 mph','drift angle-60 mph');
title('drift angle (beta)')

%---------------------------------------------------------------------
%1.6
%calculating the new biases
l2=8 ; %wheelbase / ft
speed=linspace(10,120,12); % generates the speed values to be iterated
u4=speed*5280/3600;%unit conversion from mph to ft/sec
R=400;%turning radius in feet
q6x1 =l2*60/100;
q6x2 =-l2*40/100;
q6c1 =2*(0.2*(4/10*W/2)-0.0000942*(4/10*W/2)^2)*180/pi;
q6c2 =2*(0.2*(6/10*W/2)-0.0000942*(6/10*W/2)^2)*180/pi;
q6K=(-m*(q6x1*q6c1+q6x2*q6c2))/(q6c1*q6c2*l2);
%Steering response (problem 3)
for i=1:12
deltac2(i)=(l2+q6K*(u4(i))^2)/R;
end
for i = 1:1:length(speed)
uq3c2 = u4(i);
deltaqqqq3 = deltac2(i);
delta_stepc2(1:100) = 0;
delta_stepc2(101:1000) = deltaqqqq3;
[dbeta_loopc2,beta_loopc2,dr_loopc2,r_loopc2] =
yaw(delta_stepc2,uq3c2,q6c1,q6c2,m,q6x1,q6x2,I,time,dt);
betaratec2(i,:) = beta_loopc2./delta_stepc2;
yawratec2(i,:) = r_loopc2./delta_stepc2;
end
figure(7)
subplot(2,1,1)
plot(time,betaratec2(1,:),time,betaratec2(2,:),time,betaratec2(3,:),time,betaratec2(4
,:),time,
betaratec2(5,:),time,betaratec2(6,:),time,betaratec2(7,:),time,betaratec2(8,:),time,b
etaratec2 (9,:),time,betaratec2(10,:),time,betaratec2(11,:),time,betaratec2( 12,:))
xlabel('time / s')
ylabel('beta/delta')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
title('40/60 nonlinear tire bias drift angle response')
subplot(2,1,2)
plot(time,yawratec2(1,:),time,yawratec2(2,:),time,yawratec2(3,:),time,yawratec2(4,:),
time,yawratec2(5,:),time,yawratec2(6,:),time,yawratec2(7,:),time,yawratec2(8,:),time,
yawratec2(9,:),time,yawratec2(10,:),time,yawratec2(11,:),time,yawratec2(12,:))
xlabel('time(sec)')
ylabel('r/delta')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
title('nonlinear 40/60 yaw rate response')
%yaw rate r and drift angle B vs time for steering input 1.4
deltainput=deltahw*pi/180/n;
[dbetaq5_3c2,betaq5_3c2,drq5_3c2,rq5_3c2]=yaw(deltainput,u1,q6c1,q6c2,m,q6x1,q6x2,I,t
ime,dt);
[dbetaq5_4c2,betaq5_4c2,drq5_4c2,rq5_4c2]=yaw(deltainput,u2,q6c1,q6c2,m,q6x1,q6x2,I,t
ime,dt);
figure(8);
subplot(2,1,1);
plot(time,betaq5_3c2,time,betaq5_4c2);
legend('beta-30 mph','beta-60 mph');
title('40/60 Rear Bias drift angle');
subplot(2,1,2);
plot(time,rq5_3c2,time,rq5_4c2);
legend('yaw rate-30 mph','yaw rate-60 mph');
title('40/60 Rear Bias yaw rate');
figure(9)
subplot(2,1,1);
plot(time,betaq5_3c2);
legend('beta-30 mph');
title('40/60 Rear Bias drift angle');
subplot(2,1,2);
plot(time,rq5_3c2);
legend('yaw rate-30 mph');
title('40/60 Rear Bias yaw rate');
figure(10)
subplot(4,1,1);
plot(time,betaq5_1,time,betaq5_1c1,time,betaq5_3c2);
legend('linear tires','nonlinear 60/40 front bias','nonlinear 40/60 rear bias');
title('drift angle - 30 mph');
subplot(4,1,2);
plot(time,betaq5_2,time,betaq5_2c1);
legend('linear tires','nonlinear 60/40 front bias');
title('drift angle - 60 mph');
subplot(4,1,3);
plot(time,rq5_1,time,rq5_1c1,time,rq5_3c2);
legend('linear tires','nonlinear 60/40 front bias','nonlinear 40/60 rear bias');
title('yaw rate - 30 mph');
subplot(4,1,4);
plot(time,rq5_2,time,rq5_2c1);
legend('linear tires','nonlinear 60/40 front bias');
title('yaw rate - 60 mph');

%---------------------------------------------------------------------
%2.1
%Variable declaration identical to part 1
u1=30*5280/3600; % 30 mph in ft/s - 44
u2=60*5280/3600; % 60 mph in ft/s - 88
Ca=Cf+Cr;
Cb=x1*Cf+x2*Cr;
Cc=x1^2*Cf+x2^2*Cr;
Kphi=(dldphif+dldphir)+ms*32.2*h;
Dphi=(dldphidf+dldphidr);
ef=0;
er=-0.03;
Cphif=Cf*ef;
Cphir=Cr*er;
Cphir2=0;
K2phi=(ms*h/Kphi*(-Ca*(x1*Cphif+x2*Cphir)+Cb*(Cphif+Cphir))-Cb*m)/(l2*Cf*Cr);
K2phie0=(ms*h/Kphi*(-Ca*(x1*Cphif+x2*Cphir2)+Cb*(Cphif+Cphir2))-Cb*m)/(l2*Cf*Cr);
t= 10; %system is simulated for 10 seconds
dt = 0.01; %10 ms step interval
time = linspace(0,t,t/dt); %time iteration
%3DOF SS yaw rate response, same from part 1
speed=linspace(0,120,13);
u1=speed*5280/3600;%converting to ft/sec
for i=1:13
r(i)=u1(i)/((l2)+u1(i)^2*K2phi);
end
for i=1:13
r2(i)=u1(i)/((l2)+u1(i)^2*K2phie0);
end
figure(1)
plot(speed,r,speed,r2);
xlabel('Vehicle Speed (mph)');
ylabel('SS Yaw rate response (3DOF)');
legend('roll steer,epsilon=-0.03','no roll steer,epsilon=0')

%---------------------------------------------------------------------
%2.2
%Adapted from 1.3 code
R=400;%turning radius in feet
speed=linspace(10,120,12); %speeds to iterate through
u1=speed*5280/3600;%this converts the mph speed to ft/s
for i=1:12
d(i)=(l2+K2phi*(u1(i))^2)/R;
end
for i = 1:1:length(speed)
uq8 = u1(i);
dq8 = d(i);
dstep(1:100) = 0;
dstep(101:1000) = dq8;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop] =
yawroll(dstep,uq8,Cf,Cr,Cphif,Cphir,Ca,Cb,Cc,Dphi,Kphi,x1,x2,m,ms);
betarate(i,:) = v_loop./dstep./uq8;
yawrate(i,:) = r_loop./dstep;
end

%---------------------------------------------------------------------
%2.3-4
d9=dhw*pi/180/n;
Cphifp=0.04*Cf;
Cphif0=0;
Cphifn=-0.04*Cf;
Cphirp=0.04*Cr;
cphir0=0;
Cphir_n=-0.04*Cr;
cphif9=[0.04*Cf; 0; -0.04*Cf];
cphir9=[0.04*Cr; 0; -0.04*Cr];
for i=1:3
for j=1:3
Cphif=cphif9(i);
Cphir=cphir9(j);
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop]=yawroll(d9,u1,Cf,Cr,Cph
if,Cphir,Ca,Cb,Cc,Dphi,Kphi,x1,x2,m,ms);
row = 3*(i-1)+j;
vs_loop(row,:)=v_loop./d9; %drift angle
rs_loopdel(row,:)=r_loop./d9; %yaw response
rs_loop(row,:)=r_loop; %yaw
end
end
figure(3)
subplot(2,1,1)
plot(time, rs_loopdel(1,:),time, rs_loopdel(2,:),time,
rs_loopdel(3,:),time,rs_loopdel(4,:),time, rs_loopdel(5,:),time,
rs_loopdel(6,:),time, rs_loopdel(7,:),time,rs_loopdel(8,:),time, rs_loopdel(9,:));
xlabel('t (s)');
ylabel('beta');
title('3DOF drift angle response');
legend('Model 1','Model 2','Model 3','Model 4','Model 5','Model 6','Model 7','Model
8','Model 9')
subplot(2,1,2)
plot(time, rs_loop(1,:),time, rs_loop(2,:),time, rs_loop(3,:),time,
rs_loop(4,:),time,rs_loop(5,:),time, rs_loop(6,:),time, rs_loop(7,:),time,
rs_loop(8,:),time, rs_loop(9,:));
xlabel('t (s)');
ylabel('r/delta');
title('3DOF yaw rate response');
legend('Model 1','Model 2','Model 3','Model 4','Model 5','Model 6','Model 7','Model
8','Model 9')
for i=1:3
for j=1:3
Cphif=cphif9(i);
Cphir=cphir9(j);
for k = 1:12
uq8 = u8(k);
deltaq8 = delta(k);
delta_step(1:100) = 0;
delta_step(101:1000) = deltaq8;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop]=yawroll(delta_step,uq8,
Cf,Cr,Cphif,Cphir,Ca,Cb,Cc,Dphi,Kphi,x1,x2,m,ms);
%vs_loop(row,:)=v_loop; %v for one pair of cphi
rs_loopq9(k,:)=r_loop./delta_step; %r for one pair of cphi
end
figure(4);
subplot(3,3,3*(i-1)+j);
plot(time,rs_loopq9);
xlabel('t (s)')
ylabel('r/delta')
%legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80
mph','90mph','100 mph','110 mph','120 mph')
end
end

%---------------------------------------------------------------------
%3.1
for i=1:12
delta(i)=(l2+K2phi*(u1(i))^2)/R;
end
for i = 1:1:length(speed)
u11 = u1(i);
d11 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d11;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u11,Dphi,Kphi,x1,x2,m,ms);
brate(i,:) = v_loop./ds./u11;
yrate(i,:) = r_loop./ds;
Cf3(i,:) = Cf;
Cr3(i,:) = Cr;
end
figure(1)
plot(time,yawrate(1,:),time,yawrate(2,:),time,yawrate(3,:),time,yawrate(4,:),time,yaw
rate(5,:),time,yawrate(6,:),time,yawrate(7,:),time,yawrate(8,:),time,yawrate(9,:),tim
e,yawrate(10,:),time,yawrate(11,:),time,yawrate(12,:))
xlabel('t (s)')
ylabel('r/delta')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
figure(2)
subplot(2,1,1)
plot(time,Cfpart3(1,:),time,Cfpart3(2,:),time,Cfpart3(3,:),time,Cfpart3(4,:),time,Cfp
art3(5,:),time,Cfpart3(6,:),time,Cfpart3(7,:),time,Cfpart3(8,:),time,Cfpart3(9,:),tim
e,Cfpart3(10,:),time,Cfpart3(11,:),time,Cfpart3(12,:))
xlabel('t (s)');
ylabel('K_f_r_o_n_t')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
subplot(2,1,2)
plot(time,Crpart3(1,:),time,Crpart3(2,:),time,Crpart3(3,:),time,Crpart3(4,:),time,Crp
art3(5,:),time,Crpart3(6,:),time,Crpart3(7,:),time,Crpart3(8,:),time,Crpart3(9,:),tim
e,Crpart3(10,:),time,Crpart3(11,:),time,Crpart3(12,:))
xlabel('t (s)');
ylabel('K_r_e_a_r')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')

%---------------------------------------------------------------------
%3.2
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr] =
yawroll(ds,u12,2500,15000,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u12,1000,9000,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u12,1500,15000,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
figure(1)
plot(time,yrate12(1,:),time,yrate12(2,:),time,yrate12(3,:),time,yrate12(4,:),time,yra
te12(5,:),time,yrate12(6,:),time,yrate12(7,:),time,yrate12(8,:),time,yrate12(9,:),tim
e,yrate12(10,:),time,yrate12(11,:),time,yrate12(12,:))
xlabel('t (s)')
ylabel('r/delta')
title('Increased Kphi')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u12,2500,10300,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
figure(2)
plot(time,yrate12(1,:),time,yrate12(2,:),time,yrate12(3,:),time,yrate12(4,:),time,yra
te12(5,:),time,yrate12(6,:),time,yrate12(7,:),time,yrate12(8,:),time,yrate12(9,:),tim
e,yrate12(10,:),time,yrate12(11,:),time,yrate12(12,:))
xlabel('t (s)')
ylabel('r/delta')
title('Increased Dphi')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u12,1500,9000,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
figure(3)
plot(time,yrate12(1,:),time,yrate12(2,:),time,yrate12(3,:),time,yrate12(4,:),time,yra
te12(5,:),time,yrate12(6,:),time,yrate12(7,:),time,yrate12(8,:),time,yrate12(9,:),tim
e,yrate12(10,:),time,yrate12(11,:),time,yrate12(12,:))
xlabel('t (s)')
ylabel('r/delta')
title('Reduced Kphi')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
for i = 1:1:length(speed)
u12 = u1(i);
d12 = delta(i);
ds(1:10) = 0;
ds(11:1000) = d12;
[v_loop,dv_loop,r_loop,dr_loop,phi_loop,dphi_loop,ddphi_loop,Wdiff,Wsum,Cf,Cr]
=yawroll(ds,u12,1000,10300,x1,x2,m,ms);
brate12(i,:) = v_loop./ds./u12;
yrate12(i,:) = r_loop./ds;
end
figure(4)
plot(time,yrate12(1,:),time,yrate12(2,:),time,yrate12(3,:),time,yrate12(4,:),time,yra
te12(5,:),time,yrate12(6,:),time,yrate12(7,:),time,yrate12(8,:),time,yrate12(9,:),tim
e,yrate12(10,:),time,yrate12(11,:),time,yrate12(12,:))
xlabel('t (s)')
ylabel('r/delta')
title('Reduced Dphi')
legend('10 mph','20 mph','30 mph','40 mph','50 mph','60 mph','70 mph','80 mph','90
mph','100mph','110 mph','120 mph')
