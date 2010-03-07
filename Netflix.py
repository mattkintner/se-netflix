#!/usr/bin/env python

# ----------------------------------
# Peter Dorfman   pad574
# Matt Kintner    mbk229
# ----------------------------------
import math
import os

#   CONSTANTS
# ----------------------------------
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

NUM_MOVIES              = 17770
MOVIE_WEIGHT            = 2.0
CUST_WEIGHT             = 2.0

#   GLOBALS
# ----------------------------------
movieProfiles = (NUM_MOVIES+1)*[None,]
custProfiles = {}
actualRatings = None
probe = None


class ratingProfile (object) :
    
    def __init__(self, avgRating = 0.0, numRated = 0.0, Q = 0.0, stdDev = 0.0):
        self.avgRating = avgRating
        self.numRated = numRated
        self.Q = Q
        self.stdDev = stdDev
    
    def addRating(self, rating) :
        self.numRated += 1
        oldAvg = self.avgRating
        self.avgRating = oldAvg + ((rating-oldAvg)/self.numRated)
        self.Q = self.Q + (rating - oldAvg)*(rating - self.avgRating)
        self.stdDev = math.sqrt(self.Q/self.numRated)
            
    
class custProfile (ratingProfile) :
    pass

class movieProfile (ratingProfile) :
    pass

def addMovieRating (movieID, custID, rating) :
    
    global movieProfiles, custProfiles
    
    if(movieProfiles[movieID] == None):
        movieProfiles[movieID] = movieProfile()
    movieProfiles[movieID].addRating(rating)
    
    if(custID not in custProfiles):
        custProfiles[custID] = custProfile()
    custProfiles[custID].addRating(rating)
    

def netflix_learn (toFile = True, verbose = False) :
    """
    description
    return nothing
    """
    global MOVIES_DIR, actualRatings, probe
    
    # gather all ratings data from training set
    for movieID in range(1,NUM_MOVIES + 1):
        thisFile = MOVIES_DIR + ("mv_00%05d.txt" % movieID);
        f = open(thisFile, 'r')
        thisFile = f.readlines()
        f.close()
        
        for j in range (1, len(thisFile)) :
            temp = thisFile[j].partition(",")
            custID = temp[0]
            rating = ord(temp[2][0])-48
            addMovieRating(movieID,custID,rating);
            
        if verbose
            print "Movie " + str(movieID) + " complete."
    
    
    # generate actual ratings ordered by probe file
    f = open(PROBE_PATH)
    probe = f.read()
    f.close()
    probe = probe.splitlines()
    
    movieID = 0
    
    thisMovieRatings = {}
    tempRatings = []
    
    for thisID in probe:
        i = thisID.find(":")
        
        if i > -1 :  # Movie ID - read movie entries
            lineLen = len(thisID)
            thisFile = MOVIES_DIR + "mv_00" + ((6-lineLen)*"0") + thisID[0:lineLen-1] + ".txt"
            movieID = int(thisID[0:lineLen-1])
            f = open(thisFile, 'r')
            thisFile = f.readlines()
            f.close()
            thisMovieRatings.clear()
            for j in range (1, len(thisFile)) :
                temp = thisFile[j].partition(",")
                thisMovieRatings[temp[0]] = ord(temp[2][0])-48
            
            if verbose
                print "Grabbing Actual Ratings for Movie " + thisID[0:lineLen-1]
        else :
            tempRatings.append(thisMovieRatings[thisID])
            
    actualRatings = tuple(tempRatings)
            
            

    if (toFile) :
        write_brain()
        write_actualRatings()



def write_brain() :
    cache = open(CACHE_BRAIN_FILE, 'w')
    
    cache.write("from Netflix import movieProfile, custProfile\n\nmovieProfiles = [ None, ")
    
    for movieProf in movieProfiles:
        if movieProf != None:
            cache.write("movieProfile(" + str(movieProf.avgRating) + "," + str(movieProf.numRated) + "," + str(movieProf.Q) + "," + str(movieProf.stdDev) + "), ")
        
    cache.write(" ]\n\ncustProfiles = { ")
    
    for custID, custProf in custProfiles.iteritems():
        cache.write("'" + str(custID) + "' : custProfile(" + str(custProf.avgRating) + "," + str(custProf.numRated) + "," + str(custProf.Q) + "," + str(custProf.stdDev) + "), ")
        
    cache.write(" }\n")
    
    
def write_actualRatings() :
    cache = open(CACHE_RATINGS_FILE, 'w')
    
    cache.write("actualRatings = ( ")
    
    for thisRating in actualRatings:
        cache.write( str(thisRating) + ", ")
        
    cache.write(" )\n")


def netflix_get_cache() :
    global movieProfiles, custProfiles, actualRatings
    cache_brain = __import__(CACHE_BRAIN_MODULE,fromlist=["movieProfiles", "custProfiles"])
    cache_ratings = __import__(CACHE_RATINGS_MODULE,fromlist=["actualRatings"])
    movieProfiles = cache_brain.movieProfiles
    custProfiles = cache_brain.custProfiles
    actualRatings = cache_ratings.actualRatings


# ------------
# netflix_eval
# ------------

def netflix_eval (verbose = False) :
    """
    FIXME: description
    return FIXME: something
    """
    
    global actualRatings, probe
    ourRatings = []
    
    if probe == None :
        f = open(PROBE_PATH)
        probe = f.read()
        f.close()
        probe = probe.splitlines()
        
    o = open(RATINGS_OUTPUT_FILE, 'w')
    
    movieID = 0
    
    thisMovieRatings = {}
    
    for thisID in probe:
        i = thisID.find(":")
        
        if i > -1 :  # Movie ID - read movie entries
            movieID = int(thisID[0:i])
            o.write(thisID + "\n")
        else :
            prediction = predict_rating(movieID,thisID)
            ourRatings.append(prediction)
            #prediction = int(prediction*10)/10.0
            o.write(str(prediction) + "\n")
            
    o.close()

    rmseOut = rmse(tuple(actualRatings), tuple(ourRatings))
    if verbose :
        print rmseOut
    o = open(RMSE_OUTPUT_FILE, 'w')
    o.write(str(rmseOut) + '\n')
    o.close()
    

def predict_rating(movieID, custID) :
    movieAvg = movieProfiles[movieID].avgRating
    movieStd = movieProfiles[movieID].stdDev
    custAvg = custProfiles[custID].avgRating
    custStd = custProfiles[custID].stdDev
    return (movieAvg * (MOVIE_WEIGHT - movieStd) + custAvg * (CUST_WEIGHT - custStd)) / (MOVIE_WEIGHT + CUST_WEIGHT - movieStd - custStd)

# -------------
# netflix_print
# -------------

def netflix_print (w, a, v) :
    """
    prints the values of a[0], a[1], and v
    """
    

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


def netflix_testreading () :
    """
    FIXME: description
    return FIXME: something
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
