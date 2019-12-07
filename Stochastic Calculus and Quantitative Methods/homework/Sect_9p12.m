function [Price,CF,S,t] = AmericanOptLSM(S0,K,r,T,sigma,N,M,type)

%AmericanOptLSM - Price an american option via Longstaff-Schwartz Method
%
%  By Mark Hoyle
%  https://www.mathworks.com/matlabcentral/fileexchange/16476-pricing-american-options?focused=6781443&tab=function
%
% Inputs:
%
%   S0      Initial asset price
%   K       Strike Price
%   r       Interest rate
%   T       Time to maturity of option
%   sigma   Volatility of underlying asset
%   N       Number of points in time grid to use (minimum is 3, default is 50)
%   M       Number of points in asset price grid to use (minimum is 3, default is 50)
%   type    True (default) for a put, false for a call

if nargin < 6 || isempty(N), N = 50; elseif N < 3, error('N has to be at least 3'); end
if nargin < 7 || isempty(M), M = 50; elseif M < 3, error('M has to be at least 3'); end
if nargin < 8, type = true; end
dt = T/N;

t = 0:dt:T;
t = repmat(t',1,M);

rng(1);
R = exp((r-sigma^2/2)*dt+sigma*sqrt(dt)*randn(N,M));
S = cumprod([S0*ones(1,M); R]);

ExTime = (M+1)*ones(N,1); 

% Now for the algorithm
CF = zeros(size(S)); % Cash flow matrix

CF(end,:) = max(K-S(end,:),0); % Option only pays off if it is in the money

for ii = size(S)-1:-1:2
    if type
        Idx = find(S(ii,:) < K); % Find paths that are in the money at time ii
    else
        Idx = find(S(ii,:) > K); % Find paths that are in the money at time ii
    end
    X = S(ii,Idx)'; X1 = X/S0;
    Y = CF(ii+1,Idx)'*exp(-r*dt); % Discounted cashflow
    R = [ ones(size(X1)) (1-X1) 1/2*(2-4*X1-X1.^2)];
    a = R\Y; % Linear regression step
    C = R*a; % Cash flows as predicted by the model
    if type
        Jdx = max(K-X,0) > C; % Immediate exercise better than predicted cashflow
    else
        Jdx = max(X-K,0) > C; % Immediate exercise better than predicted cashflow
    end
    nIdx = setdiff((1:M),Idx(Jdx));
    CF(ii,Idx(Jdx)) = max(K-X(Jdx),0);
    ExTime(Idx(Jdx)) = ii;
    CF(ii,nIdx) = exp(-r*dt)*CF(ii+1,nIdx);
end

Price = mean(CF(2,:))*exp(-r*dt);
end