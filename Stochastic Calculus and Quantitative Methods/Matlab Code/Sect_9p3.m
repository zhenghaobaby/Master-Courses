S0 = 100;
K = 110;
sigma = 0.3;
r = 0.05;
T = 0.5;
% Black-Scholes-Merton formula
d1 = (log(S0/K)+(r+0.5*sigma^2)*T)/(sigma*sqrt(T));
d2 = d1 - sigma*sqrt(T);
N1 = normcdf(d1);
N2 = normcdf(d2);
Call_formula = S0*N1 - K*exp(-r*T)*N2;
% option price
J = 16;
L = 2^J;
rng(0);
W = sqrt(T)*randn(L,1);
S = S0*exp((r-0.5*sigma^2)*T + sigma*W); % S_T
V = exp(-r*T)*max(S - K,0);
figure(1)
for j = 9:J
    M(j) = 2^j; % number of samples
    a(j) = mean(V(1:M(j)));
    b(j) = 1.96*std(V(1:M(j)))/sqrt(M(j));
end
x = 8:0.01:J+1;
semilogx(x,Call_formula*ones(length(x),1),'r')
axis([min(x),max(x),4,6.5])
hold on
errorbar(9:J,a(9:J),b(9:J));
xlabel('log_2(N)')
ylabel('call price');