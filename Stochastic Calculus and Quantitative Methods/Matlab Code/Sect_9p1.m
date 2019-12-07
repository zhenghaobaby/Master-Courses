% syms x; mu=int((cos(50*x)+sin(20*x)).^2,0,1)
% the following mu is the exact value of E[h(X)]
mu=1/200*sin(100)+103/105-1/70*cos(70)+1/30*cos(30)-1/80*sin(40);

% now, we pretend that we do not know the exact value of mu
% we try Monte Carlo method to estimate mu
x=linspace(0,1,1000);
h=(cos(50*x)+sin(20*x)).^2;
figure; subplot(1,3,1); plot(x,h);

rand('state',5);
N=100; L=1000;
n=zeros(N,1); muEst=zeros(N,1);
r=rand(N*L,1);
for k=1:N
    n(k)=L*k;  % number of samples
    x=r(1:n(k));
    h=(cos(50*x)+sin(20*x)).^2;
    muEst(k)=sum(h)/n(k);
end
err=abs(muEst-mu);

subplot(1,3,2); semilogx(n,muEst);

subplot(1,3,3); loglog(n,err); hold on;
loglog(n,1./sqrt(n),'r:','LineWidth',3);
legend('err vs number of trials','1/sqrt(number of trials)');
