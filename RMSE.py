#!/usr/bin/env python

# -------
# RMSE.py
# -------

import math

print "RMSE.py"

def rmse (a, p) :
    assert type(a) == tuple
    assert type(p) == tuple
    assert len(a)  == len(p)
    i = 0
    s = len(a)
    w = 0
    while i != s :
        v = a[i] - float(p[i])
        w += (v * v)
        i += 1
    assert type(w) is float
    assert 0 <= w <= (16 * s)
    m = (w / s)
    assert type(m) is float
    assert 0 <= m <= 16
    r = math.sqrt(m)
    assert type(r) is float
    assert 0 <= r <= 4
    return r

assert str(rmse((3, 3, 3),       (3, 3, 3)))       == "0.0"
assert str(rmse((1, 1, 1, 1),    (5, 5, 5, 5)))    == "4.0"
assert str(rmse((5, 3, 2, 4, 5), (2, 4, 3, 1, 2))) == "2.40831891576"

print "Done."
