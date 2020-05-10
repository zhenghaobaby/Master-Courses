% Compute the probability density function of the price S(T)
% Inputs :
% volSurf : volatility surface data
% T: time to expiry of the option
% Ks: vector of strikes
% Output :
% cdf: cumulative distirbutoin function

% f(x)' = (f(x+h)-f(x-h))/2h
function cdf = getCdf ( volSurf , T, Ks)
    
    function C = func(K)
        [vols , fwd] = getVol ( volSurf , T, K);
        C =  getBlackCall (fwd, T, K , vols);
    end
    h = 0.001;
    
    function u = f(x)
        u = (func(x+h)-func(x-h))/(2*h)+1;
    end
    cdf = arrayfun(@f,Ks);
%     cdf = @f;

end