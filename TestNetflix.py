
# To run the tests
#     TestNetflix.py

import unittest
import Netflix
netflix_learn   = Netflix.netflix_learn
netflix_eval    = Netflix.netflix_eval
netflix_print   = Netflix.netflix_print
ratingProfile   = Netflix.ratingProfile
custProfile     = Netflix.custProfile
movieProfile    = Netflix.movieProfile
addMovieRating  = Netflix.addMovieRating

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
        
        
        
    def test_addRating_cust (self) :
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

    def test_addRating_movie (self) :
        m = movieProfile()
        m.addRating(2)
        m.addRating(4)
        m.addRating(4)
        m.addRating(4)
        m.addRating(5)
        m.addRating(5)
        m.addRating(7)
        m.addRating(9)
        self.assert_(m.numRated     == 8)
        self.assert_(m.avgRating    == 5)
        self.assert_(m.stdDev       == 2)


    # ----
    # add movie ratings to global list
    # ----

    def test_addMovieRatings (self) :
        self.assert_(len(Netflix.custProfiles) == 0)
        self.assert_(Netflix.movieProfiles[1] == None);
        self.assert_(type(Netflix.movieProfiles[1]) is not Netflix.movieProfile);
        
        addMovieRating(1,2,3)
        self.assert_(len(Netflix.custProfiles) == 1)
        self.assert_(type(Netflix.movieProfiles[1]) is Netflix.movieProfile);


if __name__ == "__main__" :
    print "TestNetflix.py"
    unittest.main()
    print "Done."
