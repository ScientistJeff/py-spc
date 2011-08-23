'''
Created on Aug 23, 2011

@author: cgiacofe
'''

import numpy

def prepare_data_none(data, size):
    return data

def prepare_data_x_bar_rs_x(data, size):
    data2 = []
    for xset in data:
        data2.append(numpy.mean(xset))
    return data2

def prepare_data_x_bar_r_r(data, size):
    data2 = []
    for xset in data:
        data2.append(max(xset) - min(xset))
    return data2

def prepare_data_x_bar_s_s(data, size):
    data2 = []
    for xset in data:
        data2.append(numpy.std(xset, ddof=1))
    return data2

def prepare_data_x_mr(data, size):
    data2 = [0]
    for i in range(len(data)-1):
        data2.append(abs(data[i] - data[i+1]))
    return data2

def prepare_data_p(data, size):
    data2 = [0]
    for d in data:
        data2.append(float(d)/size)
    return data2

def prepare_data_u(data, size):
    data2 = [0]
    for d in data:
        data2.append(float(d)/size)
    return data2

if __name__ == '__main__':
    pass