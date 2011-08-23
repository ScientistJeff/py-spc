

def test_beyond_limits(data, center, lcl, ucl):
    return data[0] > ucl or data[0] < lcl

def test_violating_runs(data, center, lcl, ucl):
    for i in range(1, len(data)):
        if (data[i-1] - center)*(data[i] - center) < 0:
            return False
    return True