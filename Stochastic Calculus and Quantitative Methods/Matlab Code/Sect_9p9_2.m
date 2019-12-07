S0 = 100;
K = 150;
r = 0.05;
sigma = 0.3;
T = 1;
L = 12; % number of measurements
dt = T/L;
r1 = r + 0.5;
theta = (r - r1)/sigma;
M = 10^6;
rng(1);
dW = sqrt(dt)*randn(M,L);
W = sum(dW,2);
RN = exp(-0.5*theta^2*T + theta*W); % Radon-Nikodym derivative dQ/dQ1
S = zeros(M,L);
for i=1:M
    S(i,1) = S0*exp((r-1/2 *sigma^2)*dt + sigma*dW(i,1));
    for j=2:L
        S(i,j) = S(i,j-1) * exp((r-1/2*sigma^2)*dt+ sigma*dW(i,j));
    end
end
S1 = zeros(M,L);
for i=1:M
    S1(i,1) = S0*exp((r1-1/2 *sigma^2)*dt + sigma*dW(i,1));
    for j=2:L
        S1(i,j) = S1(i,j-1) * exp((r1-1/2*sigma^2)*dt+ sigma*dW(i,j));
    end
end
V = exp(-r*T) * max( mean(S(1:M,:),2) - K, 0);
price = mean(V)
variance = var(V)
V1 = exp(-r*T) * max( mean(S1(1:M,:),2) - K, 0);
price1 = mean(V1.*RN)
variance1 = var(V1.*RN)
ratio = variance / variance1