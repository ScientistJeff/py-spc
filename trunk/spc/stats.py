'''
Created on Aug 23, 2011

@author: cgiacofe
'''

import numpy

# n         2      3      4      5      6      7      8      9      10
A2 = [0,0, 1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308]
D3 = [0,0, 0,     0,     0,     0,     0,     0.076, 0.136, 0.184, 0.223]
D4 = [0,0, 3.267, 2.575, 2.282, 2.115, 2.004, 1.924, 1.864, 1.816, 1.777]
# n   0 1      2      3      4      5      6      7      8      9     10     11     12     13     14     15       20     25
c4 = [0,0,0.7979,0.8862,0.9213,0.9400,0.9515,0.9594,0.9650,0.9693,0.9727,0.9754,0.9776,0.9794,0.9810,0.9823]#,0.9869,0.9896]
B3 = [0,0,     0,     0,     0,     0, 0.030, 0.118, 0.185, 0.239, 0.284, 0.321, 0.354, 0.382, 0.406, 0.428]#, 0.510, 0.565]
B4 = [0,0, 3.267, 2.568, 2.266, 2.089, 1.970, 1.882, 1.815, 1.761, 1.716, 1.679, 1.646, 1.618, 1.594, 1.572]#, 1.490, 1.435]
B5 = [0,0,     0,     0,     0,     0, 0.029, 0.113, 0.179, 0.232, 0.276, 0.313, 0.346, 0.374, 0.399, 0.421]#, 0.504, 0.559]
B6 = [0,0, 2.606, 2.276, 2.088, 1.964, 1.874, 1.806, 1.751, 1.707, 1.669, 1.637, 1.610, 1.585, 1.563, 1.544]#, 1.470, 1.420]
A3 = [0,0, 2.659, 1.954, 1.628, 1.427, 1.287, 1.182, 1.099, 1.032, 0.975, 0.927, 0.886, 0.850, 0.817, 0.789]#, 0.680, 0.606]

def get_stats_x_mr_x(data, size):
    assert size == 1
    center = numpy.mean(data)
    sd = 0
    for i in range(len(data)-1):
        sd += abs(data[i] - data[i+1])
    sd /= len(data) - 1
    d2 = 1.128
    lcl = center - 3*sd/d2
    ucl = center + 3*sd/d2
    return center, lcl, ucl

def get_stats_x_mr_mr(data, size):
    assert size == 1
    sd = 0
    for i in range(len(data)-1):
        sd += abs(data[i] - data[i+1])
    sd /= len(data) - 1
    d2 = 1.128
    center = sd
    lcl = 0
    ucl = center + 3*sd/d2
    return center, lcl, ucl

def get_stats_x_bar_r_x(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Rsum = 0
    for xset in data:
        assert len(xset) == n
        Rsum += max(xset) - min(xset)
    Rbar = Rsum / len(data)

    Xbar = numpy.mean(data)

    center = Xbar
    lcl = center - A2[n]*Rbar
    ucl = center + A2[n]*Rbar
    return center, lcl, ucl

def get_stats_x_bar_r_r(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Rsum = 0
    for xset in data:
        assert len(xset) == n
        Rsum += max(xset) - min(xset)
    Rbar = Rsum / len(data)

    center = Rbar
    lcl = D3[n]*Rbar
    ucl = D4[n]*Rbar
    return center, lcl, ucl

def get_stats_x_bar_s_x(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Sbar = numpy.mean(numpy.std(data, 1, ddof=1))
    Xbar = numpy.mean(data)

    center = Xbar
    lcl = center - A3[n]*Sbar
    ucl = center + A3[n]*Sbar
    return center, lcl, ucl
    
def get_stats_x_bar_s_s(data, size):
    n = size
    assert n >= 2
    assert n <= 10

    Sbar = numpy.mean(numpy.std(data, 1, ddof=1))

    center = Sbar
    lcl = B3[n]*Sbar
    ucl = B4[n]*Sbar
    return center, lcl, ucl

def get_stats_p(data, size):
    n = size
    assert n > 1

    pbar = float(sum(data)) / (n * len(data))
    sd = numpy.sqrt(pbar*(1-pbar)/n)

    center = pbar
    lcl = center - 3*sd
    if lcl < 0:
        lcl = 0
    ucl = center + 3*sd
    if ucl > 1:
        ucl = 1.0
    return center, lcl, ucl

def get_stats_np(data, size):
    n = size
    assert n > 1

    pbar = float(sum(data)) / (n * len(data))
    sd = numpy.sqrt(n*pbar*(1-pbar))

    center = n*pbar
    lcl = center - 3*sd
    if lcl < 0:
        lcl = 0
    ucl = center + 3*sd
    if ucl > n:
        ucl = n
    return center, lcl, ucl

def get_stats_c(data, size):
    cbar = numpy.mean(data)

    center = cbar
    lcl = center - 3*numpy.sqrt(cbar)
    if lcl < 0:
        lcl = 0
    ucl = center + 3*numpy.sqrt(cbar)
    return center, lcl, ucl

def get_stats_u(data, size):
    n = size
    assert n > 1

    cbar = float(sum(data))/(len(data)*n)

    center = cbar
    lcl = center - 3*numpy.sqrt(cbar/n)
    if lcl < 0:
        lcl = 0
    ucl = center + 3*numpy.sqrt(cbar/n)
    return center, lcl, ucl

if __name__ == '__main__':
    pass