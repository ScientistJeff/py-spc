"""
@Date      Created on Aug 23, 2011
@brief     
SPC Statistical Process Control provides means to monitor process behavior
using statistical tools defined by Shewhart and others. The process run is shown
as Quality Control Charts (QCC).
@author    Chris Giacofei
@copyright GNU GPL v3 - http://www.gnu.org/licenses/gpl.html

"""

import oocrules
import stats
import data

try:
    import pylab
    from matplotlib import pyplot
    mpl_present = True
except ImportError:
    mpl_present = False

# Chart type names for dictionary function call
CHART_X_BAR_R_X = "Xbar R - X"
CHART_X_BAR_R_R = "Xbar R - R"
CHART_X_BAR_S_X = "Xbar S - X"
CHART_X_BAR_S_S = "Xbar S - S"
CHART_X_MR_X = "X mR - X"
CHART_X_MR_MR = "X mR - mR"
CHART_P = "p"
CHART_NP = "np"
CHART_C = "c"
CHART_U = "u"
CHART_EWMA = "EWMA"
CHART_CUSUM = "CUSUM"
CHART_THREE_WAY = "three way"
CHART_TIME_SERIES = "time series"

# Rule names for dictionary function call
RULES_1_BEYOND_3SIGMA = "1 beyond 3*sigma"
RULES_2_OF_3_BEYOND_2SIGMA = "2 of 3 beyond 2*sigma"
RULES_4_OF_5_BEYOND_1SIGMA = "4 of 5 beyond 1*sigma"
RULES_7_ON_ONE_SIDE = "7 on one side"
RULES_8_ON_ONE_SIDE = "8 on one side"
RULES_9_ON_ONE_SIDE = "9 on one side"
RULES_6_TRENDING = "6 trending"
RULES_14_UP_DOWN = "14 up down"
RULES_15_BELOW_1SIGMA = "15 below 1*sigma"
RULES_8_BEYOND_1SIGMA_BOTH_SIDES = "8 beyond 1*sigma on both sides"


RULES_BASIC = [RULES_1_BEYOND_3SIGMA, 
               RULES_7_ON_ONE_SIDE]

# Western Electric Rules http://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm
RULES_WECO = [RULES_1_BEYOND_3SIGMA,
              RULES_2_OF_3_BEYOND_2SIGMA, 
              RULES_4_OF_5_BEYOND_1SIGMA, 
              RULES_8_ON_ONE_SIDE,
              RULES_6_TRENDING, 
              RULES_14_UP_DOWN]

# Nelson Rules http://en.wikipedia.org/wiki/Nelson_rules
RULES_NELSON = [RULES_1_BEYOND_3SIGMA,
                RULES_9_ON_ONE_SIDE,
                RULES_6_TRENDING,
                RULES_14_UP_DOWN,
                RULES_2_OF_3_BEYOND_2SIGMA,
                RULES_4_OF_5_BEYOND_1SIGMA,
                RULES_15_BELOW_1SIGMA,
                RULES_8_BEYOND_1SIGMA_BOTH_SIDES]

# All Rules
RULES_ALL = [RULES_1_BEYOND_3SIGMA,
             RULES_2_OF_3_BEYOND_2SIGMA,
             RULES_4_OF_5_BEYOND_1SIGMA,
             RULES_7_ON_ONE_SIDE,
             RULES_8_ON_ONE_SIDE,
             RULES_6_TRENDING,
             RULES_14_UP_DOWN,
             RULES_15_BELOW_1SIGMA,
             RULES_8_BEYOND_1SIGMA_BOTH_SIDES]

STATS_FUNCS = {
    CHART_X_BAR_R_X: (stats.get_stats_x_bar_r_x, data.prepare_data_x_bar_rs_x),
    CHART_X_BAR_R_R: (stats.get_stats_x_bar_r_r, data.prepare_data_x_bar_r_r),
    CHART_X_BAR_S_X: (stats.get_stats_x_bar_s_x, data.prepare_data_x_bar_rs_x),
    CHART_X_BAR_S_S: (stats.get_stats_x_bar_s_s, data.prepare_data_x_bar_s_s),
    CHART_X_MR_X: (stats.get_stats_x_mr_x, data.prepare_data_none),
    CHART_X_MR_MR: (stats.get_stats_x_mr_mr, data.prepare_data_x_mr),
    CHART_P: (stats.get_stats_p, data.prepare_data_p),
    CHART_NP: (stats.get_stats_np, data.prepare_data_none),
    CHART_C: (stats.get_stats_c, data.prepare_data_none),
    CHART_U: (stats.get_stats_u, data.prepare_data_u),
    CHART_EWMA: (None, data.prepare_data_none),
    CHART_CUSUM: (None, data.prepare_data_none),
    CHART_THREE_WAY: (None, data.prepare_data_none),
    CHART_TIME_SERIES: (None, data.prepare_data_none)}

