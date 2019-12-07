import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

goog = web.DataReader('GOOG', data_source='yahoo', start='8/14/2007', end='8/14/2019')
# type(goog) is pandas.core.frame.DataFrame

# print(goog.tail())
goog['Log_Ret'] = np.log(goog['Close'] / goog['Close'].shift(1))
vola = np.sqrt( np.sum(np.square(goog['Log_Ret']))/(len(goog['Log_Ret'])-1)*252 )
print('Volatility = '+str(vola))

goog['Volatility'] = pd.Series(goog['Log_Ret']).rolling\
    (window=252,center=False).std() * np.sqrt(252)
goog[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8, 6))
plt.show()
