% Inputs :
% fwdCurve : forward curve data
% Ts: vector of expiry times
% cps: vetor if 1 for call , -1 for put
% deltas : vector of delta in absolute value (e.g. 0.25)
% vols : matrix of volatilities
% Output :
% surface : a struct containing data needed in getVol
function volSurf = makeVolSurface ( fwdCurve , Ts , cps , deltas , vols )
    K = ones(length(Ts),length(deltas));
    fwd = ones(length(Ts),1);
    for i=1:length(Ts)
        fwd(i) = getFwdSpot(fwdCurve, Ts(i)); 
        smile_curve(i).func = makeSmile(fwdCurve, Ts(i), cps, deltas, vols(i,:)); %save ten tenors smiles
        smile_curve(i).fwdCurve = fwdCurve;
        smile_curve(i).tenor = Ts;
    end
    
    
    %check arbitrage for k = fwd
    for i=1:length(Ts)-1
        atmvol_t1 = getSmileVol(smile_curve(i).func, fwd(i));
        C_T1 = getBlackCall(fwd(i),Ts(i),fwd(i),atmvol_t1);
        atmvol_t2 = getSmileVol(smile_curve(i+1).func,fwd(i+1));
        C_T2 = getBlackCall(fwd(i+1),Ts(i+1),fwd(i+1),atmvol_t2);
        if C_T1>=C_T2
            error("the price of call option on moneyness line is not increasing");
        else
            continue;
        end
    end
    volSurf = smile_curve;
    
        

 
    
    
    
    
