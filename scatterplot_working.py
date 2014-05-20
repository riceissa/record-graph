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
def bound_max(array, uncert_array):
    maximum = max(array)
    l = list(i for i in range(len(array)) if array[i]==maximum)
    index = max(l)
    max_with_uncert = array[index] + uncert_array[index]
    return max_with_uncert
def bound_min(array, uncert_array):
    minimum = min(array)
    l = list(i for i in range(len(array)) if array[i]==minimum)
    index = min(l)
    min_with_uncert = array[index] - uncert_array[index]
    return min_with_uncert

day = []
push_ups = []

def DictReader(fname):
    with open(fname, 'rt') as f:
        # read in csv file
        reader = csv.DictReader(f, delimiter=" ", skipinitialspace=True)
        # csv.DictReader by default uses values in the first row of the
        # data file as the field names
        #     the `skipinitialspace` is so that extra whitespace is
        # ignored (like in gnuplot)

        for line in reader:
            day.append(str(line['day']))
            push_ups.append(float(line['push_ups']))
        #print(type(reader))
        #reader.items()

    return(day, push_ups)

ret = DictReader("push_up_data.csv")

day, push_ups = range(2)
# Assign numbers to each variable so that we can use them for indexing later.

day_array = np.array([datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in ret[day]])
push_ups_array = np.array(ret[push_ups])
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

day_delims = np.array([0, 4, 8, 12, 20])
gradient_vals = np.array([0.5, 3, 5, 1])

endval = 0
def piecewise(left_bound, right_bound, start, gradient):
    global endval
    x = np.arange(left_bound, right_bound, 0.005)
    #x = np.arange(bound_min(period_inv2_array, uncert_period_inv2_array), bound_max(period_inv2_array, uncert_period_inv2_array), 0.005)
    plt.plot(x, np.add(np.multiply(gradient, np.subtract(x, left_bound)), start), 'b-', label="$f(x) = {start} + {gradient}(x-{left_bound}), {left_bound} \leq x \leq {right_bound}$".format(start=start,gradient=gradient,left_bound=left_bound,right_bound=right_bound))
    endval = np.add(np.multiply(gradient, np.subtract(right_bound, left_bound)), start)


pl.xlabel(r'Day')
pl.ylabel('Number of push-ups')
pl.title(r"Push-ups vs days")
pl.legend(loc='lower right', prop={'size':10})
turn_on_grid_lines()

#pl.show()
pl.savefig("sample.pdf", format="pdf")
pl.clf() # clear the canvas
########## END PLOT