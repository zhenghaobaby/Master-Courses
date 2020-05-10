% Inputs :
% curve : pre - computed data about an interest rate curve
% t: time
% Output :
% integ : integral of the local rate function from 0 to t
function integ = getRateIntegral (curve , t)
    N = 1000;
    delta = t/N;
    yi = arrayfun(curve,[0:N-1]*delta);
    integ = delta*sum(yi);
end
