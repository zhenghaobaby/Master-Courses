S0 = 100;
K = 40; % A deep in-the-money case chosen for the best looking plot.
r = 0.05;
T = 5;
sigma_market = 0.1; % a given condition
n = 20; %number of iterations
sigma0 = sqrt(2*abs((log(S0/K)+r*T)/T))
% definitions of functions
d1 = @(x) (log(S0/K)+(r+x.^2/2)*T)./(x*sqrt(T));
d2 = @(x) (log(S0/K)+(r-x.^2/2)*T)./(x*sqrt(T));
C = @(x) S0*normcdf(d1(x))-K*exp(-r*(T))*normcdf(d2(x));
vega = @(x) S0*sqrt(T)*normpdf(d1(x));
C_market=C(sigma_market); % observed in the market
F = @(x) C(x)-C_market;
sigma = zeros(1,n);
sigma(1)=sigma0;
for i=1:1:n-1
    sigma(i+1)=sigma(i) - F(sigma(i))/vega(sigma(i));
end
figure(1)
subplot(1,2,1);
error=zeros(1,n);
for i=1:n;
    error(i)=abs(sigma_market-sigma(i));
end
semilogy(error,'o-');
ylabel('error')
xlabel('number of iterations')
hold off
subplot(1,2,2);
x=0:0.01:2;
plot(x,C(x),'k');
hold on
plot(sigma,C(sigma),'bo');
hold on
plot(sigma_market,C_market,'r*');
xlabel('sigma')
ylabel('call option price')