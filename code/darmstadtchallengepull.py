
import urllib.request
import bz2
import tempfile
import numpy as np
from fpylll import IntegerMatrix

# change the dimension as we get more and more confident in our methodolgy
# this is for our experimentation down the track, but getting it set up now
def load_darmstadt_challenge(dimension=200):
    """
    Testing library because we need to create experiments on SVP challenge instances.
    These should be repeatable by others, and ones that are used by others
    as a sort of form of truth and benchmark.
    Downloads and parses an SVP challenge matrix from latticechallenge.org
    """
    url = f"https://www.latticechallenge.org/challenges/challenge-{dimension}.bz2"
    print(f"Fetching challenge from: {url}")
    
    # basic implementation and error handling
    try:
        # Download and decompress
        response = urllib.request.urlopen(url)
        data = bz2.decompress(response.read()).decode("utf-8")
        
        # The format starts with metadata, then the matrix inside [ ]
        # We strip the metadata to get the raw numbers
        lines = data.splitlines()
        # Find where the matrix starts (usually line 3 or 4)
        matrix_str = " ".join(lines[3:]) 
        
        # Clean up brackets and commas for fpylll parsing
        matrix_str = matrix_str.replace("[", "").replace("]", "").replace(",", "")
        numbers = list(map(int, matrix_str.split()))
        
        # Darmstadt challenges are n x n matrices
        mat = IntegerMatrix(dimension, dimension)
        for i in range(dimension):
            for j in range(dimension):
                mat[i, j] = numbers[i * dimension + j]
                
        print(f"Successfully loaded {dimension}x{dimension} challenge matrix.")
        return mat

    except Exception as e:
        print(f"Error loading challenge: {e}")
        print(f"Unable to load Darmstadt challenge of dimension {dimension}.")
        return None

# Example Usage:
# challenge_mat = load_darmstadt_challenge(60) # Start small!
# basis_as_arrays = [np.array(row) for row in challenge_mat]