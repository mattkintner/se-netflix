
# To run the tests
#     TestNetflix.py

import unittest

from Netflix import netflix_learn, netflix_eval, netflix_print

# ------
# Reader
# ------

class Reader (object) :
    def __init__ (self, s) :
        self.s = s

    def read (self) :
        return self.s

# ------
# Writer
# ------

class Writer (object) :
    def str (self) :
        return self.s

    def write (self, a, v) :
        self.s  = str(a[0]) + " "
        self.s += str(a[1]) + " "
        self.s += str(v)    + "\n"

# -----------
# TestCollatz
# -----------

class TestNetflix(unittest.TestCase) :
    # ----
    # read
    # ----

    def test_read (self) :
        r = Reader("1 10\n")
        a = []
        b = netflix_read(r, a)
        self.assert_(b    == True)
        self.assert_(a[0] ==  1)
        self.assert_(a[1] == 10)

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        v = netflix_eval([1, 10])
        self.assert_(v == 20)

    def test_eval_2 (self) :
        v = netflix_eval([100, 200])
        self.assert_(v == 125)

    def test_eval_3 (self) :
        v = netflix_eval([201, 210])
        self.assert_(v == 89)

    def test_eval_4 (self) :
        v = netflix_eval([900, 1000])
        self.assert_(v == 174)

    # -----
    # print
    # -----

    def test_print (self) :
        w = Writer()
        netflix_print(w, [1, 10], 20)
        self.assert_(w.str() == "1 10 20\n")

if __name__ == "__main__" :
    print "TestNetflix.py"
    unittest.main()
    print "Done."
