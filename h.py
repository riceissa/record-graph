import csv

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

DictReader("push_up_data.csv")
