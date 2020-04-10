# # Author : zhenghaobaby
# # Time : 2020/3/27 10:16
# # File : codetest.py
# # Ide : PyCharm
#
#
#
# def BomberMan(n, grid, ):
#     r = len(grid)
#     c = len(grid[0])
#     time_grid = [[0]*c for _ in range(r)]
#     area_grid = [[0]*c for _ in range(r)]
#
#     for i in range(r):
#         for j in range(c):
#             if grid[i][j] == chr(79):
#                 time_grid[i][j] += 1
#
#
#     for t in range(2,n+1):
#         if t%2==0:  ## fill
#             for i in range(r):
#                 for j in range(c):
#                     if grid[i][j]==chr(79):
#                         time_grid[i][j]+=1
#                     else:
#                         grid[i][j] = chr(79)
#         else: ##donate
#             for i in range(r):
#                 for j in range(c):
#                     if grid[i][j]==chr(79):
#                         time_grid[i][j]+=1
#                         if time_grid[i][j]==3:
#                             area_grid[i][j]=1
#                             up = i-1 if i-1>=0 else False
#                             down = i+1 if i+1<r else False
#                             left = j-1 if j-1>=0 else False
#                             right = j+1 if j+1<c else False
#                             if up:
#                                 area_grid[up][j] = 1
#                             if down:
#                                 area_grid[down][j] = 1
#                             if left:
#                                 area_grid[i][left] = 1
#                             if right:
#                                 area_grid[i][right] = 1
#             for i in range(r):
#                 for j in range(c):
#                     if area_grid[i][j] ==1:
#                         time_grid[i][j]=0
#                         grid[i][j]="."
#             area_grid = [[0] * c for _ in range(r)]
#
#
#     return grid
#
#
#
# import numpy as np
#
#
# def InitRandomGrid(r, c):
#     # generate random numbers
#     rand = np.random.rand(r, c)
#
#     # construct grid
#     grid = np.empty((r, c), dtype=str)
#     grid[rand < 0.5] = '.'
#     grid[rand >= 0.5] = chr(79)
#
#     return grid.tolist()
#
#
# # grid input parameters
# r = 6
# c = 7
# n = 3
#
# grid = InitRandomGrid(r, c)
# results = BomberMan(n, grid)
# m=2


import datetime
import time
from typing import Callable


class TimeEvent:
    """
    Define callback event to be passed by callback function
    """

    def __init__(self, clockType: str, triggeredDatetime: datetime.datetime):
        """"""
        self.clockType = clockType
        self.triggeredDatetime = triggeredDatetime


# Defines callback function to be used in the clock.
HandlerType = Callable[[TimeEvent], None]


class Clock:

    def __init__(self):
        """"""
        pass

    def SubscribeAlarm(self, atDatetime: datetime.datetime, callback: HandlerType):
        now = datetime.datetime.now()
        time.sleep((atDatetime - now).total_seconds())  # sleep
        # ProcessClockEvent(TimeEvent("Alarm",atDatetime))
        callback(TimeEvent("Alarm",atDatetime))

    def SubscribeTimer(self, afterTimedelta: datetime.timedelta, callback: HandlerType):
        """
        Set an alarm after a certain period of time. Function callback will be called when the timer is triggered.
        """
        seconds = afterTimedelta.total_seconds()
        time.sleep(seconds)
        callback(TimeEvent('Timer', afterTimedelta))

# define callback function
def ProcessClockEvent(e: TimeEvent):
    print(f'Clock triggered: {e.clockType}, {e.triggeredDatetime}')

# create clock
myClock = Clock()

# set alarm
atDatetime = datetime.datetime.now() + datetime.timedelta(seconds=10)
myClock.SubscribeAlarm(atDatetime, ProcessClockEvent)

# set timer
afterTimedelta = datetime.timedelta(seconds=10)
myClock.SubscribeTimer(afterTimedelta, ProcessClockEvent)

# wait for alarm and timer to be triggered and ProcessClockEvent to be called by myClock