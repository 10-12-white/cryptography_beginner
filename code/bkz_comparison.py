
# What this code is for
# Create a definite way of comparing my proposed idea against the code of the BKZ 2.0 methoodoloy.
# This is important for:
    # reproducibility
    # fair comparison
    # future people to review my work
# I will use BKZ 2.0 to compare, NOT inclusive of the Gk6 library because it is a seiving methods
# Seiving methods are much more powerful, but they are not guaranteed to behave the same way twice
# FOr the intitial stages of my experiments, I need to be able to 

from fpylll import IntegerMatrix, BKZ, LLL, GSO

def get_bkz2_params(blocksize, max_loops=8):
    """
    Standard high-performance BKZ 2.0 settings for research benchmarks.
    """
    # BKZ 2.0 flags:
    # AUTO_ABORT: Stop if slope doesn't improve (GSA-based)
    # GH_BND: Use Gaussian Heuristic to bound SVP radius
    # MAX_LOOPS: Fixed cap on tours to ensure termination
    flags = BKZ.AUTO_ABORT | BKZ.GH_BND | BKZ.MAX_LOOPS
    
    # DEFAULT_STRATEGY: The JSON strategy file in fpylll containing 
    # pre-optimized pruning trees (the heart of 2.0 speed).
    params = BKZ.Param(
        block_size=blocksize, 
        strategies=BKZ.DEFAULT_STRATEGY, 
        max_loops=max_loops, 
        flags=flags
    )
    
    return params
    # Setup: Dimension 60 is chosen due to time cost, and also, ways in which we can improve the final outcomes

dim = 60
mat = load_svp_challenge(dim) # Darmstadt downloader from earlierm will probs be in the same file but separate for now

# --- STEP 1: BKZ 2.0 BASELINE ---
mat_bkz2 = IntegerMatrix(mat) # Work on a copy
params = get_bkz2_params(blocksize=40)

# Track time and quality
import time
start = time.perf_counter()
BKZ.reduction(mat_bkz2, params)
bkz2_time = time.perf_counter() - start
bkz2_quality = mat_bkz2[0].norm()

# --- STEP 2: MY ALGORITHM (To run on same DVP so that I can show comparison)

# proposed ideas: dual lattice with same features as the BKZ 2.0 for more components,
# but take into account that we will also use statistics that we pre-generate from running LLL first
# this will be the dual lengths, because we can use the dual function to calculate the length of the primal vectors, and the other way around
# we can also grab the Geometric Series from the LLL step
# we can also grab the GSO coefficients from the LL step to help with pruning

mat_my = IntegerMatrix(mat) # Work on a copy STILL IN PROG
start = time.perf_counter()
LLL.reduction(mat_my) # Preprocess with LLL
gso = GSO.Mat(mat_my)
blocksizeintial = 40
# start a normal BKZ loop
for block_start in range(0, dim, blocksizeintial):
    block_end = min(block_start + blocksizeintial, dim)
    block_size = block_end - block_start
    # extract the GSO for this block

def dual_block_reduction(basis, block_start, block_size):
    # gso
    gso = GSO.Mat(basis)
    gso.update_gso()
    
    # 2. Extract the local block we want to reduce in the dual
    # We find a short vector in the dual of the projected block.
    # This vector corresponds to a 'large gap' in the primal.
    
    # 3. Apply a Dual-SVP solver
    # fpylll's BKZ.Reduction does this internally if 'flags=BKZ.DUAL_REDUCTION'
    # In practice, self-dual BKZ uses a 'wrapper' that treats the 
    # reversed dual GSO as a primal GSO to save computation, because there is less work to do on the GSO, 
    # than to create A = B^-1 * t
    params = BKZ.Param(block_size=block_size, strategies=BKZ.DEFAULT_STRATEGY, 
                       flags=BKZ.DUAL_REDUCTION)
    
    BKZ.Reduction(gso, LLL.Wrapper(gso), params)()

    # return for the next component in the program
    # in otherwords, the basis has been computed in a faster technique than the way that was supposed
    # from the methods using GSO from the dual, as opposed to returning to work on the lattice
    # this is better than trying to solve in the space of primal, also
    # computationally
    return basis

dual_lengths = [gso.get_dual_length(i) for i in range(dim)]
# if the lengths are smaller, then the dual is easier to work in
# then we work in the dual for this component of the BKZ block
if dual_lengths[0] < mat_my[0].norm():
    gso.update_gso()
    # proceed with dual BKZ block reduction using my proposed method
    dual_block_reduction(mat_my, block_start, dim)
    else:
    # proceed with primal BKZ block reduction using my proposed method
    run_my_bkz_block_reduction(mat_my, gso, dual=False)
my_time = time.perf_counter() - start
my_quality = mat_my[0].norm()

# edit to fplll is the backend and super fast
from fpylll import LLL, BKZ, IntegerMatrix, GSO, SVP

# dual_block_reduc done by Micciancio & Walter's Self-Dual BKZ
# will return a basis that is dual-reduced for that block

# --- STEP 3: COMPARE
print("Comparison Results: ")
print(f"BKZ 2.0: Time = {bkz2_time:.2f}s, Quality = {bkz2_quality}")
print(f"My Alg: Time = {my_time:.2f}s, Quality = {my_quality}")


