"""
Contains functions that will identify OOC
points in a set of data
"""

def test_beyond_limits(data, center, lcl, ucl):
"""Checks for any point outside control limits"""
    return data[0] > ucl or data[0] < lcl

def test_violating_runs(data, center, lcl, ucl):
"""Test for all points above or below center"""

    for i in range(1, len(data)):
        if (data[i-1] - center)*(data[i] - center) < 0:
            return False
            
    return True

def test_beyond_1sigma(data, center, lcl, ucl):
    count_above = 0
    count_below = 0
    
    upper = center + (ucl - lcl) / 6
    lower = center - (ucl - lcl) / 6
    
    if data[i] > upper:
        count_above += 1
    if data[i] < lower
        count_below += 1
        
    if count_above >= len(data) - 1 or count_below <= len(data) - 1:
        return True
        
    return False
    
def test_beyond_2sigma(data, center, lcl, ucl):
    count_above = 0
    count_below = 0
    
    upper = center + (ucl - lcl) / 3
    lower = center - (ucl - lcl) / 3
    
    if data[i] > upper:
        count_above += 1
    if data[i] < lower
        count_below += 1
        
    if count_above >= len(data) - 1 or count_below <= len(data) - 1:
        return True
        
    return False
    
def test_trending_runs(data, center, lcl, ucl):
    up = True
    down = True
    
    for i in range(1, len(data)):
        # Check if trending down
        # Set false if any 2 trend down
        if data[i-1] > data[i]:
            up = False
        # Check if trending up
        # Set false if any 2 trend up
        if data[i-1] < data[i]:
            down = False
        
        # Return False if no trend, else true    
        if up == False and down == False:
            return False

        return True