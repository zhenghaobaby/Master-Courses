# Author : zhenghao
# Time : 2020/3/15 14:22
# File : call price.py
# Ide : PyCharm

import pandas as pd
import numpy as np
import datetime
import math
import scipy.stats as si
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def BS(S,K,r,T,sigma):

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))

    return call


def solve_implied_vol(row):
    """
    call option
      c = SN(d1) - Ke-rT*N(d2)
      d2 = d1-sigma*sqrt(T-t)
      vega = S*sqrt(T-t)*density_fuc(d1)

    Newton-Raphson formula
       sigma_(i+1)  = sigma_i - (BS(sigma_i) - price)/vega(sigma_i)

       initial_value = sqrt((2*pi)/(T-t))*(P/S)
    """

    p = row['price']
    T = row['days to maturity']
    s = row['spot']
    r = row['risk_free']
    K = row['strike']


    sigma_0 = np.sqrt(math.pi*2/T)*p/s  ##initial value
    p_1 = BS(S=s, K=K, r=r, T=T, sigma=sigma_0)

    while abs(p_1-p)>0.1:
        d1 = (np.log(s / K) + (r + 0.5 * sigma_0 ** 2) * T) / (sigma_0 * np.sqrt(T))
        vega = s*np.sqrt(T)*np.exp(-0.5*d1**2)/np.sqrt(2*math.pi)
        if vega==0:
            break
        sigma_0 = sigma_0-0.1*(p_1-p)/vega   ## update sigma
        p_1 = BS(S=s, K=K, r=r, T=T, sigma=sigma_0)

    return sigma_0


def optimize_t(data, T):
    """
    model parametric
    sigma(t,T) = a+b*exp(-r(T-t))
    """

    def func(x, v1, v2, alpha):
        return np.sqrt(v1**2+2*v1*v2*((1-np.exp(-alpha*(T-x)))/alpha)+v2**2*(1-np.exp(-2*alpha*(T-x)))/(2*alpha*(T-x)))

    x = np.array(data['t'].tolist())
    y = np.array(data['implied vol'].tolist())
    popt, pcov = curve_fit(func, x, y)

    v1 = popt[0]
    v2 = popt[1]
    alpha = popt[2]

    yvals = func(x, v1, v2, alpha)
    plt.plot(x, y, '*', label='original implied vol')
    plt.plot(x, yvals, 'r', label='fit implied vol')
    plt.xlabel('t')
    plt.ylabel('implied vol')
    plt.legend(loc="best",fontsize=16)
    plt.title('curve_fit')
    plt.show()

    return (v1, v2, alpha)



def comparation(data):

    """we compare BS and Monte carlo method"""
    def calculate_BS(row):
        s = row['spot']
        T = row['T']-row['t']
        r = 0
        K = row['strike']
        sigma = row['fit vol']
        return BS(S=s, K=K, r=r, T=T, sigma=sigma)

    data['theory price'] = data.apply(lambda x:calculate_BS(x),axis=1)

    def Monte_carlo(row):
        T = row['T']
        tau = row['t']
        s = row['spot']
        r = 1.58/100
        K = row['strike']
        sigma = row['fit vol']

        value = []
        runtime = 1000
        for i in range(runtime):
            mean = (-0.5*sigma**2)*(T-tau)
            dw = np.sqrt(T-tau) * np.random.randn()
            F= s*np.exp(mean+sigma*dw)
            value.append(np.exp(-r*T)*max(F-K,0))
        value = np.array(value)
        return np.mean(value)

    data['Simulate price'] = data.apply(lambda x:Monte_carlo(x),axis=1)

    plt.plot(data['date'], data['price'], label="market_price")
    plt.plot(data['date'], data['theory price'], label="BS price")
    plt.plot(data['date'], data['Simulate price'],label = "Monte carlo price")
    plt.legend(loc="best",fontsize=16)
    plt.xlabel("t")
    plt.ylabel("call option price")
    plt.show()
    return data


def data_processing(data1):
    data1['date'] = data1['date'].apply(lambda x: datetime.datetime.strptime(str(x), "%d/%m/%Y"))
    data1.sort_values(by=['date'],inplace=True)
    data1.index = np.arange(len(data1))
    data1['T'] = [T] * len(data1)
    data1['strike'] = [strike] * len(data1)
    data1['risk_free'] = [risk_free] * len(data1)
    data1['t'] = data1['date'].apply(lambda x: (x - datetime.datetime.strptime(start_date_1, "%Y-%m-%d")).days / 365.0)
    data1['days to maturity'] = data1['T'] - data1['t']
    data1['return'] = data1['spot'].apply(lambda x: np.log(x)).diff(1)

    return data1

if __name__ == '__main__':
    """
    implied vol mode :
    0: using historical realized vol(standard deviation of 10 days)
    1: using option price (Newton-Raphson formula)
    """

    implied_vol_mode = 1
    risk_free = 0  ##our underlying is future, there is no drift term
    strike = 50

    expire_date = "2020-03-26"
    start_date_1 = "2018-01-02"
    T = (datetime.datetime.strptime(expire_date,"%Y-%m-%d")-datetime.datetime.strptime(start_date_1,"%Y-%m-%d")).days/365.0


    data1 = pd.read_csv("data1.csv")
    data1 = data_processing(data1)

    if implied_vol_mode==0:
        """use historical variance  """
        data1['implied vol'] = data1['return'].rolling(10).std()
        data1['implied vol'] = data1['implied vol'].apply(lambda x:np.sqrt(x))
        data1.dropna(inplace=True)
    else:
        """use option price to derive implied vol"""
        data1['implied vol'] = data1.apply(lambda x:solve_implied_vol(x),axis=1)


    """for some days the option is deep in the money, we can't solve the implied vol"""
    data1_train = data1[(data1['implied vol']>=0)&(data1['implied vol']<1)]
    parameter_ = optimize_t(data1_train,T=T)

    """Integral from t-T"""
    def func(x, v1, v2, alpha):
        return np.sqrt(v1**2+2*v1*v2*((1-np.exp(-alpha*(T-x)))/alpha)+v2**2*(1-np.exp(-2*alpha*(T-x)))/(2*alpha*(T-x)))

    """get the fitted implied vol"""
    data1['fit vol'] = data1['t'].apply(lambda x:func(x,parameter_[0],parameter_[1],parameter_[2]))
    data1['strike'] = [strike]*len(data1)
    data1 = comparation(data1)

    data1.to_csv("Furtue_vol_for_implied_vol.csv")







