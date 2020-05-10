% Compute the probability density function of the price S(T)
% Inputs :
% volSurf : volatility surface data
% T: time to expiry of the option
% Ks: vector of strikes
% Output :
% pdf: vector of pdf(ks)

% f(x)'' = (f(x+h)+f(x-h)-2f(x))/h^2
function pdf = getPdf ( volSurf , T, Ks)
    
    function C = func(K)
        [vols , fwd] = getVol ( volSurf , T, K);
        C =  getBlackCall (fwd, T, K , vols);
    end
    h = 1e-7;
    function u = f(x)
        u = (func(x+h)+func(x-h)-2*func(x))/h^2;
    end
    pdf = arrayfun(@f,Ks);
%     pdf = @f;
end

        
    
        
        
    
    
    
