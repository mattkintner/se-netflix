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

from Netflix import netflix_learn, netflix_eval, netflix_print, netflix_get_cache
import sys

# ------
# Reader
# ------

class Reader (object) :
    def read (self) :
        return raw_input()

# ------
# Writer
# ------

class Writer (object) :
    def write (self, a, v) :
        for i in a :
            print i,
        print v

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
    if "-cr" not in sys.argv :
        netflix_learn("-cw" in sys.argv, "-v" in sys.argv)
    else :
        netflix_get_cache()
    
    netflix_eval("-v" in sys.argv)

if __name__ == "__main__" :
    main()
