% Inputs :
% fwd: forward spot for time T, i.e. E[S(T)]
% T: time to expiry of the option
% cps: vetor if 1 for call , -1 for put
% deltas : vector of delta in absolute value (e.g. 0.25)
% vols : vector of volatilities
% Output :
% Ks: strikes obtained from delta
% curve : a struct containing data needed in getSmileK
function [ curve ]= makeSmile (fwd , T, cps , deltas , vols )
    fwd = getFwdSpot(fwd,T);
    strikes = arrayfun(@getStrikeFromDelta,repelem(fwd,length(cps)),repelem(T,length(cps)),cps,vols,deltas);
    %only check for call option
    strikes_check = [0,strikes(1:length(strikes))]; % add zero
    vols_check = [0,vols(1:length(vols))]; %add zero
    call_C = getBlackCall(fwd, T, strikes_check , vols_check);
    
    %check three types of arbitrage
    %check c>0
    if any(call_C<0)
        error("call option price less than zero!");
    end
    
    %check monotonically decrese
    first_diff = diff(call_C)./diff(strikes_check);
    if any(first_diff<=-1)|| any(first_diff>=0)
        error("call option price don't monotonically decrease")
    end
    
    %check gradient of price
    second_diff = diff(first_diff);
    sign_diff = sign(second_diff);
    if any(sign_diff==-1)
        error("the gradient of the price is not increasing")
    end

    
   
    %calculate the coffecients of spline
    polyfit = spline(strikes,vols);
    KL = strikes(1)*strikes(1)/strikes(2);
    KR = strikes(end)*strikes(end)/strikes(end-1);
    bR = atanh(sqrt(0.5))/(KR-strikes(end));
    bL = atanh(sqrt(0.5))/(strikes(1)-KL);
    
    
    sigma_K1 = polyfit.coefs(1,3);
    sigma_KN = polyfit.coefs(end,1)*3*(strikes(end)-strikes(end-1))^2+ polyfit.coefs(end,2)*2*(strikes(end)-strikes(end-1))+polyfit.coefs(end,3);
    aR = sigma_KN/bR;
    aL = sigma_K1/-bL;
   
    function vol = interpolation(K)
        if K<strikes(1)   %K<K1
         vol = ppval( polyfit,strikes(1))+aL*tanh(bL*(strikes(1)-K));
        elseif K>strikes(end)  %K>Kn
         vol = ppval( polyfit,strikes(end))+aR*tanh(bR*(K-strikes(end)));
        else
         vol = ppval( polyfit,K);
        end
    end
    curve = @interpolation; 
end