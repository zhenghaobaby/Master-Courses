% Computes the price of a European payoff by integration
% Input :
% volSurface : volatility surface data
% T : time to maturity of the option
% payoff : payoff function
% ints : optional , repartition of integration intervals e.g. [0, 3, +Inf]
% Output :
% u : forward price of the option ( undiscounted price )
function u = getEuropean ( volSurface , T, payoff , ints )
  pdf = getPdfunc(volSurface ,T);
  func = @(x)pdf(x).*payoff(x);
if nargin==3
    interval = 0.1;
    min = 0;
    max = inf;
elseif nargin==4
    if length(ints)==2
        interval = 0.1;
        min = ints(1);
        max = ints(2);
    elseif length(ints)==3
        interval = ints(2);
        min = ints(1);
        max = ints(3);
    end
else
    error("ints form is wrong");
end
    e = 1e-8;
    b = 0.1;
    while pdf(b+1)>e
        b=b+1;
    end
    if b<max
        max=b;
    end
    yi = arrayfun(func,[min:interval:max]);
    u = interval*sum(yi);
end
   
      

    

