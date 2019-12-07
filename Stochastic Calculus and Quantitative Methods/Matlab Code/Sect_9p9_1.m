% estimate P(X>a) with X~N(0,1) use importance sampling
% the exact value is 2.867e-7
b = 5;
N = 10000;
rng(1);
X = randn([N,1]);
Z1 = X>b;
mu1 = sum(Z1)/N
var1 = var(Z1)

theta = 6;
Y = X + theta;
Z2 = (Y>b).*exp(-theta*Y+0.5*theta^2);
mu2 = sum(Z2)/N
var2 = var(Z2)

% confidence interval
c = 2*sqrt(var2/N);
[mu2-c, mu2+c]