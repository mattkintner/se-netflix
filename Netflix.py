#!/usr/bin/env python

# ----------------------------------
# Peter Dorfman   pad574
# Matt Kintner    mbk229
# ----------------------------------
import math
import os, sys

#   CONSTANTS
# ----------------------------------

NUM_MOVIES              = 17770
MOVIE_WEIGHT            = 2.0
CUST_WEIGHT             = 2.0

ROOT_PATH               = "/u/downing/public_html/projects/netflix/"
MOVIE_TITLES_PATH       = ROOT_PATH + "movie_titles.txt"
PROBE_PATH              = ROOT_PATH + "probe.txt"
MOVIES_DIR              = ROOT_PATH + "training_set/"

CACHE_BRAIN_MODULE      = "NetflixCache_" + str(NUM_MOVIES)
CACHE_BRAIN_FILE        = CACHE_BRAIN_MODULE + ".py"
CACHE_RATINGS_MODULE    = "NetflixCache_Ratings"
CACHE_RATINGS_FILE      = CACHE_RATINGS_MODULE + ".py"
RATINGS_OUTPUT_FILE     = "RunNetflix.out"
RMSE_OUTPUT_FILE        = "RMSE"


#   GLOBALS
# ----------------------------------
# flags
toFile = True
verbose = False
testing = False

movieProfiles = (NUM_MOVIES+1)*[None,]
custProfiles = {}
actualRatings = None
probe = None


class ratingProfile (object) :
    """
    Represents average rating and standard deviation used in a movie or customer profile.
    """
    
    def __init__(self, avgRating = 0.0, numRated = 0, Q = 0.0, stdDev = 0.0):
        """
        Initialize this profile.
        @param  avgRating:
        @type   avgRating:  float
        @param  numRated:   
        @type   numRated:   int
        @param  Q:          
        @type   Q:          float
        @param  stdDev:     
        @type   stdDev:     float
        """
        self.avgRating = avgRating
        self.numRated = numRated
        self.Q = Q
        self.stdDev = stdDev
    
    def add_rating(self, rating) :
        """
        Add rating into statistics for this profile.
        @param rating: rating to include
        @type rating: int
        """
        self.numRated += 1
        oldAvg = self.avgRating
        self.avgRating = oldAvg + ((rating-oldAvg)/self.numRated)
        self.Q = self.Q + (rating - oldAvg)*(rating - self.avgRating)
        self.stdDev = math.sqrt(self.Q/self.numRated)
            
    
class custProfile (ratingProfile) :
    """
    Profile of a customer, including rating statistics.
    """
    pass

class movieProfile (ratingProfile) :
    """
    Profile of a movie, including rating statistics.
    """
    pass

# --------------
# addMovieRating
# --------------

def netflix_add_movie_rating (movieID, custID, rating) :
    """
	Factor movie rating into averages of movie and customer.
    @param movieID: ID of movie  
    @type movieID: int
    @param custID: ID of customer
    @type custID: string
    @param rating: rating given by customer to movie
    @type rating: int
    """
    global movieProfiles, custProfiles
    
    if(movieProfiles[movieID] == None):
        movieProfiles[movieID] = movieProfile()
        
    temp = movieProfiles[movieID].numRated
    movieProfiles[movieID].add_rating(rating)
    assert(movieProfiles[movieID].numRated == temp + 1)
    
    if(custID not in custProfiles):
        custProfiles[custID] = custProfile()
    temp = custProfiles[custID].numRated
    custProfiles[custID].add_rating(rating)
    assert(custProfiles[custID].numRated == temp + 1)
    

# -------------
# netflix_learn
# -------------

def netflix_learn () :
    """
    Read entire training set and calculate average ratings for movies and customers.
    @param toFile: store learned data to cache file
    @type toFile: bool
    @param verbose: print status during learning
    @type verbose: bool
    """
    global toFile, verbose
    global MOVIES_DIR
    
    # gather all ratings data from training set
    for movieID in range(1,NUM_MOVIES + 1):
        thisFile = MOVIES_DIR + ("mv_00%05d.txt" % movieID);
        assert(os.path.exists(thisFile))
        
        f = open(thisFile, 'r')
        thisFile = f.readlines()
        f.close()
        
        for j in range (1, len(thisFile)) :
            temp = thisFile[j].partition(",")
            custID = temp[0]
            rating = ord(temp[2][0])-48
            netflix_add_movie_rating(movieID,custID,rating);
            
        if verbose :
            print "Brain absorbed knowledge of Movie " + str(movieID) + " from training set."
    
    netflix_build_actual_ratings()
    
    if (toFile) :
        netflix_write_brain()
        if verbose :
            print "New 'Brain' Cache written to file: '" + CACHE_BRAIN_FILE + "'"
        netflix_write_actual_ratings()
        if verbose :
            print "New actualRatings Cache written to file: '" + CACHE_RATINGS_FILE + "'"
    
    

