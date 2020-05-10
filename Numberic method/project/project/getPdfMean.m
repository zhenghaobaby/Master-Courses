% Compute the probability density function of the price S(T)
% Inputs :
% volSurf : volatility surface data
% T: time to expiry of the option
% Ks: vector of strikes
% Output :
% pdf mean: function: pdf * x

% f(x)'' = (f(x+h)+f(x-h)-2f(x))/h^2
function pdfMean = getPdfMean( volSurf , T)
    
    function C = func(K)
        [vols , fwd] = getVol ( volSurf , T, K);
        C =  getBlackCall (fwd, T, K , vols);
    end
    h = 0.01;
    function u = f(x)
        u = x.*((func(x+h)+func(x-h)-2*func(x))/h^2);
    end
    pdfMean = @f;
end
