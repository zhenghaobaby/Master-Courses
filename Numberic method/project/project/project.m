% This program provides the skeleton for the project
function project()
    tic;
    [spot, lag, days, domdfs, fordfs, vols, cps, deltas] = getMarket();

    tau = lag / 365; % spot rule lag

    % time to maturities in years
    Ts = days / 365;

    % construct market objects
    domCurve = makeDepoCurve(Ts, domdfs);
    forCurve = makeDepoCurve(Ts, fordfs);
    fwdCurve = makeFwdCurve(domCurve, forCurve, spot, tau);
    volSurface = makeVolSurface(fwdCurve, Ts, cps, deltas, vols);

    % compute a discount factor
    domRate = exp(-getRateIntegral(domCurve, 0.8))

    % compute a forward spot rate G_0(0.8)
    fwd = getFwdSpot(fwdCurve, 0.8)
    
    % build ans use a smile
    smile = makeSmile(fwdCurve, Ts(end), cps, deltas, vols(end,:));
    atmfvol = getSmileVol(smile, getFwdSpot(fwdCurve, Ts(end)));
%     ezplot(smile,[0:0.1:5]);

    % get some vol
    [vol, f] = getVol(volSurface, 0.8, [fwd, fwd])

    % get pdf
    pdf = getPdf(volSurface, 0.8, [fwd, fwd])
    m = getPdf(volSurface, 0.8, [1e-2, 1e-7])

    % get cdf cutoff points
    %cutoffs = getCdfCutoffs(volSurface, 0.8, [1e-2, 1e-7])

    % european
    u = getEuropean(volSurface, 0.8, @(x)max(x-fwd,0))
    
    % european
    u = getEuropean(volSurface, 0.8, @(x)max(x-fwd,0), [0,0.1,+Inf])
    toc;