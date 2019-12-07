% code from Choe.
% binomial tree method for American and European put options
S0 = 100;
K = 110;
T = 1;
r = 0.05;
sigma = 0.3;
M = 1000; % number of time steps
dt = T/M;
u = exp(sigma*sqrt(dt));
d = exp(-sigma*sqrt(dt));
q = (exp(r*dt)-d)/(u-d);
Put_Am = max(K - S0*u.^([M:-1:0]').*d.^([0:1:M]'),0);
Put_Eu = max(K - S0*u.^([M:-1:0]').*d.^([0:1:M]'),0);
for i = M:-1:1
    S = S0*u.^([i-1:-1:0]').*d.^([0:1:i-1]');
    Put_Am =max(max(K-S,0),exp(-r*dt)*(q*Put_Am(1:i)+(1-q)*Put_Am(2:i+1)));
    Put_Eu =exp(-r*dt)*(q*Put_Eu(1:i)+(1-q)*Put_Eu(2:i+1));
end
Put_Am
Put_Eu

d1 = (log(S0/K)+(r+0.5*sigma^2)*T)/(sigma*sqrt(T));
d2 = d1 - sigma*sqrt(T);
Put_Eu_ex = K*exp(-r*T)*normcdf(-d2) - S0*normcdf(-d1)
