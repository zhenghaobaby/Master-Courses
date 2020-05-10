% Inputs :
% fwd: forward spot for time T, i.e. E[S(T)]
% T: time to expiry of the option
% cp: 1 for call , -1 for put
% sigma : implied Black volatility of the option
% delta : delta in absolute value (e.g. 0.25)
% Output :
% K: strike of the option
function K = getStrikeFromDelta (fwd , T, cp , sigma , delta )
    if cp==1
        Nd1=delta;
    elseif cp==-1
        Nd1=1-delta;
    else
        error("please give right type of option, 1 for call, -1 for put");
    end
    function f = myfunc(x)
        f = normcdf((log(fwd)-log(x))/(sigma*sqrt(T))+0.5*sigma*sqrt(T))-Nd1;
    end
%     K = secant(@myfunc,0.1,5,1.0e-5,200);
    d1 = norminv(Nd1);
    K = exp(log(fwd)+sigma*sqrt(T)*(0.5*sigma*sqrt(T)-d1));
end

        
        
        
    