### the next stage is BKZ

## different run times, and such....
## bkz relies on several things different to LLL - block size, and the same delta as before


import numpy as np

from itertools import product
from fpylll import IntegerMatrix, shortest_vector

# this takes in the basis vectors of the lattice basis
# then we will compute this based on a delta, which is our "loose" 
# factor that allows our fraction that is not too loose, or not too tight
# block size included because change from LL to BKZ is this

def compute_gso(B, B_star, Mu, k):
    #Computes/updates the Gram-Schmidt components (B_star, Mu) for vector B[k]
    #with respect to all previous orthogonal vectors B_star[j] for j < k.
    b_k = B[k]
    b_star_k = b_k.copy()

    # Iterate through all preceding vectors j = 0 to k-1
    for j in range(k):
        # Calculate mu_k, j
        # Inner product of the vector b_k and the orthogonal vector b_j*
        mu_kj = np.dot(b_k, B_star[j]) / np.dot(B_star[j], B_star[j])
    
        Mu[k, j] = mu_kj
    
        # Calculate b_k* = b_k - sum_{j=0}^{k-1} mu_k, j * b_j*
        b_star_k -= mu_kj * B_star[j]

    B_star[k] = b_star_k

def size_reduce(B, B_star, Mu, k, j):
    # The coefficient mu_k, j
    mu_kj = Mu[k, j]

    # The integer k to subtract: k = round(mu_k, j)
    # rounded because we are in integer lattice
    k_int = np.round(mu_kj)

    # Perform the reduction if k_int is non-zero
    if k_int != 0:
        # Update the basis vector: b_k = b_k - k_int * b_j
        B[k] -= k_int * B[j]
        
        # Update the GSO coefficient: mu_k, j = mu_k, j - k_int
        Mu[k, j] = mu_kj - k_int
        
        # Then update all preceding coefficients Mu[k, l] for l < j
        for l in range(j):
            Mu[k, l] -= k_int * Mu[j, l]
        
        # Since b_k changed,  recompute b_k* (B_star[k]).
        # The easiest way is to call the GSO function again for index k.
        compute_gso(B, B_star, Mu, k)

    # Return True if a reduction occurred, False otherwise
    return k_int != 0

def find_shortest_vector(subbasis):
    if not subbasis:
        return None
    # SVP Solver: This doesn't just run LLL. 
    # It performs an "Enumeration" search to find the literal shortest vector.
    mat = IntegerMatrix.from_matrix([list(map(int, b)) for b in subbasis])
    sv = shortest_vector(mat)
    return np.array(sv)


def LLL_alg(basis_vectors, delta=0.75):
    # The input basis_vectors are a list of lists
    B = [np.array(v, dtype=float) for v in basis_vectors]
    d = len(B) # Dimension of the lattice basis

    # Initialize GSO matrices
    B_star = [np.zeros_like(B[0], dtype=float) for _ in range(d)]
    Mu = np.zeros((d, d), dtype=float)

    # Compute initial GSO for the whole basis (only needed once), for this process
    for i in range(d):
        compute_gso(B, B_star, Mu, i)

    # LLL Loop starts at k=1 (checking b_2 and b_1)
    k = 1 
    while k < d:
        # Size Reduction (for b_k w.r.t b_{j} where j < k) 
        # Reduce b_k w.r.t. b_{k-1}, b_{k-2}, ..., b_0
        for j in range(k - 1, -1, -1): # Iterate backwards from k-1 down to 0
            size_reduce(B, B_star, Mu, k, j)

        # Lovász Condition Check
        # The condition checks: delta * ||b_k*||^2 >= (||b_{k-1}^*||^2 + mu_{k, k-1}^2 * ||b_{k-1}^*||^2)
        
        # Calculate the squared norms ||b_{i}^*||^2 = <b_{i}^*, b_{i}^*>
        norm_sq_k = np.dot(B_star[k], B_star[k])
        norm_sq_k_minus_1 = np.dot(B_star[k-1], B_star[k-1])
        
        mu_k_k_minus_1 = Mu[k, k-1]
        
        # delta * ||b_k*||^2 > ||b_{k-1}^*||^2 * (delta - mu_{k, k-1}^2)
        # We will use the common form: 
        lovasz_satisfied = (delta * norm_sq_k) >= \
                           (norm_sq_k_minus_1 + (mu_k_k_minus_1**2 * norm_sq_k_minus_1))

        if lovasz_satisfied:
            # Condition satisfied: move to the next vector k+1
            k += 1
        else:
            # --- Step 3: Swap and return to Step 1 
            # Swap B[k] and B[k-1] in the basis
            B[k], B[k-1] = B[k-1], B[k]
            
            # Since the basis changed, the GSO components are invalid.
            # We must update GSO for the affected vectors (k-1 and k).
            # The easiest way is to re-calculate GSO for both k-1 and k
            #
            compute_gso(B, B_star, Mu, k - 1)
            compute_gso(B, B_star, Mu, k)

            # Return to the previous index k-1 to re-check the swapped vectors
            k = max(1, k - 1)

    # Return the LLL-reduced basis as a list of numpy arrays
    return B

