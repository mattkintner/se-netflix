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

from Netflix import netflix_read, netflix_eval, netflix_print

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
    runs the program
    """
    netflix_read()

if __name__ == "__main__" :
    main()
