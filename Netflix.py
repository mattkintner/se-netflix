#!/usr/bin/env python

# ----------------------------------
# Peter Dorfman   pad574
# Matt Kintner    mbk229
# ----------------------------------
from RMSE import rmse

# ------------
# netflix_read
# ------------

rootPath     = "/u/downing/public_html/projects/netflix/"
movieTitlesPath    = rootPath + "movie_titles.txt"
probePath     = rootPath + "probe.txt"
moviesDir     = rootPath + "training_set/"

def netflix_read () :
    """
    reads an int into a[0] and a[1]
    return true if that succeeds, false otherwise
    """
    
    trainingData = []
    
    currentRatings = {}
    
    f = open(probePath)
    probeData = f.readlines()
    f.close()
    
    
    
    for probeLine in probeData:
        i = probeLine.find(":")
        if i > -1:
            thisFile = moviesDir + "mv_%07d.txt" % (int(probeLine.rstrip(":\n")))
            f = open(thisFile, 'r')
            thisFile = f.readlines()
            f.close()
            currentRatings.clear()
            for j in range (1, len(thisFile)) :
                temp = thisFile[j].split(",")
                currentRatings[int(temp[0])] = int(temp[1])
        else:
            trainingData.append(currentRatings[int(probeLine)])
    
    controlData = len(trainingData)*(3,)

    print rmse(tuple(trainingData), controlData)


# ------------
# netflix_eval
# ------------

def netflix_eval (a) :
    """
    computes the max cycle length in the range [i, j]
    and stores the result in v
    """

# -------------
# netflix_print
# -------------

def netflix_print (w, a, v) :
    """
    prints the values of a[0], a[1], and v
    """
    
