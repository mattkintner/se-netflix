#!/usr/bin/env python

# -------------------------------------
# projects/python/netflix/RunNetflix.py
# Copyright (C) 2010
# Glenn P. Downing
# -------------------------------------

# To run the program
#     RunNetflix.py < RunNetflix.in > RunNetflix.out

# To document the program
#     pydoc -w Netflix RunNetflix TestNetflix

import Netflix
import sys


# ----
# main
# ----

def main () :
    """
    runs the program. Cache used is determined by flags below
    Default (no flags): use training set to create internal cache (no cache file read or write)
    @flag   -cw     Cache Write: process training set to write cache to external file
    @flag   -cr     Cache Read:  use external cache file (no training set processing)
    @flag   -v      Verbose:  use external cache file (no training set processing)
    """
    
    Netflix.verbose = "-v" in sys.argv
    Netflix.toFile = "-cw" in sys.argv
    
    if "-cr" not in sys.argv :
        Netflix.netflix_learn()
    else :
        Netflix.netflix_get_cache()
    
    Netflix.netflix_eval()

if __name__ == "__main__" :
    main()
