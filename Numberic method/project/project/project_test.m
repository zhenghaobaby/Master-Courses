function project_test()
    tic;
    % clear all;clc
    epsilon = 0.001; % allowed error
    % read data
    [spot, lag, days, domdfs, fordfs, vols, cps, deltas] = getMarket();
    tau = lag / 365; % spot rule lag
    Ts = days / 365; % time to maturities in years
    % construct market objects
    domCurve = makeDepoCurve(Ts, domdfs);
    forCurve = makeDepoCurve(Ts, fordfs);
    fwdCurve = makeFwdCurve(domCurve, forCurve, spot, tau);
    volSurface = makeVolSurface(fwdCurve, Ts, cps, deltas, vols);

    
    % test getBlackCall
    res1=abs(getBlackCall(100,1,100,0.5) - 19.7413);
    res2=abs(getBlackCall(100,2,[90, 100, 110],[0.1, 0.5, 1]) - [11.7725, 27.6326, 49.7571]);
    if all(res1<epsilon) & all(res2<epsilon)
        disp('pass: getBlackCall')
    else
        disp('fail: getBlackCall')
    end
    
    
    % test getRateIntegral
    res = exp(getRateIntegral(domCurve,Ts(end))) - 1/domdfs(end);
    % If a function is stepwise constant, it's integral should be linear,
    % and the derivative of the integral is constant.
    result = zeros(1,1000);
    for t = 1:1000
        result(t) = getRateIntegral(domCurve,t/1000);
    end
    result_diff = diff(diff(result));
    if (abs(res) < epsilon) && all(abs(result_diff)<epsilon)
        disp('pass: getRateIntegral')
    else
        disp('fail: getRateIntegral')
    end
    
    
    % test getFwdSpot
    res = getFwdSpot(fwdCurve ,Ts(end)) - spot*fordfs(end)/domdfs(end);
    result = zeros(1,1000);
    for t = 1:1000
        result(t) = getFwdSpot(fwdCurve,t/1000);
    end
    result_diff = diff(diff(result));
    if (abs(res) < epsilon) && all(abs(result_diff)<epsilon)
        disp('pass: getFwdSpot')
    else
        disp('fail: getFwdSpot')
    end


    % test getStrikeFromDelta
    fwd = getFwdSpot(fwdCurve,Ts(end));
    Ks = arrayfun(@getStrikeFromDelta,repelem(fwd,length(cps)),repelem(Ts(end),length(cps)),cps,vols(end,:),deltas);
    deltas_test = arrayfun(@getStrikeFromDelta_test,repelem(fwd,length(cps)),repelem(Ts(end),length(cps)),cps,vols(end,:),Ks);
    if abs(deltas_test-deltas) < epsilon
        disp('pass: getStrikeFromDelta')
    else
        disp('fail: getStrikeFromDelta')
    end



    % test getSmileVol
    smile = makeSmile(fwdCurve, Ts(end), cps, deltas, vols(end,:));
    vols_test = arrayfun(smile,Ks);
    if abs(vols(end,:)-vols_test) < epsilon
        disp('pass: getSmileVol')
    else
        disp('fail: getSmileVol')
    end

    % test getVol
    flag_getVol = 1;
    i = 2;
    while i <= length(Ts) & flag_getVol
        fwd = getFwdSpot(fwdCurve,Ts(i));
        Ks = arrayfun(@getStrikeFromDelta,repelem(fwd,length(cps)),...
            repelem(Ts(i),length(cps)),cps,vols(i,:),deltas);
        [vol_test,f] = getVol(volSurface, Ts(i), Ks);
        if abs(vols(i,:)-vol_test) >= epsilon
            flag_getVol = 0;
            disp(i)
        end
        i = i+1;
    end

    if flag_getVol
        disp('pass: getVol')
    else
        disp('fail: getVol')
    end


    % test getPdf
    % test whether integral of pdf is 1
    pdf_func = getPdfunc(volSurface,Ts(end));
    % test whether the mean is the forward (fail after modification of getFwdSpot)
    pdf_func_mean = getPdfMean(volSurface,Ts(end));
    fwd = getFwdSpot(fwdCurve,Ts(end));
    if (integral(pdf_func,0.1,10)-1 < epsilon) & (integral(pdf_func_mean,0.1,10)-fwd < epsilon)
        disp('pass: getPdf')
    else
        disp('fail: getPdf')
    end

    % test getEuropean
    % whether match with BS formula
    flag_Euro = 1;
    K = 1.4;
    for time = [0.8,Ts(end)]
        fwd = getFwdSpot(fwdCurve, time);
        [vols , ~] = getVol ( volSurface , time, fwd);
        if (abs(getBlackCall(fwd, time, K, vols(1))-...
            getEuropean(volSurface,time,@(x)max(x-K,0))) > epsilon)||...
            (abs(getBlackPut(fwd, time, K, vols(1))-...
            getEuropean(volSurface,time,@(x)max(K-x,0),[0.2,+Inf])) > epsilon)
            flag_Euro = 0;
        end
    end
    lhs = getEuropean(volSurface,time,@(x)max(x-K,0)-max(x-K-1,0));
    rhs = getEuropean(volSurface,time,@(x)max(x-K,0))-...
        getEuropean(volSurface,time,@(x)max(x-K-1,0));
    if  abs(lhs-rhs) > epsilon
        flag_Euro = 0;
    end
    if flag_Euro
        disp('pass: getEuropean')
    else
        disp('fail: getEuropean')
    end
    toc;
    
    
    % test smoothness of spline
    % plot of spline, we can test it visually
end



