### the next stage is BKZ

## different run times, and such....
## bkz relies on several things different to LLL - block size, and the same delta as before


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
