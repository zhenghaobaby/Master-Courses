% Inputs :
% curve : pre - computed fwd curve data
% T: forward spot date
% Output :
% fwdSpot : E[S(t) | S (0)]
function fwdSpot = getFwdSpot (curve , T)
    [fp,s,lag] = curve(T);
    if T==0
        fwdSpot = s(1);
        return
    end
    N = 1000;
    delta = T/N;
    [fp,s,~] = arrayfun(curve,[lag:delta:T+lag]);
    fwdrate = delta*sum(fp);
    fwdSpot = s(1)*exp(fwdrate);
 
end