"""
Contains functions that will identify OOC
points in a set of data
"""

def test_beyond_limits(data, center, lcl, ucl):
    """Checks for any point outside control limits"""
    return data[0] > ucl or data[0] < lcl

def test_violating_runs(data, center, lcl, ucl):
    """Test for all points above or below center"""

    for idx, curr in enumerate(data):
        if idx > 0:
            if (prev - center)*(curr - center) < 0:
                return False
        prev = curr
        
    return True

def test_beyond_onesigma(data, center, lcl, ucl):
    """Test for data - 1 points above or below 1 sigma"""

    count_above = 0
    count_below = 0
    
    upper = center + (ucl - lcl) / 6
    lower = center - (ucl - lcl) / 6
    
    for idx, curr in enumerate(data):
        if curr > upper:
            count_above += 1
        if curr < lower:
            count_below += 1
   
    if count_above >= idx or count_below >= idx:
        return True
        
    return False
    
def test_beyond_twosigma(data, center, lcl, ucl):
    """Test for data - 1 points above or below 2 sigma"""

    count_above = 0
    count_below = 0
    
    upper = center + (ucl - lcl) / 3
    lower = center - (ucl - lcl) / 3
    
    for idx, curr in enumerate(data):
        if curr > upper:
            count_above += 1
        if curr < lower:
            count_below += 1
   
    if count_above >= idx or count_below >= idx:
        return True
        
    return False
    
def test_trending_runs(data, center, lcl, ucl):
    """Test for point trending up or down"""
    
    up = True
    down = True

    #ToDo: Change to enumerate
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
