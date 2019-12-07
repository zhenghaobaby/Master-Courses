# Black-Scholes-Merton Implied Volatilities of
# Call Options on the DAX
# Quotes from 29 Apr 2011
# Source: www.eurexchange.com
# DAX_imp_vol.py
#
# (c) Dr. Yves J. Hilpisch
# Derivatives Analytics with Python
#

# code obtained from
# https://github.com/yhilpisch/dawp
# under the folder book/03_stf/

from bsm_functions import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#
# Option Data
#
S0 = 7514.46  # initial index level 29 Apr 2011
T = np.array([21., 49., 140., 231., 322.]) / 365.  # call option maturities
r = [0.0124, 0.0132, 0.015, 0.019, 0.0214]  # approx. short rates

# May 2011
K = np.array([7000, 7050, 7100, 7150, 7200, 7250, 7300, 7350, 7400, 7450,
         7500, 7550, 7600, 7650, 7700, 7750, 7800, 7850, 7900, 7950, 8000])
C1 = np.array([530.8, 482.9, 435.2, 388.5, 342.5, 297.8, 254.8, 213.7, 175.4,
          140.2, 108.7, 81.6, 59, 41.2, 27.9, 18.5, 12.1, 7.9, 5.1, 3.4, 2.3])

# June 2011
C2 = np.array([568.9, 524.5, 481.1, 438.7, 397.3, 357.5, 318.9, 281.9, 247, 214,
          183.3, 155.1, 129.3, 106.3, 86.1, 68.8, 54.1, 42, 32.2, 24.5, 18.4])

# Sep 2011
C3 = np.array([697.1, 657.9, 619.5, 581.8, 544.9, 509.1, 474.2, 440, 407.2, 375.4,
          344.8, 315.3, 287.5, 260.6, 235.5, 211.5, 189, 168, 148.8, 130.7,
          114.2])

# Dec 2011
C4 = np.array([811.5, 774.4, 737.9, 702.1, 666.9, 632.3, 598.5, 565.6, 533.5,
          502.1, 471.6, 442.1, 413.2, 385.6, 359, 333.2, 308.4, 284.9, 262.4,
          240.9, 220.4])

# Mar 2012
C5 = np.array([921.3, 885.4, 849.8, 814.7, 780.1, 746.6, 713.4, 680.8, 648.9,
          617.7, 587.1, 557.4, 528.6, 500.2, 472.6, 446, 419.9, 395, 370.4,
          347.1, 324.6])

#
# BSM Implied Volatilities
#
imv1 = np.zeros(len(K));
imv2 = np.zeros(len(K));
imv3 = np.zeros(len(K));
imv4 = np.zeros(len(K));
imv5 = np.zeros(len(K));
for j in range(len(K)):
    imv1[j] = bsm_call_imp_vol(S0, K[j], T[0], r[0], C1[j], 0.2)
    imv2[j] = bsm_call_imp_vol(S0, K[j], T[1], r[1], C2[j], 0.2)
    imv3[j] = bsm_call_imp_vol(S0, K[j], T[2], r[2], C3[j], 0.2)
    imv4[j] = bsm_call_imp_vol(S0, K[j], T[3], r[3], C4[j], 0.2)
    imv5[j] = bsm_call_imp_vol(S0, K[j], T[4], r[4], C5[j], 0.2)

imv = np.stack((imv1, imv2, imv3, imv4, imv5))

#
# Graphical Output
#
## 1st Output
plt.figure(0)
plt.plot(K, imv1 * 100, 'ro')
plt.plot(K, imv2 * 100, 'gx')
plt.plot(K, imv3 * 100, 'bv')
plt.plot(K, imv4 * 100, 'yD')
plt.plot(K, imv5 * 100, 'mh')
plt.grid(True)
plt.xlabel('Strike')
plt.ylabel('Implied Volatility')
plt.show()

## 2nd Output
k, t = np.meshgrid(K, T)
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(k, t, imv)
ax.set_xlabel('K')
ax.set_ylabel('T')
ax.set_zlabel('Implied Volatility')
plt.show()
