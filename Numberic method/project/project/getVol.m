% Inputs :
% volSurf : volatility surface data
% T: time to expiry of the option
% Ks: vetor of strike
% Output :
% vols : volatilities
% fwd: forward spot price for maturity T
function [vols , fwd] = getVol ( volSurf , T, Ks)
    Ts = volSurf(1).tenor; %get tenor
    fwdCurve = volSurf(1).fwdCurve; %get fwdCurve
    
    if T<Ts(1)
        vols = getSmileVol(smile_curve(1).func, Ks);
        fwd = getFwdSpot(fwdCurve,T);
        return 
        
    elseif T>Ts(end)
        error("exceed max tenor");
    else
        pos = BinarySearch(T,Ts); %search T belongs to which interval.
        fwd = getFwdSpot(fwdCurve,T);
        moneyness = Ks/fwd;  %calculate the moneyness line
        
        G0_Ti =  getFwdSpot(fwdCurve,Ts(pos-1));
        G0_Ti1 = getFwdSpot(fwdCurve,Ts(pos));
        K_Ti = moneyness*G0_Ti;
        K_Ti1 = moneyness*G0_Ti1;
        sigma_Ti = getSmileVol(volSurf(pos-1).func, K_Ti); % get vol from Ti smile
        sigma_Ti1 = getSmileVol(volSurf(pos).func,K_Ti1); % get vol from Ti+1 smile
        
        T_i1 = Ts(pos);
        T_i = Ts(pos-1);
        total_vol = 1./(T_i1-T_i).*((T_i1-T).*sigma_Ti.^2*T_i+(T-T_i).*sigma_Ti1.^2*T_i1);
        
        vols = sqrt(total_vol/T);
    end
        
    
    
    
    

    
    
    
    

