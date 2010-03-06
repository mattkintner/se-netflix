#!/usr/bin/env python

# ----------------------------------
# Peter Dorfman   pad574
# Matt Kintner    mbk229
# ----------------------------------
from RMSE import rmse
import math
import os

#   CONSTANTS
ROOT_PATH           = "/u/downing/public_html/projects/netflix/"
MOVIE_TITLES_PATH   = ROOT_PATH + "movie_titles.txt"
PROBE_PATH          = ROOT_PATH + "probe.txt"
MOVIES_DIR          = ROOT_PATH + "training_set/"

NUM_MOVIES          = 17770
META_CACHE_MODULE   = "NetflixCache_" + str(NUM_MOVIES)
META_CACHE_FILE     = META_CACHE_MODULE + ".py"

MOVIE_WEIGHT        = 4
CUST_WEIGHT         = 4

#   GLOBALS
movieProfiles = (NUM_MOVIES+1)*[None,]
custProfiles = {}


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
    

def netflix_learn (toFile = True) :
    """
    description
    return nothing
    """
    global MOVIES_DIR
    
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
        print "Movie " + str(movieID) + " complete."

    if (toFile) :
        write_cache()



def write_cache() :
    cache = open(META_CACHE_FILE, 'w')
    
    cache.write("from Netflix import movieProfile, custProfile\n\nmovieProfiles = [ None, ")
    
    for movieProf in movieProfiles:
        if movieProf != None:
            cache.write("movieProfile(" + str(movieProf.avgRating) + "," + str(movieProf.numRated) + "," + str(movieProf.Q) + "," + str(movieProf.stdDev) + "), ")
        
    cache.write("None ]\n\ncustProfiles = { ")
    print(len(custProfiles))
    for custID, custProf in custProfiles.iteritems():
        cache.write("'" + str(custID) + "' : custProfile(" + str(custProf.avgRating) + "," + str(custProf.numRated) + "," + str(custProf.Q) + "," + str(custProf.stdDev) + "), ")
        
    cache.write("-1 : None }\n")


def netflix_get_cache() :
    global movieProfiles, custProfiles
    cache = __import__(META_CACHE_MODULE,fromlist=["movieProfiles", "custProfiles"])
    movieProfiles = cache.movieProfiles
    custProfiles = cache.custProfiles


# ------------
# netflix_eval
# ------------

def netflix_eval () :
    """
    FIXME: description
    return FIXME: something
    """
    
    actualRatings = []
    ourRatings = []
    
    f = open(PROBE_PATH)
    probe = f.read()
    f.close()
    probe = probe.splitlines()
    
    movieID = 0
    
    thisMovieRatings = {}
    
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
        else :
            actualRatings.append(thisMovieRatings[thisID])
            ourRatings.append(predict_rating(movieID,thisID))
            
    

    print rmse(tuple(actualRatings), tuple(ourRatings))
    

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
