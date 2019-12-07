S0 = 100;
K = 110;
r = 0.05;
sigma = 0.3;
T = 1;

L = 60; % a lower barrier
d1K = (log(S0/K) + (r + 0.5*sigma^2)*T)/(sigma*sqrt(T));
d2K = (log(S0/K) + (r - 0.5*sigma^2)*T)/(sigma*sqrt(T));
d1L = (log(S0/L) + (r + 0.5*sigma^2)*T)/(sigma*sqrt(T));
d2L = (log(S0/L) + (r - 0.5*sigma^2)*T)/(sigma*sqrt(T));
d3 = (log(L/S0) + (r + 0.5*sigma^2)*T)/(sigma*sqrt(T));
d4 = (log(L/S0) + (r - 0.5*sigma^2)*T)/(sigma*sqrt(T));
d5 = (log(L^2/S0/K) + (r + 0.5*sigma^2)*T)/(sigma*sqrt(T));
d6 = (log(L^2/S0/K) + (r - 0.5*sigma^2)*T)/(sigma*sqrt(T));
put_vanilla = K*exp(-r*T)*normcdf(-d2K) - S0*normcdf(-d1K);
P2 = - K*exp(-r*T)*normcdf(-d2L) + S0*normcdf(-d1L) ;
P3 = - K*exp(-r*T)*(L/S0)^(2*r/sigma^2-1)*(normcdf(d4)-normcdf(d6));
P4 = S0*(L/S0)^(2*r/sigma^2+1)*(normcdf(d3)-normcdf(d5));
P_do = put_vanilla + P2 + P3 + P4
% the above exact price of a down-and-out put option is derived
% in Theorem 18.3 of Choe's book.

N = 10000;
dt = T/N;
M = 10^4;
V1 = zeros(M,1);
V2 = zeros(M,1);
V_anti = zeros(M,1);
S1 = ones(1,N+1);
S2 = ones(1,N+1);
rng(1)
for i=1:M
    S1(1,1) = S0;
    S2(1,1) = S0;
    dW = sqrt(dt)*randn(1,N);
    for j = 1:N
        S1(1,j+1) = S1(1,j)*exp((r-0.5*sigma^2)*dt + sigma*dW(1,j));
        S2(1,j+1) = S2(1,j)*exp((r-0.5*sigma^2)*dt - sigma*dW(1,j));
    end
    S1_min = min(S1(1,:));
    S2_min = min(S2(1,:));
    if S1_min > L
        V1(i) = exp(-r*T)*max(K - S1(1,N+1),0);
    else
        V1(i) = 0;
    end
    if S2_min > L
        V2(i) = exp(-r*T)*max(K - S2(1,N+1),0);
    else
        V2(i)=0;
    end
    V_anti(i) = (V1(i)+V2(i))/2;
end

a = mean(V1)
b = var(V1)
a_anti = mean(V_anti)
b_anti = var(V_anti)
ratio = b/b_anti