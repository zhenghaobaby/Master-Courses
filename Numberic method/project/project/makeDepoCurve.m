function curve = makeDepoCurve (ts , dfs)
% Inputs :
% ts: array of size N containing times to settlement in years
% dfs: array of size N discount factors
%compute method:
% r(t,T) = log(df_t/df_T))/(T-t) where T,t to settlemnt in years
% Output :
% curve : a struct containing data needed by getRateIntegral
    curve_rate = zeros(1,length(ts));
    curve_rate(1) = -log(dfs(1))/ts(1);
    index_1 = 1:1:length(ts)-1;
    index_2 = 2:1:length(ts);
    curve_rate(index_2) = log(dfs(index_1)./dfs(index_2))./(ts(index_2)-ts(index_1));
    

    % only can extrapolate for 30 day
    function rate = CurveRate(t)
        if t>ts(length(ts))
            if t<ts(length(ts))+30/365.0
                rate = curve_rate(length(curve_rate));
            else
            fprintf('exceed max tenor!!!\n');
            rate = -1;
            return 
            end
        else
            position = BinarySearch(t,ts);
            rate = curve_rate(position);
        end      
    end
    curve = @CurveRate;
end