def BKZ_alg(basis_vectors, blocksize, delta=0.75):
    print(f"--- Starting BKZ with blocksize {blocksize} ---")
    B = LLL_alg(basis_vectors, delta)
    d = len(B)
    B_star = [np.zeros_like(B[0]) for _ in range(d)]
    Mu = np.zeros((d,d))
    
    for i in range(d):
        compute_gso(B, B_star, Mu, i)
        
    changed = True
    tour_count = 0
    while changed:
        tour_count += 1
        changed = False
        print(f"Starting Tour #{tour_count}...")
        
        for i in range(d - 1):
            h = min(i + blocksize, d)
            subbasis = B[i:h]
            
            # The "Oracle" call
            v = find_shortest_vector(subbasis)
            
            if v is not None and np.any(v != 0):
                norm_v = np.linalg.norm(v)
                norm_bi = np.linalg.norm(B[i])
                
                # If the Oracle found something better than our current leading vector
                if norm_v < delta * norm_bi:
                    B[i] = v
                    # Clean up the dependency created by inserting v
                    # We cast to list for your LLL_alg implementation
                    sub_list = [b.tolist() for b in B[i:h]]
                    refined_sub = LLL_alg(sub_list, delta)
                    B[i:i+len(refined_sub)] = [np.array(b) for b in refined_sub]
                    
                    # Refresh GSO for the whole basis after a change
                    for j in range(d):
                        compute_gso(B, B_star, Mu, j)
                    changed = True
        
    print(f"BKZ finished after {tour_count} tours.")
    return B

# --- FIXED TESTING BLOCK ---
basis_list = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]] 
# Added the required blocksize argument (e.g., 2 or 3)
reduced_basis1 = BKZ_alg(basis_list, blocksize=3)

print("\nFinal BKZ-reduced basis:")
for b in reduced_basis1:
    print(b)

basis_list = [[105, 821, 432], [123, 456, 789], [234, 567, 890], [345, 678, 901]]
reduced_basis2 = BKZ_alg(basis_list, blocksize=3)

print(f"My vector basis was:\n{basis_list}")
print("\nMy new LLL-reduced basis is (as numpy arrays):")
for b in basis_basis1:
    print(b)
for b in reduced_basis2:
    print(b)

"""
How it does what it doesies:
For a lattice basis L and a block size k:
    Beings wiht: Run LLL on the entire basis to get it into a decent starting shape.
    The Outer Loop (aka the Tours): Repeat the following until the basis stabilizes:
        The Inner Loop (Sliding Window): For i=1 to n−1:
            Define the current block size h=min(k,n−i+1).
            Local Projection: Project the vectors bi​,…,bi+h−1​ onto the space orthogonal to b1​,…,bi−1​. (Then this is the focus on the block).
            SVP Oracle: Find the absolute shortest vector (v) in this small h-dimensional projected lattice. HiHLYI EXPENSIVE
            Update: If this new vector v is shorter than the current bi​, insert it into the basis.  NOTE: IF 
            Local LLL: Because you just added a vector, the basis is now "linearly dependent" (too many vectors). Run LLL on this local block to remove the dependency and clean up the vectors.

    MAtches project overleaf documentation: 
    Algorithm 4 The basic BKZ algorithm
    Input: basis vectors b1, . . . , bn for a lattice
    Output: a BKZ-shortened lattice basis b1, . . . , bn
    while the last epoch did a nontrivial insertion do
        for i = 1, 2, . . . , n − 1 do
    h ← min(i + k − 1, n) {Block size k}
    v ← FullEnumeration(L[i,h])
            if ∥v∥ < δ∥bi∥ then
            LLL(. . . ) {Updating the basis }
            end if
        end for
    end while 

The idea is to use BKZ 2.0 with Pruning as our benchmark baseline because its behavior is well-characterized in the literature and it provides a stable environment for isolating the effects of our [Variable Change]. While Sieve-based variants offer better performance at blocksizes β>60, BKZ 2.0 remains the standard for assessing the fundamental efficiency of new reduction strategies.
"""