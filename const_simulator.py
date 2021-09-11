'''
Author: your name
Date: 2021-09-09 14:20:28
LastEditTime: 2021-09-10 14:20:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Code/const_simulator.py
'''
import os
import ephem
import datetime
import math


def cycleCompute(height):
    r = 6371000 + height
    G = 6.67428e-11
    M = 5.965e+24
    res = 4*math.pi*math.pi*r*r*r/G
    res = res/M
    res = math.sqrt(res)
    rot = 24*60*60  # ((23*60)+56)*60+4
    motion = rot/res  # 所谓速度，是地球自转周期是卫星周期的多少倍
    # return res,motion
    return motion


'''
class EarthSatellite(__ephem.Body):
    """
    A satellite in orbit around the Earth, usually built by passing the text of a TLE entry to the `ephem.readtle()` routine. You can read and write its orbital parameters through the following attributes:
    
    _ap -- argument of perigee at epoch (degrees) 近地点的论据
    _decay -- orbit decay rate (revolutions per day-squared)
    _drag -- object drag coefficient (per earth radius)
    _e -- eccentricity 离心率
    _epoch -- reference epoch (mjd)
    _inc -- inclination (degrees)
    _M -- mean anomaly (degrees from perigee at epoch)
    _n -- mean motion (revolutions per day)
    _orbit -- integer orbit number of epoch
    _raan -- right ascension of ascending node (degrees)
    """
'''
os.system("rm starlink/*")
NUM_ORBITS = 72
NUM_SATS_PER_ORBIT = 22
INCLINATION = 53
ECCENTRICITY = 0.000001  # 离心率
ARG_OF_PERIGEE = 0.0  # 近地点
HEIGHT = 540000
# 这个是按550km高度计算的，所谓速度，是地球自转周期是卫星周期的多少倍 TLE给的15.19
MEAN_MOTION = cycleCompute(HEIGHT)
floder = 'starlink'
one_day = 60*24*60
snap = 1
cnt = 0  # 卫星编号
now = datetime.datetime.now()
# 预测60*24分钟，时间片3分钟
F = 18
for cur_min in range(0, one_day, snap):
    cur_time = (now + datetime.timedelta(minutes=cur_min)
                ).strftime("%Y-%m-%d %H:%M:%S")
    cnt = 0
    file = floder + '/%d.txt' % cur_min  # 输出的文件
    with open(file, 'w') as f:
        for cur_orbit in range(NUM_ORBITS):
            raan = cur_orbit * 360 / NUM_ORBITS  # 轨道参数
            for cur_sat in range(NUM_SATS_PER_ORBIT):
                meanAnomaly = (cur_sat * 360 / NUM_SATS_PER_ORBIT + 360 * F / (NUM_SATS_PER_ORBIT * NUM_ORBITS) * (
                    cur_orbit - 1)) % 360  # 轨道内的卫星参数
                sat = ephem.EarthSatellite()
                sat._epoch = now
                sat._inc = INCLINATION
                sat._raan = raan
                sat._M = meanAnomaly
                sat._n = MEAN_MOTION
                sat._e = ECCENTRICITY  # 偏心率
                sat._ap = ARG_OF_PERIGEE  # 圆
                sat.compute(cur_time)
                f.writelines('%d,%d,%d,%s,%s,%s\n' % (
                    cnt, cur_orbit, cur_sat, math.degrees(sat.sublat), math.degrees(sat.sublong), sat.elevation / 1000))
                cnt += 1
    print('done in %d minutes' % (cur_min + snap))