def netflix_build_actual_ratings () :
    """
    Generate actual ratings, with order dictated by probe file, to be compared to predictions
    @param verbose: print status during learning
    @type verbose: bool
    """
    
    global verbose
    global MOVIES_DIR, PROBE_PATH
    global actualRatings, probe
    
    # allows for testing with hard-coded probe data
    if probe == None :
        f = open(PROBE_PATH)
        probe = f.read()
        f.close()
        probe = probe.splitlines()
    
    movieID = 0
    thisMovieRatings = {}
    tempRatings = []
    
    for thisID in probe:
        i = thisID.find(":")
        
        if i > -1 :  # This is Movie ID - read movie entries
            
            lineLen = len(thisID)
            thisFile = MOVIES_DIR + "mv_00" + ((6-lineLen)*"0") + thisID[0:lineLen-1] + ".txt"
            movieID = int(thisID[0:lineLen-1])
            assert(movieID > 0)
            assert(movieID <= NUM_MOVIES)
            
            f = open(thisFile, 'r')
            thisFile = f.readlines()
            f.close()
            
            thisMovieRatings.clear()
            for j in range (1, len(thisFile)) :
                temp = thisFile[j].partition(",")
                tempRating = ord(temp[2][0])-48
                assert(tempRating > 0)
                assert(tempRating <= 5)
                thisMovieRatings[temp[0]] = tempRating
            
            if verbose :
                print "Grabbing Actual Ratings for Movie " + thisID[0:lineLen-1]
                
        else :  #this is a Customer ID, find and add their rating
            tempRatings.append(thisMovieRatings[thisID])
            
    actualRatings = tuple(tempRatings)



# -----------
# netflix_write_brain
# -----------

def netflix_write_brain() :
    """
    Store movie and customer profiles to cache.
    """
    cache = open(CACHE_BRAIN_FILE, 'w')
    
    cache.write("from Netflix import movieProfile, custProfile\n\nmovieProfiles = [ None, ")
    
    for movieProf in movieProfiles:
        if movieProf != None:
            assert(type(movieProf) is movieProfile)
            cache.write("movieProfile(" + str(movieProf.avgRating) + "," + str(movieProf.numRated) + "," + str(movieProf.Q) + "," + str(movieProf.stdDev) + "), ")
        
    cache.write(" ]\n\ncustProfiles = { ")
    
    for custID, custProf in custProfiles.iteritems():
        assert(type(custProf) is custProfile)
        cache.write("'" + str(custID) + "' : custProfile(" + str(custProf.avgRating) + "," + str(custProf.numRated) + "," + str(custProf.Q) + "," + str(custProf.stdDev) + "), ")
        
    cache.write(" }\n")
    cache.close()
    

# -------------------
# netflix_write_actual_ratings
# -------------------
    
def netflix_write_actual_ratings() :
    """
    Store actual ratings to cache file.
    """
    global CACHE_RATINGS_FILE
    global actualRatings
    
    cache = open(CACHE_RATINGS_FILE, 'w')
    cache.write("actualRatings = ( ")
    
    for thisRating in actualRatings:
        cache.write( str(thisRating) + ", ")
        
    cache.write(" )\n")
    cache.close()

# -----------------
# netflix_get_cache
# -----------------

def netflix_get_cache() :
    """
    Load movie and customer profiles and actual ratings from cache.
    """
    global movieProfiles, custProfiles, actualRatings
    global CACHE_BRAIN_MODULE, CACHE_RATINGS_MODULE
    
        
    try :
        cache_ratings = __import__(CACHE_RATINGS_MODULE,fromlist=["actualRatings"])
    except ImportError:
        print "Netflix Actual Ratings Cache File '" + CACHE_RATINGS_FILE + "' not found."
        print "Try running again without the -cr flag."
        exit(1)
        
    try :
        cache_brain = __import__(CACHE_BRAIN_MODULE,fromlist=["movieProfiles", "custProfiles"])
    except ImportError:
        print "Netflix Brain Cache File '" + CACHE_BRAIN_FILE + "' not found."
        print "Try running again without the -cr flag."
        sys.exit(1)
        
    movieProfiles = cache_brain.movieProfiles
    custProfiles = cache_brain.custProfiles
    actualRatings = cache_ratings.actualRatings
    assert(movieProfiles != None)
    assert(len(movieProfiles) > 0)
    assert(custProfiles != None)
    assert(len(custProfiles ) > 0)
    assert(actualRatings != None)
    assert(len(actualRatings) > 0)


