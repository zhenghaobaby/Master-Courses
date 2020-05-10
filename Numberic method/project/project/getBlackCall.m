function u = getBlackCall (f, T, Ks , Vs)
% Inputs :
% f: forward spot for time T, i.e. E[S(T)]
% T: time to expiry of the option
% Ks: vector of strikes
% Vs: vector of implied Black volatilities
% Output :
% u: vector of call options undiscounted prices
    function value = BS(f,T,Ks,Vs)
        if Ks<=0
            value=f;
        elseif Ks==inf
            value=0;
        else
             d1 = (log(f)-log(Ks))/(Vs*sqrt(T))+0.5*Vs*sqrt(T);
             d2 = d1-Vs*sqrt(T);
             value=f*normcdf(d1)-Ks*normcdf(d2);
        end
    end
    u = arrayfun(@BS,repelem(f,length(Ks)),repelem(T,length(Ks)),Ks,Vs);
end