RULES_FUNCS = {
    RULES_1_BEYOND_3SIGMA: (oocrules.test_beyond_limits, 1),
    RULES_2_OF_3_BEYOND_2SIGMA: (None, 3),
    RULES_4_OF_5_BEYOND_1SIGMA: (None, 5),
    RULES_7_ON_ONE_SIDE: (oocrules.test_violating_runs, 7),
    RULES_8_ON_ONE_SIDE: (oocrules.test_violating_runs, 8),
    RULES_9_ON_ONE_SIDE: (oocrules.test_violating_runs, 9),
    RULES_6_TRENDING: (None, 6),
    RULES_14_UP_DOWN: (None, 14),
    RULES_15_BELOW_1SIGMA: (None, 15),
    RULES_8_BEYOND_1SIGMA_BOTH_SIDES: (None, 8)}

class Spc(object):
    """
    Main class that provides SPC analysis. It detects SPC rules violations.
    It can draw charts using matplotlib.

    :arguments:
      data
       user data as flat array

    **Usage**

    >>> s = Spc([1, 2, 3, 3, 2, 1, 3, 8], CHART_X_MR_X)
    >>> s.get_stats()
    (2.875, 1, 0.21542553191489322, 5.5345744680851068)
    >>> s.get_violating_points()
    {'1 beyond 3*sigma': [7]}
    """

    def __init__(self, data, chart_type, rules=RULES_BASIC, newdata=[], sizes=None):
        self.orig_data = data
        self.chart_type = chart_type
        self.rules = rules
        self.stats = []

        sf, pd = STATS_FUNCS[chart_type]
        if sizes == None:
            if isinstance(data[0], (list, tuple)):
                size = len(data[0])
            else:
                size = 1
        else:
            size = sizes
        self.center, self.lcl, self.ucl = sf(data, size)
        self._data = pd(data, size)

        self.violating_points = self._find_violating_points()

    def _find_violating_points(self, rules=[]):
        if len(rules) > 0:
            rs = rules
        else:
            rs = self.rules
        points = {}
        
        for i in range(len(self._data)):
            for r in rs: # For each rule evaluate data
                func, points_num = RULES_FUNCS[r] # Set the rule and num point in run
                if func == None or i <= points_num - 1:
                    continue
                if func(self._data[i-points_num+1:i+1], self.center, self.lcl, self.ucl):
                    points.setdefault(r, []).append(i)
        return points

    def get_chart(self, ax=None):
        """Generate chart using matplotlib."""
        if not mpl_present:
            raise Exception("matplotlib not installed")
        if ax == None:
            ax = pylab
        ax.plot(self._data, "bo-")
        ax.plot([0, len(self._data)], [self.center, self.center], "k-")
        ax.plot([0, len(self._data)], [self.lcl, self.lcl], "k:")
        ax.plot([0, len(self._data)], [self.ucl, self.ucl], "k:")

        if self.violating_points.has_key(RULES_7_ON_ONE_SIDE):
            for i in self.violating_points[RULES_7_ON_ONE_SIDE]:
                ax.plot([i], [self._data[i]], "yo")
        if self.violating_points.has_key(RULES_1_BEYOND_3SIGMA):
            for i in self.violating_points[RULES_1_BEYOND_3SIGMA]:
                ax.plot([i], [self._data[i]], "ro")
        pylab.figtext(0.05, 0.04, "Center = %0.3f" % self.center)
#        pylab.figtext(0.05, 0.01, "StdDev = %0.3f" % self.sd)
        pylab.figtext(0.3, 0.04, "LCL = %0.3f" % self.lcl)
        pylab.figtext(0.3, 0.01, "UCL = %0.3f" % self.ucl)
        #pylab.show()

    def get_violating_points(self, rules=[]):
        """Return points that violates rules of control chart"""
        return self.violating_points

    def get_stats(self):
        """Return basic statistics about data as tuple: (center, LCL, UCL)."""
        return self.center, self.lcl, self.ucl