# ------------
# netflix_eval
# ------------

def netflix_eval () :
    """
    Use learned data to evaluate and predict ratings of other movies.
    @param verbose: print status during evaulation
    @type verbose:  bool
    @return:        calculated RMSE
    @rtype:         float
    """
    global verbose
    global PROBE_PATH, RATINGS_OUTPUT_FILE, RMSE_OUTPUT_FILE
    global actualRatings, probe, CUST_WEIGHT, MOVIE_WEIGHT
    
    ourRatings = []
    
    if probe == None :
        f = open(PROBE_PATH)
        probe = f.read()
        f.close()
        probe = probe.splitlines()
    
    movieID = 0
    thisMovieRatings = {}
    
    if(not testing) :
        o = open(RATINGS_OUTPUT_FILE, 'w')
    for thisID in probe:
        i = thisID.find(":")
        
        if i > -1 :  # Movie ID - read movie entries
            movieID = int(thisID[0:i])
            if(not testing) :
                o.write(thisID + "\n")
        else :
            prediction = netflix_predict_rating(movieID,thisID)
            assert(prediction >= 1.0)
            assert(prediction <= 5.0)
            ourRatings.append(prediction)
            #prediction = int(prediction*10)/10.0
            if(not testing) :
                o.write(str(prediction) + "\n")
    if(not testing) :
        o.close()
    
    if verbose and not testing:
        print "Brain predictions written to file: '" + RATINGS_OUTPUT_FILE + "'"
            
    rmseOut = rmse(tuple(actualRatings), tuple(ourRatings))
    if verbose :
        print "RMSE result: " + str(rmseOut)
    
    if(not testing) :
        o = open(RMSE_OUTPUT_FILE, 'w')
        o.write(str(rmseOut) + '\n')
        o.close()
    
    if verbose and not testing:
        print "RMSE result written to file: '" + RMSE_OUTPUT_FILE + "'"
    
    return rmseOut
    

def netflix_predict_rating(movieID, custID) :
    """
    Compute this user's predicted rating of this movie
    @param movieID:       the ID of the movie this customer will rate
    @type movieID:        int
    @param custID:        the ID of the customer to predict for
    @type custID :        string
    @return:              predicted rating
    @rtype:               float
    """
    global movieProfiles, custProfiles, CUST_WEIGHT, MOVIE_WEIGHT
    movieAvg = movieProfiles[movieID].avgRating
    movieStd = movieProfiles[movieID].stdDev
    custAvg = custProfiles[custID].avgRating
    custStd = custProfiles[custID].stdDev
    return (movieAvg * (MOVIE_WEIGHT - movieStd) + custAvg * (CUST_WEIGHT - custStd)) / (MOVIE_WEIGHT + CUST_WEIGHT - movieStd - custStd)
    

# -----------------------
# rmse
#
# (from provided RMSE.py)
# -----------------------

def rmse (a, p) :
    """
    Calculate RMSE.

    From provided RMSE.py
    @param a: actual ratings
    @type a: tuple
    @param p: predicted ratings
    @type p: tuple
    @return: root mean squared error
    @rtype: float
    """
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


# -------------------
# netflix_test_reading
# -------------------

def netflix_test_reading () :
    """
    Predict ratings of all 3's.
    """
    
    trainingData = []
    
    currentRatings = {}
    
    f = open(PROBE_PATH)
    probeData = f.read()
    f.close()
    probeData = probeData.splitlines()
    
    
    for probeLine in probeData:
        i = probeLine.find(":")
        if i > -1:
            probeLineLen = len(probeLine)
            thisFile = MOVIES_DIR + "mv_00" + ((6-probeLineLen)*"0") + probeLine[0:probeLineLen-1] + ".txt"
            f = open(thisFile, 'r')
            thisFile = f.readlines()
            f.close()
            currentRatings.clear()
            for j in range (1, len(thisFile)) :
                temp = thisFile[j].partition(",")
                currentRatings[temp[0]] = ord(temp[2][0])-48
        else:
            trainingData.append(currentRatings[probeLine])
            
    
    controlData = len(trainingData)*(3,)

    print rmse(tuple(trainingData), controlData)
