
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
    # rating profiles
    # ----

    def test_createMovieRating (self) :
        m = movieProfile()
        self.assert_(m.avgRating    == 0)
        self.assert_(m.numRated     == 0)
        self.assert_(m.Q            == 0)
        self.assert_(m.stdDev       == 0)

    def test_createCustRating (self) :
        p = custProfile()
        self.assert_(p.avgRating    == 0)
        self.assert_(p.numRated     == 0)
        self.assert_(p.Q            == 0)
        self.assert_(p.stdDev       == 0)
        
        
        
    def test_addCustRatings (self) :
        p = custProfile()
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

    def test_addMovieRatings (self) :
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


    # ----
    # rating profiles
    # ----

    def test_movieRatings (self) :
        pass


if __name__ == "__main__" :
    print "TestNetflix.py"
    unittest.main()
    print "Done."
