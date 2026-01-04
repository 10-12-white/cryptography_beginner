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

LLL tuner from the first run through

Block-Chunker-Decider: Before solving a block of size k with the SVP Oracle, 
BKZ 2.0 will recursively call a smaller BKZ (say, size k−10) on that local block.
It doesn't do this for every block. It decides whether to preprocess based on the current "state" of the basis.
If the block is already relatively "clean" (from a previous tour), it skips the extra work.

Probability helper: What chance do I have that this is better? If not, skip

Pruner helper:  It calculates a "pruning bounding function" dynamically for each block.
It essentially says: "I am going to ignore 99.9% of this search tree. I might miss the absolute shortest vector, 
but I will find a 'short enough' one 1,000 times faster."

Link to this: https://github.com/Summwer/pro-pnj-bkz for inspiration

There is different probabilities for each block
"""





