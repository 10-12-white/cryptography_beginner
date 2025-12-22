"""
This is normal BKZ:
For a lattice basis L and a block size k:
    Preprocessing: Run LLL on the entire basis to get it into a decent starting shape.
    The Outer Loop (Tours): Repeat the following until the basis stabilizes:
        The Inner Loop (Sliding Window): For i=1 to n−1:
            Define the current block size h=min(k,n−i+1).
            Local Projection: Project the vectors bi​,…,bi+h−1​ onto the space orthogonal to b1​,…,bi−1​.
            SVP Oracle: Find the absolute shortest vector (v) in this small h-dimensional projected lattice. This is the "expensive" part where we use enumeration or sieving.
            Update: If this new vector v is shorter than the current bi​, insert it into the basis.
            Local LLL: Because you just added a vector, the basis is now "linearly dependent" (too many vectors). Run LLL on this local block to remove the dependency and clean up the vectors.
    RETURN: Once you complete a full pass (a "tour") and no changes occur, the basis is BKZ-reduced.
    
DYNANIC BKZ is slightly different:

For a lattice basis L and a block size k:
    Preprocessing: Run LLL on the entire basis to get it into a decent starting shape.
    The Outer Loop (Tours): Repeat the following until the basis stabilizes :
        CHECK: IF RUN 2X, STOP ABORT.  This is because a lot of the runs done earliy, maybe 10x, etc, did not improve the performance of the basis, and then resulted in not better conditioning
            The Inner Loop (Sliding Window): For i=1 to n−1 OR OTHER NUMBER: (Skipping is introduced which allows the algorithm to run in large blocks, if there is less information in those vectors
                Define the current block size h=min(k,n−i+1).
                Local Projection: Project the vectors bi​,…,bi+h−1​ onto the space orthogonal to b1​,…,bi−1​.
                SVP Oracle: Find the absolute shortest vector (v) in this small h-dimensional projected lattice. This is the "expensive" part where we use enumeration or sieving.
                Update: If this new vector v is shorter than the current bi​, insert it into the basis.
                Local LLL: Because you just added a vector, the basis is now "linearly dependent" (too many vectors). Run LLL on this local block to remove the dependency and clean up the vectors.
        
    RETURN: Once you complete a full pass (a "tour") and no changes occur, the basis is BKZ-reduced.

3 Helper functions:

Block-Chunker-Decider: Before solving a block of size k with the SVP Oracle, 
BKZ 2.0 will recursively call a smaller BKZ (say, size k−10) on that local block.
It doesn't do this for every block. It decides whether to preprocess based on the current "state" of the basis.
If the block is already relatively "clean" (from a previous tour), it skips the extra work.

Probability helper: What chance do I have that this is better? If not, skip

Pruner helper:  It calculates a "pruning bounding function" dynamically for each block.
It essentially says: "I am going to ignore 99.9% of this search tree. I might miss the absolute shortest vector, 
but I will find a 'short enough' one 1,000 times faster."
    
"""

import numpy as np

# this takes in the basis vectors of the lattice basis
# then we will compute this based on a delta, which is our "loose" factor that allows our fraction that is not too loose, or not too tight
# block size included because change from LL to BKZ is this
def BKZ_alg(basis_vectors, blocksize, delta=0.75):
    # The input basis_vectors are a list of lists
    B = [np.array(v, dtype=float) for v in basis_vectors]
    d = len(B) # Dimension of the lattice basis

    # Initialize GSO matrices
    B_star = [np.zeros_like(B[0], dtype=float) for _ in range(d)]
    Mu = np.zeros((d, d), dtype=float)

    #Size-reduces b_k with respect to b_j by updating B[k].
    #The Mu matrix is updated for row k, which is needed
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
            # (Note: A more efficient method exists, but this is simpler).
            compute_gso(B, B_star, Mu, k - 1)
            compute_gso(B, B_star, Mu, k)

            # Return to the previous index k-1 to re-check the swapped vectors
            k = max(1, k - 1)

    # Return the LLL-reduced basis as a list of numpy arrays
    return B

# TESTING Usage:
basis_list = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]] 
reduced_basis1 = LLL_alg(basis_list)

basis_vectors = [[1,1],[1,100]]
reduced_basis2 = LLL_alg(basis_vectors)

print(f"My vector basis was:\n{basis_list}")
print("\nMy new LLL-reduced basis is (as numpy arrays):")
for b in reduced_basis1:
    print(b)
for b in reduced_basis2:
    print(b)

