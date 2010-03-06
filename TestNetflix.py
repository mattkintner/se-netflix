
# To run the tests
#     TestNetflix.py

import unittest

from Netflix import netflix_learn, netflix_eval, netflix_print, ratingProfile, custProfile, movieProfile

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
    # rating profile
    # ----

    def test_custRatings (self) :
        p = custProfile()
        self.assert_(p.avgRating    == 0)
        self.assert_(p.numRated     == 0)
        self.assert_(p.Q            == 0)
        self.assert_(p.stdDev       == 0)
        
        p.addRating(2)
        p.addRating(4)
        p.addRating(4)
        p.addRating(4)
        p.addRating(5)
        p.addRating(5)
        p.addRating(7)
        p.addRating(9)
        self.assert_(p.numRated     == 8)
        self.assert_(p.avgRating    == 5)
        self.assert_(p.stdDev       == 2)

    def test_movieRatings (self) :
        p = movieProfile()
        self.assert_(p.avgRating    == 0)
        self.assert_(p.numRated     == 0)
        self.assert_(p.Q            == 0)
        self.assert_(p.stdDev       == 0)
        
        p.addRating(2)
        p.addRating(4)
        p.addRating(4)
        p.addRating(4)
        p.addRating(5)
        p.addRating(5)
        p.addRating(7)
        p.addRating(9)
        self.assert_(p.numRated     == 8)
        self.assert_(p.avgRating    == 5)
        self.assert_(p.stdDev       == 2)
        
    def test_test (self) :
        d = 17771*[None,]
        if(d[1] == None):
            d[1] = movieProfile()
        d[1].addRating(1)
        print d[1].avgRating
        if(d[1] == None):
            d[1] = movieProfile()
        d[1].addRating(3)
        print d[1].avgRating
        
        


if __name__ == "__main__" :
    print "TestNetflix.py"
    unittest.main()
    print "Done."
