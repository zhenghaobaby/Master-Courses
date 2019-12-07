S0 = 100;
K = 110;
r = 0.05;
sigma = 0.3;
T = 1;
d1 = (log(S0/K) + (r + 0.5*sigma^2)*T)/(sigma*sqrt(T));
d2 = (log(S0/K) + (r - 0.5*sigma^2)*T)/(sigma*sqrt(T));
call_vanilla = S0*normcdf(d1) - K*exp(-r*T)*normcdf(d2)

N = 1000;
dt = T/N;
M = 10^5;
S = ones(1,N+1);
S2 = ones(1,N+1);
V = zeros(M,1);
V2 = zeros(M,1);
V_anti = zeros(M,1);
rng(1)
for i = 1:M
    S(1,1) = S0;
    S2(1,1) = S0;
    dW = sqrt(dt)*randn(1,N);
    for j = 1:N
        S(1,j+1) = S(1,j)*exp((r-0.5*sigma^2)*dt + sigma*dW(1,j));
        S2(1,j+1) = S2(1,j)*exp((r-0.5*sigma^2)*dt - sigma*dW(1,j));
    end
    V(i) = exp(-r*T)*max(S(1,N+1)-K,0);
    V2(i) = exp(-r*T)*max(S2(1,N+1)-K,0);
    V_anti(i) = (V(i)+V2(i))/2;
end
a = mean(V)
b = var(V)
a_anti = mean(V_anti)
b_anti = var(V_anti)
ratio = b/b_anti