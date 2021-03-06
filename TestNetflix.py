
# To run the tests
#     TestNetflix.py

import unittest
import Netflix
netflix_learn               = Netflix.netflix_learn
netflix_eval                = Netflix.netflix_eval
netflix_build_actual_ratings= Netflix.netflix_build_actual_ratings
netflix_add_movie_rating    = Netflix.netflix_add_movie_rating
netflix_predict_rating      = Netflix.netflix_predict_rating
netflix_get_cache           = Netflix.netflix_get_cache

ratingProfile               = Netflix.ratingProfile
custProfile                 = Netflix.custProfile
movieProfile                = Netflix.movieProfile


# -----------
# TestNetflix
# -----------

class TestNetflix(unittest.TestCase) :
    
    def tearDown(self) :
        """
        Reset Netflix module globals that may have been edited during a test
        """
        Netflix.toFile          = True
        Netflix.verbose         = False
        Netflix.testing         = True
        Netflix.NUM_MOVIES      = 17770
        Netflix.movieProfiles   = (Netflix.NUM_MOVIES+1)*[None,]
        Netflix.custProfiles    = {}
        Netflix.actualRatings   = None
        Netflix.probe           = None
    
    # ----
    # rating profiles
    # ----

    def test_createMovieProfile (self) :
        """
        Create a new movie profile
        """
        m = movieProfile()
        self.assert_(m.avgRating    == 0)
        self.assert_(m.numRated     == 0)
        self.assert_(m.Q            == 0)
        self.assert_(m.stdDev       == 0)

    def test_createCustProfile (self) :
        """
        Create a new customer profile
        """
        p = custProfile()
        self.assert_(p.avgRating    == 0)
        self.assert_(p.numRated     == 0)
        self.assert_(p.Q            == 0)
        self.assert_(p.stdDev       == 0)
        
    def test_add_rating_cust (self) :
        """
        Add ratings to a customer profile
        """
        p = custProfile()
        p.add_rating(2)
        p.add_rating(4)
        p.add_rating(4)
        p.add_rating(4)
        p.add_rating(5)
        p.add_rating(5)
        p.add_rating(7)
        p.add_rating(9)
        self.assert_(p.numRated     == 8)
        self.assert_(p.avgRating    == 5)
        self.assert_(p.stdDev       == 2)

    def test_add_rating_movie (self) :
        """
        Add ratings to a movie profile
        """
        m = movieProfile()
        m.add_rating(2)
        m.add_rating(4)
        m.add_rating(4)
        m.add_rating(4)
        m.add_rating(5)
        m.add_rating(5)
        m.add_rating(7)
        m.add_rating(9)
        self.assert_(m.numRated     == 8)
        self.assert_(m.avgRating    == 5)
        self.assert_(m.stdDev       == 2)


    # ----
    # add movie ratings to global lists
    # ----

    def test_add_ratings (self) :
        """
        Add specific ratings of a customer for a movie and test that they 
        append to the appropriate structures and the structures update correctly
        """
        self.assert_(len(Netflix.custProfiles) == 0)
        self.assert_(Netflix.movieProfiles[1] == None);
        self.assert_(type(Netflix.movieProfiles[1]) is not Netflix.movieProfile);
        
        # add first movie and customer (now 1 movies, 1 customers)
        netflix_add_movie_rating(1,"7",3)
        self.assert_(len(Netflix.custProfiles) == 1)
        self.assert_(type(Netflix.custProfiles["7"]) is Netflix.custProfile)
        thisCust = Netflix.custProfiles["7"]
        self.assert_(thisCust.numRated == 1);
        self.assert_(thisCust.avgRating == 3);
        self.assert_(thisCust.stdDev == 0);
        self.assert_(type(Netflix.movieProfiles[1]) is Netflix.movieProfile);
        thisMovie = Netflix.movieProfiles[1]
        self.assert_(thisMovie.numRated == 1);
        self.assert_(thisMovie.avgRating == 3);
        self.assert_(thisMovie.stdDev == 0);
        
        # add second customer rating first movie (now 1 movies, 2 customers)
        netflix_add_movie_rating(1,"77",2)
        self.assert_(len(Netflix.custProfiles) == 2)
        self.assert_(type(Netflix.custProfiles["77"]) is Netflix.custProfile)
        thisCust = Netflix.custProfiles["77"]
        self.assert_(thisCust.numRated == 1);
        self.assert_(thisCust.avgRating == 2);
        self.assert_(thisCust.stdDev == 0);
        self.assert_(type(Netflix.movieProfiles[1]) is Netflix.movieProfile);
        thisMovie = Netflix.movieProfiles[1]
        self.assert_(thisMovie.numRated == 2);
        self.assert_(thisMovie.avgRating == 2.5);
        self.assert_(thisMovie.stdDev == .5);
        
        # add second movie rated by first customer (now 2 movies, 2 customers)
        netflix_add_movie_rating(3,"7",4)
        self.assert_(len(Netflix.custProfiles) == 2)
        self.assert_(type(Netflix.custProfiles["7"]) is Netflix.custProfile)
        thisCust = Netflix.custProfiles["7"]
        self.assert_(thisCust.numRated == 2);
        self.assert_(thisCust.avgRating == 3.5);
        self.assert_(thisCust.stdDev == .5);
        self.assert_(type(Netflix.movieProfiles[3]) is Netflix.movieProfile);
        thisMovie = Netflix.movieProfiles[3]
        self.assert_(thisMovie.numRated == 1);
        self.assert_(thisMovie.avgRating == 4);
        self.assert_(thisMovie.stdDev == 0);
        
    
    # ----
    # rating prediction
    # ----
    def test_netflix_predict_rating(self) :
        """
        Test the prediction algorithm
        """
        self.assert_(len(Netflix.custProfiles) == 0)
        self.assert_(Netflix.movieProfiles[1] == None);
        self.assert_(type(Netflix.movieProfiles[1]) is not Netflix.movieProfile);
        
        # movie 1 ratings setup
        netflix_add_movie_rating(1,"7",4)
        netflix_add_movie_rating(1,"8",4)
        netflix_add_movie_rating(1,"9",4)
        
        # customer 1 ratings setup
        netflix_add_movie_rating(2,"1",2)
        netflix_add_movie_rating(3,"1",2)
        netflix_add_movie_rating(4,"1",2)
        
        self.assert_(netflix_predict_rating(1, "1") == 3)
        
        
    # ----
    # building actual ratings tuple
    # ----
    def test_build_actual_ratings(self) :
        """
        Test the building of the global actualRatings variable
        """
        verifiedRatings         = (5, 3, 3, 2)
        Netflix.probe           = ["2043:", "779760", "92056", "11197", "163:", "2147527"]
        netflix_build_actual_ratings()
        self.assert_(verifiedRatings == Netflix.actualRatings)
        
        
    # ----
    # eval
    # ----
    def test_netflix_eval(self) :
        """
        Test the evaluation method
        """
        Netflix.testing         = True
        Netflix.actualRatings   = (5, 3, 2)
        Netflix.probe           = ["2043:", "779760", "11197", "163:", "2147527"]
        
        Netflix.movieProfiles[2043] = movieProfile(4.0, 2, 0.0, 1.0)
        Netflix.movieProfiles[163]  = movieProfile(2.0, 1, 0.0, 0.0)
        Netflix.custProfiles    = { '779760' : custProfile(5.0, 1, 0.0, 0.0), '11197' : custProfile(3.0, 1, 0.0, 0.0), '2147527' : custProfile(2.0, 1, 0.0, 0.0),  }
        out = int(netflix_eval() * 100000)/100000.0
        self.assert_(out == 0.27216)



if __name__ == "__main__" :
    print "TestNetflix.py"
    unittest.main()
    print "Done."
