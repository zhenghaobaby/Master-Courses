% Inputs :
% domCurve : domestic IR curve data
% forCurve : Foreign IR curve data
% spot : spot exchange rate
% tau: lag between spot and settlement
% Output :
% curve : a struct containing data needed by getFwdSpot
function curve = makeFwdCurve ( domCurve , forCurve , spot , tau)
    function [fp,s,lag] = FwdCurve(t)
        if domCurve(t+tau)~=-1
            fp=domCurve(t)-forCurve(t); 
            s = spot;
            lag = tau;
            return
        else
            error("exceed max tenor!!!\n");
        end
    end
    curve = @FwdCurve;
end
        
        
    