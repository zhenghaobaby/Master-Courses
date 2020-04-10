# Author : zhenghaobaby
# Time : 2020/2/22 10:14
# File : try.py
# Ide : PyCharm




a = "20200306"

b = "20200327"

import datetime

a = datetime.datetime.strptime(a,"%Y%m%d")
b = datetime.datetime.strptime(b,"%Y%m%d")

m = b-a

print(m.days)