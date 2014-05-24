import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, MonthLocator, DateFormatter
import datetime
import numpy as np
import pylab as pl
import scipy
from scipy import stats
import csv
from scipy.optimize import curve_fit
##### Begin font settings
#mpl.use("pgf")
pgf_with_rc_fonts = {
    ##'family': 'serif',
    ##'serif': ['cmr10'],
    "font.family": "serif",
    "font.serif": ["cmr10"], # use latex default serif font
    #"font.sans-serif": ["cmr10"], # use latex for sans too :)
    "text.usetex": True # requires LaTeX, I think
}
mpl.rcParams.update(pgf_with_rc_fonts)
##### End font settings

def turn_on_grid_lines():
    # I'm not entirely sure how this function works, other than that it
    # produces gray dashed lines in the background.  The name "ax" as
    # used here may also conflict with another plot that the user is
    # using, which should be fixed.
    ax = plt.subplot(111)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.set_axisbelow(True)
    ax2 = plt.subplot(111)
    ax2.xaxis.grid(color='gray', linestyle='dashed')
    ax2.set_axisbelow(True)

def DictReader(fname):
    with open(fname, 'rt') as f:
        # Read in csv file
        reader = csv.reader(f, delimiter=" ", skipinitialspace=True)
        # The `skipinitialspace` is so that extra whitespace is ignored
        # (like in gnuplot).  For what follows, see
        # http://stackoverflow.com/a/7958192/3422337 and
        # http://riceissa.github.io/math/python_zip.html
        keys = next(reader)
        data = [row for row in reader]
        columns = map(list, zip(*data))
        return dict(zip(keys,columns))

ret = DictReader("push_up_data.csv")

day_array = np.array([datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in ret['day']])
push_ups_array = np.array([float(i) for i in ret['push_ups']])
push_ups_array = np.cumsum(push_ups_array)
print(day_array)
print(push_ups_array)
########## BEGIN PLOT
myDays = DayLocator(interval=5)
myMonths = MonthLocator()
myFmt = DateFormatter('%d')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(myDays)
ax.xaxis.set_major_formatter(myFmt)
#ax.autoscale_view()
plt.scatter(day_array, push_ups_array, label="push-up dots", c='r', marker='p')


def graph_piecewise():
    for i in range(len(day_delims)-1):
        piecewise(day_delims[i], day_delims[i+1], endval, gradient_vals[i])

grad = DictReader("gradient_changes.csv")
day_delims = np.array([datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in grad['alt_day']])
gradient_vals = np.array(grad['gradient_val'])
#day_array = np.array([datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in ret['day']])
date_today = datetime.date.today()
day_delims = np.append(day_delims, [date_today])

endval = 0
def piecewise(left_bound, right_bound, start, gradient):
    global endval
    day_diff = (right_bound - left_bound).days
    x = np.array([left_bound + datetime.timedelta(days=i) for i in xrange(day_diff + 1)])
    #x = np.arange(bound_min(period_inv2_array, uncert_period_inv2_array), bound_max(period_inv2_array, uncert_period_inv2_array), 0.005)
    #plt.plot(x, np.add(np.multiply(gradient, np.subtract(x, left_bound)), start), 'b-', label="$f(x) = {start} + {gradient}(x-{left_bound}), {left_bound} \leq x \leq {right_bound}$".format(start=start,gradient=gradient,left_bound=left_bound,right_bound=right_bound))
    plt.plot(x, np.array([start + float(gradient) * float((d - left_bound).days) for d in x]))
    #endval = np.add(np.multiply(gradient, np.subtract(right_bound, left_bound)), start)
    endval = (float(gradient) * float(day_diff)) + float(start)
    #endval = np.multiply(gradient, day_diff)
    #print "EV: " + str(float(gradient) * float(day_diff))
    print "EV: " + str(endval)

graph_piecewise()

pl.xlabel(r'Day')
pl.ylabel('Number of push-ups (cumulative)')
pl.title(r"Push-ups vs days")
pl.legend(loc='lower right', prop={'size':10})
turn_on_grid_lines()

#pl.show()
pl.savefig("sample.pdf", format="pdf")
pl.clf() # clear the canvas
########## END PLOT
