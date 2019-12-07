S0 = 100;
K = 110;
r = 0.05;
sigma = 0.3;
T = 1;
L = 12; % number of observations
dt = T/L;
sigma_bar = sqrt( sigma^2*(L+1)*(2*L+1)/(6*L^2));
mu_bar = 1/2*sigma_bar^2 + (r-1/2*sigma^2)*(L+1) / (2*L);
d1 = (log(S0/K) + (mu_bar+1/2*sigma_bar^2)*T)/(sigma_bar*sqrt(T));
d2 = (log(S0/K) + (mu_bar-1/2*sigma_bar^2)*T)/(sigma_bar*sqrt(T));
V_geo_formula = S0*exp((mu_bar -r)*T)*normcdf(d1) -K*exp(-r*T)*normcdf(d2);
J = 20;
ave = zeros(J,1);
ave_control = zeros(J,1);
error = zeros(J,1);
error_control = zeros(J,1);
ratio = ones(J,1);
S = ones(2^J,L);
rng(1);
dW = sqrt(dt)*randn(2^J,L);
for i=1:2^J
    S(i,1) = S0*exp((r-1/2*sigma^2)*dt +sigma*dW(i,1)); %asset price at T_1
    for j=2:L
        S(i,j) = S(i,j-1) *exp((r-1/2*sigma^2)*dt+ sigma*dW(i,j));
    end
end
J1 = 12;
for n=J1:J
    N = 2^n;
    V_arith = exp(-r*T) * max( mean(S(1:N,:),2) - K , 0);
    ave(n) = mean(V_arith);
    var_V_arith = var(V_arith);
    error(n) = 1.96*sqrt(var_V_arith)/sqrt(N);
    V_geo = exp(-r*T) * max( exp(mean(log(S(1:N,:)),2)) - K , 0);
    V = V_arith - V_geo + V_geo_formula;
    ave_control(n) = mean(V);
    var_control = var(V);
    error_control(n) = 1.96*sqrt(var_control)/sqrt(N);
    ratio(n) = var_V_arith/var_control;
end
errorbar(J1:J, ave(J1:J), error(J1:J), 'ro--')
hold on
errorbar(J1:J, ave_control(J1:J), error_control(J1:J),'k*-','linewidth',2)
legend('standard', 'control variate');
xlabel('log_2(N)');
ylabel('Price');