% Inputs :
% curve : pre - computed smile data
% Ks: vetor of strikes
% Output :
% vols : implied volatility at strikes Ks
function vols = getSmileVol (curve , Ks)
    vols = arrayfun(curve,Ks);
end