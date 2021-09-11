import numpy as np
import json
from scipy.io import loadmat
import math
import random

sat_per_orbit = 22
num_orbit = 72


def readMat(filename):
    m = loadmat(filename)
    return m


def readJson(filename):
    f = open(filename)
    m = json.load(f)
    f.close()
    return m


def No2Orbit(no):
    # "input satellite number, return orbit number and number in orbit"
    return no // sat_per_orbit, no % sat_per_orbit


def cir_to_car(lat, lng, h):
    radius = 6371000
    """theta = np.pi / 2 - lat * np.pi / 180
    phi = 2 * np.pi + lng * np.pi / 180
    x = (radius+h) * np.sin(theta) * np.cos(phi)
    y = (radius+h) * np.sin(theta) * np.sin(phi)
    z = (radius+h) * np.cos(theta)
    return x,y,z"""
    return np.array([(radius+h)*math.cos(math.radians(lat))*math.cos(math.radians(lng)),
                     (radius+h)*math.cos(math.radians(lat)) *
                     math.sin(math.radians(lng)),
                     (radius+h)*math.sin(math.radians(lat))])


def calDist(loc1, loc2):
    return np.linalg.norm(loc1 - loc2)


def loadPos2np(satfile, gsfile, usr_loc):
    '''
    load both satellite and gs postion info into np array
    satfile and gsfile are filenames of satellites' and gses' postion
    return No_sat, No_gs, position_np_array 
    '''
    #########################################
    # this part should be modified since the format of the file could be different
    sats_pos = readMat(satfile)['position']
    gses_pos = readJson(gsfile)['cities']

    No_sat = len(sats_pos)
    No_gs = len(gses_pos)
    No_slot = len(sats_pos[0][0][0])
    all_pos = []
    for i in range(No_sat):
        sat_pos = []
        sat_lats = sats_pos[i][0][0]
        sat_lons = sats_pos[i][0][1]
        sat_alts = sats_pos[i][0][2]
        sat_pos.append(sat_lats)
        sat_pos.append(sat_lons)
        sat_pos.append(sat_alts)
        all_pos.append(sat_pos)

    for i in range(No_gs):
        gs_pos = []
        gs_lats = [float(gses_pos[i]['lat'])] * No_slot
        gs_lons = [float(gses_pos[i]['lon'])] * No_slot
        gs_alts = [float(gses_pos[i]['alt'])*1000] * No_slot
        gs_pos.append(gs_lats)
        gs_pos.append(gs_lons)
        gs_pos.append(gs_alts)
        all_pos.append(gs_pos)

    for i in range(len(usr_loc[0])):
        loc = []
        usr_lats = [usr_loc[0][i]] * No_slot
        usr_lons = [usr_loc[1][i]] * No_slot
        usr_alts = [usr_loc[2][i]] * No_slot
        loc.append(usr_lats)
        loc.append(usr_lons)
        loc.append(usr_alts)
        all_pos.append(loc)

    return No_sat, No_gs, all_pos
    #########################################


def getNeighbors(sat):
    [orbit_idx, in_orbit_idx] = No2Orbit(sat)
    neighbor_sat_1 = orbit_idx*sat_per_orbit+(in_orbit_idx+1) % sat_per_orbit
    neighbor_sat_2 = orbit_idx*sat_per_orbit+(in_orbit_idx-1) % sat_per_orbit
    neighbor_sat_3 = ((orbit_idx+1) % num_orbit)*sat_per_orbit+in_orbit_idx
    neighbor_sat_4 = ((orbit_idx-1) % num_orbit)*sat_per_orbit+in_orbit_idx
    neighbor_sat_list = [neighbor_sat_1,
                         neighbor_sat_2, neighbor_sat_3, neighbor_sat_4]
    return neighbor_sat_list


def generate_random_gps(base_log=None, base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    loga = '%.8f' % longitude
    lata = '%.8f' % latitude
    return float(loga), float(lata)
